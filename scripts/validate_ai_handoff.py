"""Validate the lightweight GitHub handoff directory.

This script is a publishing guard only. It does not run MATLAB, train CQL,
generate experiment data, or modify project files.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


MISSING = "\u672a\u751f\u6210"

REQUIRED_HANDOFF_FILES = [
    "README_AI_HANDOFF.md",
    "ACCOUNT_SWITCH_HANDOFF.md",
    "LATEST_STATUS.md",
    "CODEX_CHANGELOG.md",
    "CURRENT_DECISIONS.md",
    "KNOWN_ISSUES.md",
    "NEXT_PLAN.md",
    "REPORTS_INDEX.json",
    "RUNS_INDEX.json",
    "ARTIFACT_MANIFEST.json",
]

JSON_FILES = [
    "REPORTS_INDEX.json",
    "RUNS_INDEX.json",
    "ARTIFACT_MANIFEST.json",
]

FORBIDDEN_SUFFIXES = {
    ".jsonl",
    ".npz",
    ".pt",
    ".pth",
    ".ckpt",
    ".mat",
    ".fig",
    ".slxc",
    ".zip",
}

FORBIDDEN_NAMES = {"raw_steps.jsonl"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate ai_handoff before GitHub publishing.")
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Project root containing ai_handoff/.",
    )
    parser.add_argument(
        "--max-handoff-file-bytes",
        type=int,
        default=1_000_000,
        help="Maximum allowed size for any ai_handoff file.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.project_root.resolve()
    handoff_dir = root / "ai_handoff"
    failures: list[str] = []
    passes: list[str] = []

    if not handoff_dir.is_dir():
        failures.append(f"missing directory: {handoff_dir}")
        return finish(passes, failures)

    check_required_files(handoff_dir, passes, failures)
    json_docs = check_json_files(handoff_dir, passes, failures)
    check_index_paths(root, json_docs, passes, failures)
    check_forbidden_handoff_files(handoff_dir, args.max_handoff_file_bytes, passes, failures)
    check_latest_fields(handoff_dir, json_docs, passes, failures)

    return finish(passes, failures)


def check_required_files(handoff_dir: Path, passes: list[str], failures: list[str]) -> None:
    missing = [name for name in REQUIRED_HANDOFF_FILES if not (handoff_dir / name).is_file()]
    if missing:
        failures.append("missing required handoff files: " + ", ".join(missing))
        return
    passes.append(f"required handoff files exist: {len(REQUIRED_HANDOFF_FILES)}")


def check_json_files(
    handoff_dir: Path,
    passes: list[str],
    failures: list[str],
) -> dict[str, dict[str, Any]]:
    docs: dict[str, dict[str, Any]] = {}
    for name in JSON_FILES:
        path = handoff_dir / name
        try:
            with path.open("r", encoding="utf-8") as handle:
                docs[name] = json.load(handle)
        except Exception as exc:  # pragma: no cover - error text is the important output.
            failures.append(f"JSON parse failed for {path}: {exc}")
    if len(docs) == len(JSON_FILES):
        passes.append("handoff JSON files parse successfully")
    return docs


def check_index_paths(
    root: Path,
    docs: dict[str, dict[str, Any]],
    passes: list[str],
    failures: list[str],
) -> None:
    missing: list[str] = []

    reports = docs.get("REPORTS_INDEX.json", {}).get("reports", [])
    for item in reports:
        if item.get("status") == MISSING:
            continue
        rel_path = item.get("path")
        if not rel_path:
            missing.append("<REPORTS_INDEX item missing path>")
        elif not (root / rel_path).exists():
            missing.append(str(rel_path))

    runs = docs.get("RUNS_INDEX.json", {}).get("runs", [])
    for item in runs:
        rel_path = item.get("path")
        if not rel_path:
            missing.append("<RUNS_INDEX item missing path>")
        elif not (root / rel_path).exists():
            missing.append(str(rel_path))

    artifacts = docs.get("ARTIFACT_MANIFEST.json", {}).get("artifacts", [])
    for item in artifacts:
        rel_path = item.get("path")
        if not rel_path:
            missing.append("<ARTIFACT_MANIFEST item missing path>")
        elif not (root / rel_path).exists():
            missing.append(str(rel_path))

    if missing:
        failures.append("indexed paths missing: " + "; ".join(missing))
        return
    passes.append("all indexed report, run, and artifact paths exist")


def check_forbidden_handoff_files(
    handoff_dir: Path,
    max_bytes: int,
    passes: list[str],
    failures: list[str],
) -> None:
    forbidden: list[str] = []
    oversized: list[str] = []
    for path in handoff_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.name in FORBIDDEN_NAMES or path.suffix.lower() in FORBIDDEN_SUFFIXES:
            forbidden.append(str(path))
        if path.stat().st_size > max_bytes:
            oversized.append(f"{path} ({path.stat().st_size} bytes)")

    if forbidden:
        failures.append("forbidden files inside ai_handoff: " + "; ".join(forbidden))
    else:
        passes.append("no forbidden raw data/checkpoint/binary files inside ai_handoff")

    if oversized:
        failures.append("oversized files inside ai_handoff: " + "; ".join(oversized))
    else:
        passes.append(f"all ai_handoff files are <= {max_bytes} bytes")


def check_latest_fields(
    handoff_dir: Path,
    docs: dict[str, dict[str, Any]],
    passes: list[str],
    failures: list[str],
) -> None:
    run_index = docs.get("RUNS_INDEX.json", {})
    latest_run = run_index.get("latest_completed_run_id")
    run_ids = {item.get("run_id") for item in run_index.get("runs", [])}
    if not latest_run:
        failures.append("RUNS_INDEX.json missing latest_completed_run_id")
    elif latest_run not in run_ids:
        failures.append(f"latest_completed_run_id not present in runs list: {latest_run}")
    else:
        passes.append(f"latest run field is present: {latest_run}")

    reports_index = docs.get("REPORTS_INDEX.json", {})
    if not reports_index.get("latest_run"):
        failures.append("REPORTS_INDEX.json missing latest_run")
    elif not reports_index.get("reports"):
        failures.append("REPORTS_INDEX.json has no reports")
    else:
        passes.append(f"latest report index field is present for run: {reports_index['latest_run']}")

    required_text_markers = {
        "ACCOUNT_SWITCH_HANDOFF.md": ["Can A New Codex Take Over?", "Start Here", "Do Not Do"],
        "LATEST_STATUS.md": ["Latest Completed Run", "Latest Report Pointers", "Safe To Proceed?"],
        "KNOWN_ISSUES.md": ["Current Blockers", "Explicit Non-Claims"],
        "NEXT_PLAN.md": ["Immediate Safe Work", "Decision Gates", "Do Not Do Yet"],
        "README_AI_HANDOFF.md": ["Current Headline", "Most Important Local Reports"],
    }
    marker_failures: list[str] = []
    for file_name, markers in required_text_markers.items():
        text = (handoff_dir / file_name).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                marker_failures.append(f"{file_name} missing marker: {marker}")

    if marker_failures:
        failures.append("latest report/blocker text fields missing: " + "; ".join(marker_failures))
    else:
        passes.append("latest run, latest report, and blocker sections are present")


def finish(passes: list[str], failures: list[str]) -> int:
    print("AI handoff validation")
    for item in passes:
        print(f"PASS: {item}")
    for item in failures:
        print(f"FAIL: {item}")
    print(f"SUMMARY: {'PASS' if not failures else 'FAIL'}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())

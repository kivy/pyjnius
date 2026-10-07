"""Check that a release tag matches the version packaged by pyjnius."""

import ast
from pathlib import Path
import re
import sys


TAG_PATTERN = re.compile(r"(?P<version>[0-9]+\.[0-9]+\.[0-9]+)(?:-test)?")
AD_HOC_TEST_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9._-]*-test")
VERSION_FILE = Path(__file__).resolve().parents[2] / "jnius" / "__init__.py"


def package_version(source):
    """Read the single literal top-level version without importing jnius.

    Assignments inside conditional blocks are not inspected.
    """
    assignments = []
    for statement in ast.parse(source).body:
        if isinstance(statement, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == "__version__"
                   for target in statement.targets):
                assignments.append(statement.value if len(statement.targets) == 1 else None)
        elif isinstance(statement, ast.AnnAssign):
            if isinstance(statement.target, ast.Name) and statement.target.id == "__version__":
                raise ValueError("Annotated __version__ is not supported by this check; use __version__ = 'X.Y.Z'")

    if len(assignments) != 1:
        raise ValueError("Expected exactly one top-level __version__ assignment in jnius/__init__.py")
    value = assignments[0]
    if not isinstance(value, ast.Constant) or not isinstance(value.value, str):
        raise ValueError("Expected a string literal for __version__ in jnius/__init__.py")
    return value.value


def check_release_version(tag, source_path=VERSION_FILE):
    match = TAG_PATTERN.fullmatch(tag)
    if match is None:
        # Historical issue-specific test tags build desktop prereleases on TestPyPI.
        # Stable tags must always match the packaged version.
        if AD_HOC_TEST_PATTERN.fullmatch(tag):
            return
        raise ValueError(f"Invalid release tag {tag!r}; expected X.Y.Z, X.Y.Z-test, or an ad-hoc -test tag")

    version = package_version(Path(source_path).read_text(encoding="utf-8"))
    if match.group("version") != version:
        raise ValueError(f"Release tag {tag!r} does not match package version {version!r} in jnius/__init__.py")


def main(argv):
    if len(argv) != 1:
        print("Usage: check_release_version.py X.Y.Z[-test] | ad-hoc-test", file=sys.stderr)
        return 1
    try:
        check_release_version(argv[0])
    except (ValueError, OSError, SyntaxError) as exc:
        print(f"Release version check failed: {exc}", file=sys.stderr)
        return 1
    print(f"Release tag {argv[0]!r} passed release version check")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

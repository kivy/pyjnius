"""Release validation must work without importing the JNI extension."""

import importlib.util
from pathlib import Path
import subprocess
import sys

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "check_release_version.py"
spec = importlib.util.spec_from_file_location("check_release_version", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


@pytest.mark.parametrize("tag", ["1.8.0", "1.8.0-test"])
def test_matching_tags(tmp_path, tag):
    source = tmp_path / "__init__.py"
    source.write_text("__version__ = '1.8.0'\nraise RuntimeError('must not execute')\n", encoding="utf-8")
    assert validator.check_release_version(tag, source) is None


def test_ad_hoc_test_tag_does_not_require_version(tmp_path):
    source = tmp_path / "__init__.py"
    source.write_text("__version__ = '1.8.0'\n", encoding="utf-8")
    assert validator.check_release_version("issue_428-test", source) is None


@pytest.mark.parametrize("tag", ["", "v1.8.0", "1.8", "1.8.0-dev0", "1.8.0-test-extra", "1.8.0\n", "issue_428", "1.9.0-test-extra", "issue_428\n-test"])
def test_invalid_tag(tmp_path, tag):
    source = tmp_path / "__init__.py"
    source.write_text("__version__ = '1.8.0'\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid release tag"):
        validator.check_release_version(tag, source)


@pytest.mark.parametrize("source, message", [
    ("pass\n", "exactly one"),
    ("__version__ = get_version()\n", "string literal"),
    ("__version__ = 123\n", "string literal"),
    ("__version__ = '1.8.0'\n__version__ = '1.8.0'\n", "exactly one"),
    ("__version__: str = '1.8.0'\n", "Annotated __version__"),
    ("__version__: str\n", "Annotated __version__"),
])
def test_invalid_version_source(source, message):
    with pytest.raises(ValueError, match=message):
        validator.package_version(source)


def test_mismatch_names_tag_and_package_version(tmp_path):
    source = tmp_path / "__init__.py"
    source.write_text("__version__ = '1.3.0-dev0'\n", encoding="utf-8")
    with pytest.raises(ValueError, match="1.3.0.*1.3.0-dev0"):
        validator.check_release_version("1.3.0", source)


def test_cli_reports_mismatch():
    current_version = validator.package_version(validator.VERSION_FILE.read_text(encoding="utf-8"))
    mismatched_tag = "0.0.0" if current_version != "0.0.0" else "0.0.1"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), mismatched_tag],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 1
    assert mismatched_tag in result.stderr
    assert current_version in result.stderr

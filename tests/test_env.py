from pathlib import Path

import pytest

from jnius_config import env


@pytest.mark.parametrize("architecture", ["ppc64", "ppc64le", "s390x", "aarch64"])
def test_unix_jvm_library_lookup_uses_machine_architecture(
    architecture, monkeypatch, tmp_path
):
    monkeypatch.setattr(env, "machine", architecture)
    library = tmp_path / "jre" / "lib" / architecture / "server" / "libjvm.so"
    library.parent.mkdir(parents=True)
    library.touch()

    java = env.UnixJavaLocation("linux", str(tmp_path))
    assert Path(java.get_jnius_lib_location()) == library

from os.path import join
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


@pytest.mark.parametrize(
    ("variables", "chosen"),
    [
        ({"JAVA_HOME": "java", "JDK_HOME": "jdk", "JRE_HOME": "jre"}, "java"),
        ({"JDK_HOME": "jdk", "JRE_HOME": "jre"}, "jdk"),
        ({"JRE_HOME": "jre"}, "jre"),
    ],
)
def test_java_setup_prefers_home_variables(
    variables, chosen, monkeypatch, tmp_path
):
    for key in ("JAVA_HOME", "JDK_HOME", "JRE_HOME"):
        monkeypatch.delenv(key, raising=False)
    for key, directory in variables.items():
        monkeypatch.setenv(key, str(tmp_path / directory))

    location = env.get_java_setup("linux")
    assert isinstance(location, env.UnixJavaLocation)
    assert location.get_javahome() == str(tmp_path / chosen)


def test_jvm_path_overrides_library_lookup(monkeypatch, tmp_path):
    override = tmp_path / "explicit" / "libjvm.so"
    monkeypatch.setenv("JVM_PATH", str(override))

    location = env.UnixJavaLocation("linux", str(tmp_path / "java"))
    assert location.get_jnius_lib_location() == str(override)


def test_missing_jvm_library_reports_candidates(monkeypatch, tmp_path):
    monkeypatch.delenv("JVM_PATH", raising=False)
    monkeypatch.setattr(env, "machine", "x86_64")
    home = tmp_path / "missing-java"
    location = env.UnixJavaLocation("linux", str(home))

    with pytest.raises(RuntimeError) as error:
        location.get_jnius_lib_location()

    message = str(error.value)
    assert "JVM_PATH" in message
    for relative in (
        "lib/server/libjvm.so",
        "jre/lib/amd64/default/libjvm.so",
        "jre/lib/amd64/server/libjvm.so",
    ):
        assert repr(join(str(home), relative)) in message

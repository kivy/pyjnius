from os.path import join
from pathlib import Path

import pytest

from jnius_config import env


@pytest.fixture
def cleared_java_homes(monkeypatch):
    for name in ("JAVA_HOME", "JDK_HOME", "JRE_HOME"):
        monkeypatch.delenv(name, raising=False)


@pytest.mark.parametrize(
    "architecture", ["ppc64", "ppc64le", "s390x", "aarch64"]
)
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
    ("platform", "location_type"),
    [("linux", env.UnixJavaLocation), ("win32", env.WindowsJavaLocation)],
)
@pytest.mark.parametrize(
    ("variables", "chosen"),
    [
        ({"JAVA_HOME": "java", "JDK_HOME": "jdk", "JRE_HOME": "jre"}, "java"),
        ({"JDK_HOME": "jdk", "JRE_HOME": "jre"}, "jdk"),
        ({"JRE_HOME": "jre"}, "jre"),
    ],
)
def test_java_setup_prefers_home_variables(
    platform, location_type, variables, chosen, monkeypatch, tmp_path
):
    for key in ("JAVA_HOME", "JDK_HOME", "JRE_HOME"):
        monkeypatch.delenv(key, raising=False)
    for key, directory in variables.items():
        monkeypatch.setenv(key, str(tmp_path / directory))
    monkeypatch.setattr(
        env, "which", lambda command: pytest.fail(f"PATH probed: {command}")
    )

    location = env.get_java_setup(platform)
    assert isinstance(location, location_type)
    assert location.get_javahome() == str(tmp_path / chosen)


def test_jdk_home_uses_existing_explicit_home(
    cleared_java_homes, monkeypatch, tmp_path
):
    home = tmp_path / "selected-jdk"
    home.mkdir()
    monkeypatch.setenv("JDK_HOME", str(home))
    monkeypatch.setattr(
        env, "which", lambda command: pytest.fail(f"PATH probed: {command}")
    )

    assert env.get_jdk_home("linux") == str(home)


def test_jdk_home_rejects_nonexistent_explicit_home(
    cleared_java_homes, monkeypatch, tmp_path
):
    home = tmp_path / "missing-jdk"
    monkeypatch.setenv("JDK_HOME", str(home))
    monkeypatch.setattr(
        env, "which", lambda command: pytest.fail(f"PATH probed: {command}")
    )

    assert env.get_jdk_home("linux") is None


def test_java_setup_discovers_resolved_path_jdk(
    cleared_java_homes, monkeypatch
):
    executables = {
        "javac": "/path-entry/javac",
        "java": "/path-entry/java",
    }
    resolved = {
        "/path-entry/javac": "/resolved-jdk/bin/javac",
        "/path-entry/java": "/resolved-jre/bin/java",
    }
    monkeypatch.setattr(env, "which", executables.__getitem__)
    monkeypatch.setattr(env, "realpath", resolved.__getitem__)
    monkeypatch.setattr(
        env, "exists",
        lambda path: path in ("/resolved-jdk/", "/resolved-jre/"),
    )

    location = env.get_java_setup("linux")
    assert isinstance(location, env.UnixJavaLocation)
    assert location.get_javahome() == "/resolved-jdk/"


@pytest.mark.parametrize("home_suffix", ["bin", ""])
def test_jdk_home_recognizes_windows_compiler(
    home_suffix, cleared_java_homes, monkeypatch, tmp_path
):
    home = tmp_path / "windows-java"
    (home / "bin").mkdir(parents=True)
    (home / "bin" / "javac.exe").touch()
    monkeypatch.setenv("JAVA_HOME", str(home / home_suffix))

    assert Path(env.get_jdk_home("win32")) == home


def test_jdk_home_rejects_windows_runtime(
    cleared_java_homes, monkeypatch, tmp_path
):
    home = tmp_path / "windows-runtime"
    (home / "bin").mkdir(parents=True)
    monkeypatch.setenv("JAVA_HOME", str(home))

    assert env.get_jdk_home("win32") is None


def test_jdk_home_returns_none_without_path_compiler(
    cleared_java_homes, monkeypatch
):
    monkeypatch.setattr(env, "which", {"javac": None}.__getitem__)

    assert env.get_jdk_home("linux") is None


def test_jdk_home_returns_none_without_windows_home(
    cleared_java_homes, monkeypatch
):
    monkeypatch.setattr(
        env, "which", lambda command: pytest.fail(f"PATH probed: {command}")
    )

    assert env.get_jdk_home("win32") is None


@pytest.mark.parametrize(
    ("platform", "location_type"),
    [("linux", env.UnixJavaLocation), ("freebsd14", env.BSDJavaLocation)],
)
@pytest.mark.parametrize(
    ("architecture", "relative_library"),
    [
        ("x86_64", "lib/server/libjvm.so"),
        ("x86_64", "lib/amd64/server/libjvm.so"),
        ("aarch64", "lib/aarch64/server/libjvm.so"),
    ],
)
def test_java_setup_falls_back_to_path_jre(
    platform, location_type, architecture, relative_library,
    cleared_java_homes, monkeypatch, tmp_path
):
    home = tmp_path / "runtime-only"
    library = home / relative_library
    library.parent.mkdir(parents=True)
    library.touch()
    monkeypatch.delenv("JVM_PATH", raising=False)
    monkeypatch.setattr(env, "machine", architecture)
    executables = {"javac": None, "java": "/path-entry/java"}
    resolved = {"/path-entry/java": (home / "bin" / "java").as_posix()}
    monkeypatch.setattr(env, "which", executables.__getitem__)
    monkeypatch.setattr(env, "realpath", resolved.__getitem__)

    location = env.get_java_setup(platform)
    assert isinstance(location, location_type)
    assert Path(location.get_javahome()) == home
    assert not location.is_jdk()
    assert Path(location.get_jnius_lib_location()) == library


def test_java_setup_keeps_explicit_runtime(
    cleared_java_homes, monkeypatch, tmp_path
):
    home = tmp_path / "explicit-runtime"
    (home / "bin").mkdir(parents=True)
    monkeypatch.setenv("JAVA_HOME", str(home))
    monkeypatch.setattr(
        env, "which", lambda command: pytest.fail(f"PATH probed: {command}")
    )

    location = env.get_java_setup("linux")
    assert Path(location.get_javahome()) == home
    assert not location.is_jdk()


@pytest.mark.parametrize("platform", ["linux", "win32"])
def test_jre_home_uses_nested_runtime(
    platform, cleared_java_homes, monkeypatch, tmp_path
):
    home = tmp_path / "jre"
    home.mkdir()
    monkeypatch.setenv("JAVA_HOME", str(tmp_path))
    monkeypatch.setattr(
        env, "which", lambda command: pytest.fail(f"PATH probed: {command}")
    )

    assert Path(env.get_jre_home(platform)) == home


@pytest.mark.parametrize(
    ("available_homes", "expected_home"),
    [
        (
            (
                "/usr/java/latest/",
                "/usr/java/default/",
                "/usr/lib/jvm/default-java/",
            ),
            "/usr/java/latest/",
        ),
        (
            ("/usr/java/default/", "/usr/lib/jvm/default-java/"),
            "/usr/java/default/",
        ),
        (("/usr/lib/jvm/default-java/",), "/usr/lib/jvm/default-java/"),
    ],
)
def test_java_setup_uses_first_default_runtime(
    available_homes, expected_home, cleared_java_homes, monkeypatch
):
    executables = {join(home, "bin", "java") for home in available_homes}
    monkeypatch.setattr(
        env, "which", {"javac": None, "java": None}.__getitem__
    )
    monkeypatch.setattr(env, "exists", executables.__contains__)

    location = env.get_java_setup("linux")
    assert isinstance(location, env.UnixJavaLocation)
    assert location.get_javahome() == expected_home


def test_jre_home_returns_none_when_exhausted(cleared_java_homes, monkeypatch):
    monkeypatch.setattr(env, "which", {"java": None}.__getitem__)
    monkeypatch.setattr(env, "exists", lambda path: False)

    assert env.get_jre_home("linux") is None


def test_jre_home_returns_none_without_windows_home(
    cleared_java_homes, monkeypatch
):
    monkeypatch.setattr(
        env, "which", lambda command: pytest.fail(f"PATH probed: {command}")
    )

    assert env.get_jre_home("win32") is None


@pytest.mark.parametrize("platform", ["linux", "win32"])
@pytest.mark.parametrize(
    "variables",
    [{}, {"JAVA_HOME": "", "JDK_HOME": "", "JRE_HOME": ""}],
    ids=["absent", "empty"],
)
def test_java_setup_reports_exhausted_discovery(
    platform, variables, cleared_java_homes, monkeypatch
):
    for name, value in variables.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setattr(
        env, "which", {"javac": None, "java": None}.__getitem__
    )
    monkeypatch.setattr(env, "exists", lambda path: False)

    with pytest.raises(RuntimeError, match="JAVA_HOME"):
        env.get_java_setup(platform)


@pytest.mark.parametrize(
    "discover_home", [env.get_jdk_home, env.get_jre_home]
)
def test_discovery_propagates_executable_probe_error(
    discover_home, cleared_java_homes, monkeypatch
):
    error = OSError("executable probe failed")

    def which(command):
        raise error

    monkeypatch.setattr(env, "which", which)

    with pytest.raises(OSError) as raised:
        discover_home("linux")

    assert raised.value is error


@pytest.mark.parametrize(
    "discover_home", [env.get_jdk_home, env.get_jre_home]
)
def test_discovery_propagates_resolution_error(
    discover_home, cleared_java_homes, monkeypatch
):
    error = TypeError("unexpected resolution failure")

    def realpath(path):
        raise error

    monkeypatch.setattr(
        env, "which",
        {"javac": "/path-entry/javac", "java": "/path-entry/java"}.__getitem__,
    )
    monkeypatch.setattr(env, "realpath", realpath)

    with pytest.raises(TypeError) as raised:
        discover_home("linux")

    assert raised.value is error


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
        "lib/amd64/server/libjvm.so",
    ):
        assert repr(join(str(home), relative)) in message


def test_windows_java_location_build_paths(monkeypatch, tmp_path):
    home = tmp_path / "windows-java"
    monkeypatch.setenv("JAVA_HOME", str(home))

    location = env.get_java_setup("win32")
    assert isinstance(location, env.WindowsJavaLocation)
    assert location.get_javahome() == str(home)
    assert location.get_java() == join(str(home), "bin", "java") + ".exe"
    assert location.get_javac() == join(str(home), "bin", "javac") + ".exe"
    assert not location.is_jdk()
    (home / "bin").mkdir(parents=True)
    (home / "bin" / "javac.exe").touch()
    assert location.is_jdk()
    assert location.get_include_dirs() == [
        join(str(home), "include"), join(str(home), "include", "win32")
    ]
    assert location.get_libraries() == ["jvm"]
    assert location.get_library_dirs() == [
        join(str(home), "lib"), join(str(home), "bin", "server")
    ]


def test_android_java_location_build_paths(monkeypatch, tmp_path):
    home = tmp_path / "android-java"
    monkeypatch.setenv("JAVA_HOME", str(home))

    location = env.get_java_setup("android")
    assert isinstance(location, env.AndroidJavaLocation)
    assert location.get_javahome() == str(home)
    assert location.get_libraries() == ["log"]
    assert location.get_include_dirs() == []
    assert location.get_library_dirs() == []


def test_bsd_java_location_include_and_library(monkeypatch, tmp_path):
    home = tmp_path / "bsd-java"
    monkeypatch.setenv("JAVA_HOME", str(home))
    monkeypatch.delenv("JVM_PATH", raising=False)
    library = home / "lib" / "server" / "libjvm.so"
    library.parent.mkdir(parents=True)
    library.touch()

    location = env.get_java_setup("freebsd14")
    assert isinstance(location, env.BSDJavaLocation)
    assert location.get_javahome() == str(home)
    assert location.get_include_dirs() == [
        join(str(home), "include"), join(str(home), "include", "freebsd")
    ]
    assert Path(location.get_jnius_lib_location()) == library


def test_modern_macos_java_location_include_and_library(monkeypatch, tmp_path):
    home = tmp_path / "modern-macos-java"
    monkeypatch.setenv("JAVA_HOME", str(home))
    monkeypatch.delenv("JVM_PATH", raising=False)
    library = home / "lib" / "jli" / "libjli.dylib"
    library.parent.mkdir(parents=True)
    library.touch()

    location = env.get_java_setup("darwin")
    assert isinstance(location, env.MacOsXJavaLocation)
    assert location.get_javahome() == str(home)
    assert location.get_include_dirs() == [
        join(str(home), "include"), join(str(home), "include", "darwin")
    ]
    assert Path(location.get_jnius_lib_location()) == library

"""Java helper targeting checks that do not import JNI or start a JVM."""

import subprocess
from textwrap import dedent

import pytest

from jnius_config import env


@pytest.mark.parametrize(
    ("version", "options"),
    [
        ("javac 1.8.0_504\n", ["-source", "8", "-target", "8"]),
        ("javac 9.0.4\n", ["--release", "8"]),
        ("javac 11.0.30\n", ["--release", "8"]),
        ("javac 17.0.20.1\n", ["--release", "8"]),
        ("javac 25\n", ["--release", "8"]),
        ("javac 25-ea\n", ["--release", "8"]),
        (
            "Picked up JAVA_TOOL_OPTIONS: -Xmx256m\njavac 1.8.0_504\n",
            ["-source", "8", "-target", "8"],
        ),
        (
            "NOTE: Picked up JDK_JAVAC_OPTIONS: -J-Xmx256m\njavac 25-ea\n",
            ["--release", "8"],
        ),
    ],
)
def test_javac_options_select_java8_target(version, options, monkeypatch):
    monkeypatch.setattr(env, "check_output", lambda *args, **kwargs: version)

    assert env.get_javac_options("/selected/jdk/bin/javac") == options


@pytest.mark.parametrize(
    "javac",
    [
        "/selected/jdk/bin/javac",
        "/opt/Java Development Kit/bin/javac",
        r"C:\Program Files\Java\jdk-17\bin\javac.exe",
    ],
)
def test_javac_probe_uses_selected_executable(javac, monkeypatch):
    calls = []

    def check_output(*args, **kwargs):
        calls.append((args, kwargs))
        return "javac 17.0.20.1\n"

    monkeypatch.setattr(env, "check_output", check_output)

    assert env.get_javac_options(javac) == ["--release", "8"]
    assert calls == [
        (([javac, "-version"],), {"stderr": subprocess.STDOUT, "text": True})
    ]


@pytest.mark.parametrize(
    "version",
    ["", 'openjdk version "17.0.20.1"\n', "javac unknown\n", "javac 17invalid\n"],
)
def test_javac_options_reject_unknown_version(version, monkeypatch):
    monkeypatch.setattr(env, "check_output", lambda *args, **kwargs: version)
    javac = "/selected/jdk/bin/javac"

    with pytest.raises(
        RuntimeError, match="Could not determine Java compiler version"
    ) as error:
        env.get_javac_options(javac)

    assert repr(javac) in str(error.value)
    assert repr(version) in str(error.value)


@pytest.mark.parametrize("version", ["javac 1.7.0_80\n", "javac 7\n"])
def test_javac_options_reject_old_compiler(version, monkeypatch):
    monkeypatch.setattr(env, "check_output", lambda *args, **kwargs: version)

    with pytest.raises(RuntimeError, match="requires JDK 8 or newer"):
        env.get_javac_options("/selected/jdk/bin/javac")


@pytest.mark.parametrize(
    "error",
    [
        subprocess.CalledProcessError(1, ["/selected/jdk/bin/javac", "-version"]),
        FileNotFoundError("selected compiler is missing"),
    ],
)
def test_javac_probe_errors_propagate(error, monkeypatch):
    calls = []

    def check_output(*args, **kwargs):
        calls.append((args, kwargs))
        raise error

    monkeypatch.setattr(env, "check_output", check_output)

    with pytest.raises(type(error)) as raised:
        env.get_javac_options("/selected/jdk/bin/javac")

    assert raised.value is error
    assert len(calls) == 1


def test_real_javac_enforces_java8_api_target(tmp_path):
    java = env.get_java_setup()
    javac = java.get_javac()
    if not java.is_jdk():
        pytest.skip(f"real_javac requires a JDK compiler; {javac!r} is unavailable")
    options = env.get_javac_options(javac)
    sources = tmp_path / "sources"
    sources.mkdir()
    positive = sources / "Java8ApiProbe.java"
    positive.write_text(dedent("""\
        public class Java8ApiProbe {
            public static String encode(byte[] value) {
                return java.util.Base64.getEncoder().encodeToString(value);
            }
        }
        """), encoding="utf-8")
    negative = sources / "NewApiProbe.java"
    negative.write_text(dedent("""\
        public class NewApiProbe {
            public static java.util.List<String> values() {
                return java.util.List.of("probe");
            }
        }
        """), encoding="utf-8")

    def compile_source(source, output, target_options):
        output.mkdir()
        return subprocess.run(
            [javac, *target_options, "-d", str(output), str(source)],
            capture_output=True, text=True, check=False,
        )

    java8_output = tmp_path / "java8-classes"
    result = compile_source(positive, java8_output, options)
    assert result.returncode == 0, result.stdout + result.stderr
    header = (java8_output / "Java8ApiProbe.class").read_bytes()[:8]
    assert header[:4] == b"\xca\xfe\xba\xbe"
    assert int.from_bytes(header[6:8], "big") == 52

    rejected_output = tmp_path / "rejected-classes"
    result = compile_source(negative, rejected_output, options)
    assert result.returncode != 0, result.stdout + result.stderr
    assert not (rejected_output / "NewApiProbe.class").exists()

    if "--release" in options:
        untargeted_output = tmp_path / "untargeted-classes"
        result = compile_source(negative, untargeted_output, [])
        assert result.returncode == 0, result.stdout + result.stderr
        assert (untargeted_output / "NewApiProbe.class").is_file()

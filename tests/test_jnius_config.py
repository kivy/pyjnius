from importlib import resources
import os

import pytest
import jnius_config


@pytest.fixture
def packaged_java_src(monkeypatch, tmp_path):
    package = tmp_path / "jnius"
    source = package / "src"
    source.mkdir(parents=True)

    def files(name):
        assert name == "jnius"
        return package

    monkeypatch.setattr(resources, "files", files)
    return source


class TestJniusConfig:
    def setup_method(self):
        """Resets the options global."""
        jnius_config.options = []
        jnius_config.vm_running = False
        jnius_config.vm_started_at = None
        jnius_config.classpath = None

    def teardown_method(self):
        self.setup_method()

    @pytest.mark.parametrize(
        "function,args",
        [
            (jnius_config.set_options, ("option1",)),
            (jnius_config.add_options, ("option1",)),
            (jnius_config.set_classpath, (".",)),
            (jnius_config.add_classpath, (".",)),
        ],
    )
    def test_set_options_vm_running(self, function, args):
        """The functions should only raise an error when the vm is running."""
        assert jnius_config.vm_running is False
        function(*args)
        jnius_config.vm_started_at = "test stack"
        jnius_config.vm_running = True
        with pytest.raises(ValueError) as ex_info:
            function(*args)
        assert "VM is already running, can't set" in ex_info.value.args[0]

    def test_set_options(self):
        assert jnius_config.vm_running is False
        assert jnius_config.options == []
        jnius_config.set_options("option1", "option2")
        assert jnius_config.options == ["option1", "option2"]
        jnius_config.set_options("option3")
        assert jnius_config.options == ["option3"]

    def test_add_options(self):
        assert jnius_config.vm_running is False
        assert jnius_config.options == []
        jnius_config.add_options("option1", "option2")
        assert jnius_config.options == ["option1", "option2"]
        jnius_config.add_options("option3")
        assert jnius_config.options == ["option1", "option2", "option3"]

    def test_set_classpath(self):
        assert jnius_config.vm_running is False
        assert jnius_config.classpath is None
        jnius_config.set_classpath(".")
        assert jnius_config.classpath == ["."]
        jnius_config.set_classpath(".", "/usr/local/fem/plugins/*")
        assert jnius_config.classpath == [".", "/usr/local/fem/plugins/*"]

    def test_add_classpath(self):
        assert jnius_config.vm_running is False
        assert jnius_config.classpath is None
        jnius_config.add_classpath(".")
        assert jnius_config.classpath == ["."]
        jnius_config.add_classpath("/usr/local/fem/plugins/*")
        assert jnius_config.classpath == [".", "/usr/local/fem/plugins/*"]

    def test_get_classpath_explicit_overrides_environment(
        self, monkeypatch, tmp_path, packaged_java_src
    ):
        monkeypatch.setenv("CLASSPATH", str(tmp_path / "from-env"))
        explicit = [str(tmp_path / "first"), str(tmp_path / "second")]
        jnius_config.set_classpath(*explicit)

        result = jnius_config.get_classpath()
        assert result[:-1] == explicit
        assert result[-1] == str(packaged_java_src)

    def test_get_classpath_from_environment(
        self, monkeypatch, tmp_path, packaged_java_src
    ):
        entries = [str(tmp_path / "first"), str(tmp_path / "second")]
        monkeypatch.setenv("CLASSPATH", jnius_config.split_char.join(entries))

        result = jnius_config.get_classpath()
        assert result[:-1] == entries
        assert result[-1] == str(packaged_java_src)

    def test_get_classpath_defaults_to_working_directory(
        self, monkeypatch, tmp_path, packaged_java_src
    ):
        monkeypatch.delenv("CLASSPATH", raising=False)
        monkeypatch.chdir(tmp_path)

        result = jnius_config.get_classpath()
        assert result[:-1] == [os.path.realpath(".")]
        assert result[-1] == str(packaged_java_src)

    def test_expand_classpath_matches_jars(
        self, monkeypatch, tmp_path, packaged_java_src
    ):
        monkeypatch.delenv("CLASSPATH", raising=False)
        jars = tmp_path / "plugins"
        jars.mkdir()
        first = jars / "first.jar"
        second = jars / "second.JAR"
        first.touch()
        second.touch()
        (jars / "ignore.txt").touch()
        literal = str(tmp_path / "literal")
        jnius_config.set_classpath(literal, str(jars / "*"))

        entries = jnius_config.expand_classpath().split(jnius_config.split_char)
        assert entries[0] == literal
        assert len(entries) == 4
        assert set(entries[1:-1]) == {str(first), str(second)}
        assert entries[-1] == str(packaged_java_src)

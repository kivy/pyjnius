import sys
import pytest
import jnius_config


class TestJniusConfig:
    def setup_method(self):
        """Resets the options global."""
        jnius_config.options = []
        jnius_config.vm_running = False
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
        jnius_config.vm_running = True
        with pytest.raises(ValueError) as ex_info:
            function(*args)
        pytest.mark.skipif(
            sys.version_info < (3, 5), reason="Exception args are different on Python 2"
        )
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

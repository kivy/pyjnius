import sys
import pytest
import jnius_config


class TestJniusConfig:
    def setup_method(self):
        """Resets the options global."""
        jnius_config.options = []
        jnius_config.vm_running = False

    def teardown_method(self):
        self.setup_method()

    def test_set_options(self):
        assert jnius_config.vm_running is False
        assert jnius_config.options == []
        jnius_config.set_options("option1", "option2")
        assert jnius_config.options == ["option1", "option2"]
        jnius_config.set_options("option3")
        assert jnius_config.options == ["option3"]

    def test_set_options_vm_running(self):
        assert jnius_config.vm_running is False
        jnius_config.set_options("option1", "option2")
        jnius_config.vm_running = True
        with pytest.raises(ValueError) as ex_info:
            jnius_config.set_options("option1", "option2")
        pytest.mark.skipif(
            sys.version_info < (3, 5), reason="Exception args are different on Python 2"
        )
        assert (
            "VM is already running, can't set options; VM started at"
            in ex_info.value.args[0]
        )

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import json
import pytest
import subprocess
import sys
import textwrap


class TestJVMOptions:
    @pytest.mark.skipif(
        sys.platform == 'android',
        reason='JNIus on Android does not take JVM options'
    )
    def test_jvm_options(self):
        options = ['-Dtest.var{}=value'.format(i) for i in range(40)]
        process = subprocess.Popen([sys.executable, '-c', textwrap.dedent(
            '''\
            import jnius_config
            import json
            import sys
            jnius_config.set_options(*json.load(sys.stdin))
            import jnius
            ManagementFactory = jnius.autoclass("java.lang.management.ManagementFactory")
            json.dump(list(ManagementFactory.getRuntimeMXBean().getInputArguments()), sys.stdout)''')],
            bufsize=-1, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdoutdata, _ = process.communicate(json.dumps(options).encode())
        assert process.wait() == 0
        actual_options = json.loads(stdoutdata.decode())
        assert list(sorted(options)) == list(sorted(actual_options))

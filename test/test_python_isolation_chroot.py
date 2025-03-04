import pytest
from unit.applications.lang.python import TestApplicationPython


class TestPythonIsolation(TestApplicationPython):
    prerequisites = {'modules': {'python': 'any'}}

    def test_python_isolation_chroot(self, is_su, temp_dir):
        if not is_su:
            pytest.skip('requires root')

        isolation = {
            'rootfs': temp_dir,
        }

        self.load('ns_inspect', isolation=isolation)

        assert not (
            self.getjson(url=f'/?path={temp_dir}')['body']['FileExists']
        ), 'temp_dir does not exists in rootfs'

        assert self.getjson(url='/?path=/proc/self')['body'][
            'FileExists'
        ], 'no /proc/self'

        assert not (
            self.getjson(url='/?path=/dev/pts')['body']['FileExists']
        ), 'no /dev/pts'

        assert not (
            self.getjson(url='/?path=/sys/kernel')['body']['FileExists']
        ), 'no /sys/kernel'

        ret = self.getjson(url='/?path=/app/python/ns_inspect')

        assert ret['body']['FileExists'], 'application exists in rootfs'

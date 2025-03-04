import os

import pytest
from unit.applications.lang.go import TestApplicationGo


class TestGoIsolationRootfs(TestApplicationGo):
    prerequisites = {'modules': {'go': 'all'}}

    @pytest.fixture(autouse=True)
    def setup_method_fixture(self, skip_alert):
        skip_alert(r'\[unit\] close\(\d+\) failed: Bad file descriptor')

    def test_go_isolation_rootfs_chroot(self, is_su, temp_dir):
        if not is_su:
            pytest.skip('requires root')

        if os.uname().sysname == 'Darwin':
            pytest.skip('chroot tests not supported on OSX')

        isolation = {
            'rootfs': temp_dir,
        }

        self.load('ns_inspect', isolation=isolation)

        obj = self.getjson(url='/?file=/go/app')['body']

        assert obj['FileExists'], 'app relative to rootfs'

        obj = self.getjson(url='/?file=/bin/sh')['body']
        assert not obj['FileExists'], 'file should not exists'

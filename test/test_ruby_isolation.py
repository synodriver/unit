import pytest
from unit.applications.lang.ruby import TestApplicationRuby
from unit.option import option


class TestRubyIsolation(TestApplicationRuby):
    prerequisites = {'modules': {'ruby': 'any'}, 'features': ['isolation']}

    def test_ruby_isolation_rootfs(self, is_su, temp_dir):
        isolation_features = option.available['features']['isolation'].keys()

        if not is_su:
            if 'unprivileged_userns_clone' not in isolation_features:
                pytest.skip('requires unprivileged userns or root')

            if 'user' not in isolation_features:
                pytest.skip('user namespace is not supported')

            if 'mnt' not in isolation_features:
                pytest.skip('mnt namespace is not supported')

            if 'pid' not in isolation_features:
                pytest.skip('pid namespace is not supported')

        isolation = {'rootfs': temp_dir}

        if not is_su:
            isolation['namespaces'] = {
                'mount': True,
                'credential': True,
                'pid': True,
            }

        self.load('status_int', isolation=isolation)

        assert 'success' in self.conf(
            '"/ruby/status_int/config.ru"',
            'applications/status_int/script',
        )

        assert 'success' in self.conf(
            '"/ruby/status_int"',
            'applications/status_int/working_directory',
        )

        assert self.get()['status'] == 200, 'status int'

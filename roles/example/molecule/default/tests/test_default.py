import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_application_is_installed(host):
    application = host.package("application")

    assert application.is_installed


def test_application_is_running(host):
    application = host.service("application")

    assert application.is_running
    assert application.is_enabled

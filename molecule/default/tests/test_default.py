#!/usr/bin/env python

import os
import stat
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_file_config(host):
    file = host.file("/etc/redis/redis_6379.conf")
    assert file.exists
    assert file.user == 'redis'

def test_redis_listening(host):
    assert host.socket("tcp://0.0.0.0:6379").is_listening
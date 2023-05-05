#!/usr/bin/env python

import os
import stat
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_file_config(host):
    first_file = host.file("/etc/redis/redis_6379.conf")
    second_file = host.file("/etc/redis/redis_6378.conf")
    assert first_file.exists
    assert first_file.user == "redis"
    assert second_file.exists
    assert second_file.user == "redis"


def test_redis_listening(host):
    assert host.socket("tcp://0.0.0.0:6379").is_listening
    assert host.socket("tcp://0.0.0.0:6378").is_listening

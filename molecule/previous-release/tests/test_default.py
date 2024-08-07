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
    assert file.user == "redis"


def test_redis_listening(host):
    assert host.socket("tcp://0.0.0.0:6379").is_listening


def test_redis_service(host):
    redis_service = host.service("redis-server@6379")
    assert redis_service.is_enabled
    assert redis_service.is_running


def test_redis_cli(host):
    config = host.check_output("redis-cli -p 6379 config get loglevel")
    version = host.check_output("redis-cli -p 6379 info server")
    assert "notice" in config
    assert ("redis_version:7.0" in version) or ("redis_version:6.2" in version)

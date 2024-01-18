#!/usr/bin/env python

import os
import stat
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_file_config(host):
    file_6379 = host.file("/etc/redis/redis_6379.conf")
    file_6378 = host.file("/etc/redis/redis_6378.conf")
    assert file_6379.exists
    assert file_6379.user == "redis"
    assert file_6378.exists
    assert file_6378.user == "redis"


def test_redis_listening(host):
    assert host.socket("tcp://0.0.0.0:6379").is_listening
    assert host.socket("tcp://0.0.0.0:6378").is_listening


def test_redis_service(host):
    redis_service_6379 = host.service('redis-server@6379')
    redis_service_6378 = host.service('redis-server@6378')
    assert redis_service_6379.is_enabled
    assert redis_service_6379.is_running
    assert redis_service_6378.is_enabled
    assert redis_service_6378.is_running


def test_redis_cli(host):
    config_6379 = host.check_output("redis-cli -p 6379 config get loglevel")
    config_6378 = host.check_output("redis-cli -p 6378 config get loglevel")
    assert "notice" in config_6379
    assert "notice" in config_6378

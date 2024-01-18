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


def test_redis_service(host):
    redis_service_1 = host.service('redis-server@6379')
    redis_service_2 = host.service('redis-server@6378')
    assert redis_service_1.is_enabled
    assert redis_service_1.is_running
    assert redis_service_2.is_enabled
    assert redis_service_2.is_running


def test_redis_cli(host):
    config_1 = host.check_output("redis-cli -p 6379 config get loglevel")
    config_2 = host.check_output("redis-cli -p 6379 config get loglevel")
    assert "notice" in config_1
    assert "notice" in config_2

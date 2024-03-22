#!/usr/bin/env python

import os
import stat
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_file_config(host):
    file_redis = host.file("/etc/redis/redis_6379.conf")
    file_sentinel = host.file("/etc/redis/sentinel_26379.conf")
    assert file_redis.exists
    assert file_redis.user == "redis"
    assert file_sentinel.exists
    assert file_sentinel.user == "redis"


def test_service_listening(host):
    assert host.socket("tcp://0.0.0.0:6379").is_listening
    assert host.socket("tcp://0.0.0.0:26379").is_listening


def test_redis_service(host):
    redis_service = host.service('redis-server@6379')
    sentinel_service = host.service('redis-sentinel@26379')
    assert redis_service.is_enabled
    assert redis_service.is_running
    assert sentinel_service.is_enabled
    assert sentinel_service.is_running


def test_redis_cli(host):
    config = host.check_output("redis-cli -p 6379 config get loglevel")
    assert "notice" in config


def test_redis_sentinel(host):
    sentinel_status = host.check_output(
        "redis-cli -p 26379 info sentinel | grep master0 | cut -d ':' -f2 | cut -d ',' -f2 | cut -d '=' -f2"
    )
    assert sentinel_status == "ok"

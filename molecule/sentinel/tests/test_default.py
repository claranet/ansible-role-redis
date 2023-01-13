#!/usr/bin/env python

import os
import stat
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_service_listening(host):
    # assert host.socket("tcp://0.0.0.0:26379").is_listening
    assert host.socket("tcp://0.0.0.0:6379").is_listening


def test_redis_sentinel(host):
    sentinel_status = host.check_output(
        "redis-cli -p 26379 info sentinel | grep master0 | cut -d ':' -f2 | cut -d ',' -f2 | cut -d '=' -f2"
    )
    assert sentinel_status == "ok"

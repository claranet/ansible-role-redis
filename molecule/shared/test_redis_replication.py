def is_master(host):
    all_variables = host.ansible.get_variables()
    if all_variables["redis_role"] == "master":
        return True
    return False


def test_redis_replication_with_get_infos(host):
    role = host.check_output("redis-cli -p 6379 role | head -n 1")

    if is_master(host=host):
        number_of_slaves = host.check_output(
            "redis-cli -p 6379 info replication | grep connected_slaves | cut -d ':' -f2"
        )
        assert role == "master"
        assert int(number_of_slaves) == 2

    else:
        master_status = host.check_output(
            "redis-cli -p 6379 info replication | grep master_link_status | cut -d ':' -f2"
        )
        assert master_status == "up"
        assert role == "slave"


def test_redis_replication_with_read_and_write(host):
    if is_master(host=host):
        write_command = host.check_output(
            "redis-cli -p 6379 set data test"
        )
        assert write_command == "OK"
    
    data = host.check_output(
            "redis-cli -p 6379 get data"
        )
    assert data == "test"

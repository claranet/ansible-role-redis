# Ansible role - redis
[![Maintainer](https://img.shields.io/badge/maintained%20by-claranet-e00000?style=flat-square)](https://www.claranet.fr/)
[![License](https://img.shields.io/github/license/claranet/ansible-role-redis?style=flat-square)](LICENSE)
[![Release](https://img.shields.io/github/v/release/claranet/ansible-role-redis?style=flat-square)](https://github.com/claranet/ansible-role-redis/releases)
[![Status](https://img.shields.io/github/actions/workflow/status/claranet/ansible-role-redis/molecule.yml?style=flat-square&label=tests&branch=main)](https://github.com/claranet/ansible-role-redis/actions?query=workflow%3A%22Ansible+Molecule%22)
[![Ansible version](https://img.shields.io/badge/ansible-%3E%3D2.10-black.svg?style=flat-square&logo=ansible)](https://github.com/ansible/ansible)
[![Ansible Galaxy](https://img.shields.io/badge/ansible-galaxy-black.svg?style=flat-square&logo=ansible)](https://galaxy.ansible.com/claranet/redis)


> :star: Star us on GitHub — it motivates us a lot!

Install and configure Redis

## :warning: Requirements

Ansible >= 2.10

## :zap: Installation

```bash
ansible-galaxy install claranet.redis
```

## :gear: Role variables

Variable                              | Default value                                      | Description
--------------------------------------|----------------------------------------------------|------------------------------------------------------------------
redis_server_enabled                  | **true**                                           | enable installation and configuration of redis server
redis_master_ip                       | **null**                                           | redis master ip. used for clustering scenario
redis_group                           | **groups.redis**                                   | redis group name in inventory
redis_server_version                  | **latest**                                         | redis version to install
redis_server_user                     | **redis**                                          | redis user for configuration
redis_server_group                    | **redis**                                          | group for redis
redis_server_listen                   | **0.0.0.0**                                        | listen address
redis_server_port                     | **6379**                                           | listen port
redis_server_timeout                  | **0**                                              | server timeout
redis_server_tcp_keepalive            | **300**                                            | server tcp keepalive
redis_server_loglevel                 | **notice**                                         | server log level
redis_server_logdir                   | **/var/log/redis**                                 | path to log directory
redis_server_logfile                  | **redis-server_{{ redis_server_port }}.log**       | name of redis log file 
redis_server_databases_number         | **16**                                             | number of databases
redis_server_databases_dir            | **/var/lib/redis**                                 | path of databases files
redis_server_dbfilename               | **dump.rdb**                                       | database filename
redis_server_replica_readonly         | **yes**                                            | allow replica readonly with yes/no
redis_server_replica_priority         | **100**                                            | set priority to replicas
redis_server_replica_serve_stale_data | **yes**                                            | allow replica server stale data
redis_server_maxclients               | **10000**                                          | maxclients number
redis_server_limitnofile              | **65535**                                          | server limitnofile
redis_server_maxmemory_policy         | **allkeys-lru**                                    | max memory policy
redis_server_maxmemory_samples        | **5**                                              | max memory samples allowed
redis_server_maxmemory                | **'{{ autocalculated | int }}'**                   | max memory available
redis_server_password                 | **null**                                           | redis server password
redis_sentinel_version                | **'{{ redis_server_version }}'**                   | sentinel version to install
redis_sentinel_enabled                | **false**                                          | sentinel version to install
redis_sentinel_daemonize              | **true**                                           | daemonize redis sentinel
redis_sentinel_listen                 | **0.0.0.0**                                        | listen address for sentinel
redis_sentinel_port                   | **26379**                                          | port for listen address
redis_sentinel_logdir                 | **'{{ redis_server_logdir }}'**                    | logdir path for sentinel
redis_sentinel_logfile                | **'redis-sentinel_{{ redis_sentinel_port }}.log'** | sentinel logfile
redis_sentinel_databases_dir          | **'{{ redis_server_databases_dir }}'**             | sentinel database directory
redis_sentinel_quorum                 | **2**                                              | redis sentinel quorum
redis sentinel downafter              | **10000**                                          | time for downafter
redis_sentinel_failover_timeout       | **30000**                                          | failover timeout


## :arrows_counterclockwise: Dependencies

N/A

## :pencil2: Example Playbook


* #### Standalone scenario

```yaml
---
- hosts: all
  vars:
    redis_sentinel_enabled: false
    redis_server_version: 6:7.0.7
  roles:
    - role: claranet.redis
```

* #### Multi-instance scenario

```yaml
---
- name: First instance
  hosts: all
  vars:
    redis_sentinel_enabled: false
    redis_server_version: 6:7.0.7
  roles:
    - role: claranet.redis

- name: Second instance
  hosts: all
  vars:
    redis_sentinel_enabled: false
    redis_server_version: 6:7.0.7
    redis_server_port: 6378
  roles:
    - role: claranet.redis
```

* #### Master slave scenario

**inventory**

```yaml
---
all:
  children:
    redis:
      hosts:
        master:
          redis_role: master
        slave-01:
          redis_role: slave
        slave-02:
          redis_role: slave
```

**playbook**

```yaml
---
- hosts: all
  vars:
    redis_sentinel_enabled: false
    redis_server_version: latest
  roles:
    - role: claranet.redis
```

* #### Sentinel scenario

**inventory**

```yaml
---
all:
  children:
    redis:
      hosts:
        master:
          redis_role: master
        slave-01:
          redis_role: slave
        slave-02:
          redis_role: slave
```

**playbook**

```yaml
---
- hosts: all
  vars:
    redis_sentinel_enabled: true
    redis_server_version: 6:7.0.7
  roles:
    - role: claranet.redis
```

## :closed_lock_with_key: [Hardening](HARDENING.md)

## :heart_eyes_cat: [Contributing](CONTRIBUTING.md)

## :copyright: [License](LICENSE)

[Mozilla Public License Version 2.0](https://www.mozilla.org/en-US/MPL/2.0/)

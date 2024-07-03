---
categories:
- 技术
- 虚拟化&云计算
date: '2019-07-29 13:53:03+08:00'
tags:
- openStack
thumbnailImage: //www.azheimage.top/markdown-img-paste-20181113164516536.png
title: 15-openstack故障
---
OpenStack故障
<!--more-->


### 1. OpenStack集群中mariadb集群容器启动失败
用kolla部署的带有高可用的openstack环境中，服务器断电之后，mariadb启动失败问题解决：
1. ssh到无法启动mariadb容器的控制节点，停止mariadb容器。
docker stop mariadb.
2. 备份mariadb的配置文件。
cp /etc/kolla/mariadb/config.json /etc/kolla/mariadb/config.json.bck
3. 将mariadb容器启动的命令修改成sleep 3600
vim /etc/kolla/mariadb/config.json,将“command”:"/usr/bin/mysqld_safe"改为“command”：“sleep 3600”
4. 启动mariadb容器。
docker start mariadb
5. 进入mariadb容器。
docker exec -it mariadb bash
6. 执行mysqld_safe,查看日志
验证是否出现Found 1 prepared transactions! It means that mysqld was not shut down properly last time and critical recovery information (last binlog or tc.log file)
was manually deleted after a crash.You have to start mysqld with --tc-heuristic-recover switch to commit or rollback pending transactions的错误。
7. 执行回滚
mysqld_safe --tc-heuristic-revocer rollback.
8. 若第7步回滚失败，执行
rm -rf /var/lib/mysql/galera.cache
rm -rf /var/lib/mysql/grastate.dat
mysqld_safe --wsrep-new-cluster
9. 数据库回滚完成后，将/etc/kolla/mariadb/config.json恢复为原来配置，重启docker，问题解决！


### 2. 预检查报错
`kolla-ansible -i add-compute prechecks`
>[nova : Checking that libvirt is not running]

libvirt 已经启动，把libvurt关闭，然后再执行检查
service libvirtd stop

### 3. OpenStack重启有问题
kolla-ansible -i add-compute deploy
#### 问题1：
>fatal: [dataocean-d-030019]: FAILED! => {"changed": true, "msg": "'Traceback (most recent call last):\\n  File \"/tmp/ansible_kolla_docker_payload_GOiF32/__main__.py\", line 909, in main\\n    result = bool(getattr(dw, module.params.get(\\'action\\'))())\\n  File \"/tmp/ansible_kolla_docker_payload_GOiF32/__main__.py\", line 679, in recreate_or_restart_container\\n    self.start_container()\\n  File \"/tmp/ansible_kolla_docker_payload_GOiF32/__main__.py\", line 692, in start_container\\n    self.pull_image()\\n  File \"/tmp/ansible_kolla_docker_payload_GOiF32/__main__.py\", line 532, in pull_image\\n    repository=image, tag=tag, stream=True\\n  File \"/usr/lib/python2.7/site-packages/docker/api/image.py\", line 414, in pull\\n    self._raise_for_status(response)\\n  File \"/usr/lib/python2.7/site-packages/docker/api/client.py\", line 263, in _raise_for_status\\n    raise create_api_error_from_http_exception(e)\\n  File \"/usr/lib/python2.7/site-packages/docker/errors.py\", line 31, in create_api_error_from_http_exception\\n    raise cls(e, response=response, explanation=explanation)\\nAPIError: 500 Server Error: Internal Server Error (\"Get https://10.57.30.16:4000/v1/_ping: http: error connecting to proxy http://10.57.22.8:3128/: dial tcp 10.57.22.8:3128: i/o timeout\")\\n'"}

问题原因是代理不通，删除docker代理
rm -rf /etc/systemd/system/docker.service.d/http-proxy.conf
#### 问题2：
>fatal: [dataocean-d-030018]: FAILED! => {"changed": true, "msg": "'Traceback (most recent call last):\\n  File \"/tmp/ansible_kolla_docker_payload_eefO8O/__main__.py\", line 909, in main\\n    result = bool(getattr(dw, module.params.get(\\'action\\'))())\\n  File \"/tmp/ansible_kolla_docker_payload_eefO8O/__main__.py\", line 679, in recreate_or_restart_container\\n    self.start_container()\\n  File \"/tmp/ansible_kolla_docker_payload_eefO8O/__main__.py\", line 692, in start_container\\n    self.pull_image()\\n  File \"/tmp/ansible_kolla_docker_payload_eefO8O/__main__.py\", line 532, in pull_image\\n    repository=image, tag=tag, stream=True\\n  File \"/usr/lib/python2.7/site-packages/docker/api/image.py\", line 414, in pull\\n    self._raise_for_status(response)\\n  File \"/usr/lib/python2.7/site-packages/docker/api/client.py\", line 263, in _raise_for_status\\n    raise create_api_error_from_http_exception(e)\\n  File \"/usr/lib/python2.7/site-packages/docker/errors.py\", line 31, in create_api_error_from_http_exception\\n    raise cls(e, response=response, explanation=explanation)\\nAPIError: 500 Server Error: Internal Server Error (\"Get https://10.57.30.16:4000/v1/_ping: http: server gave HTTP response to HTTPS client\")\\n'"}

问题原因是docker私有仓库连接配置错误
vim /etc/docker/daemon.json
{
 "insecure-registries":["10.57.30.15:4000"]
}
修改为
cat /etc/docker/daemon.json
{
 "insecure-registries":["10.57.30.16:4000"]
}

#### 问题3：
实例一直卡在重启状态，该实例做不了其他操作
>![](https://www.azheimage.top/markdown-img-paste-2019101616221118.png)

1. 进入nova容器
2. source 环境变量
3. nova list查看实例列表
```
+--------------------------------------+--------------+---------+------------+-------------+---------------------+
| ID                                   | Name         | Status  | Task State | Power State | Networks            |
+--------------------------------------+--------------+---------+------------+-------------+---------------------+
| c3f301de-0e6d-4b84-80bf-c7d8fdebe7f8 | cdh-01       | SHUTOFF | -          | Shutdown    | vlan_26=10.57.26.13 |
| 2d5cd48b-8ac1-4898-8652-f255928c5b78 | cdh-02       | SHUTOFF | -          | Shutdown    | vlan_26=10.57.26.26 |
| 9cdc5ab5-a6a3-4426-815f-de7c534f2eb8 | cdh-03       | SHUTOFF | -          | Shutdown    | vlan_26=10.57.26.29 |
| acc4b887-cb6d-4a5e-997e-434537e353d4 | cdh-04       | SHUTOFF | -          | Shutdown    | vlan_26=10.57.26.17 |
| cc6dec1e-d70c-42d0-90dd-3da0964dfd8f | cirros_1     | SHUTOFF | -          | Shutdown    | vlan_26=10.57.26.14 |
| 1d217483-35d7-43f7-8c17-a0e70d533f5d | databi-01    | SHUTOFF | -          | Shutdown    | vlan_26=10.57.26.10 |
| db36a334-987a-484b-a853-03bea189a449 | databi-02    | SHUTOFF | -          | Shutdown    | vlan_26=10.57.26.39 |
| 6b93ad22-ef9a-45e6-8b16-b1daeda4a35f | databi-03    | SHUTOFF | -          | Shutdown    | vlan_26=10.57.26.40 |
| e83e2923-c2cf-49f6-9f8b-379ec7fb8cc1 | dataocean_01 | ACTIVE  | -          | Running     | vlan_26=10.57.26.5  |
| 78c45430-a49f-4383-b8fd-e83910387000 | dataocean_02 | REBOOT  | rebooting  | Running     | vlan_26=10.57.26.9  |
| ed318929-d1bf-4f0e-8bb9-c85c66a27123 | suse-01      | SHUTOFF | -          | Shutdown    | vlan_26=10.57.26.19 |
| d69650f5-d40c-4cc0-84e4-d2b174f18237 | windows_1    | SHUTOFF | -          | Shutdown    | vlan_26=10.57.26.4  |
| c2f3aca9-a05c-48f5-aa4a-6c65e186156c | yinlian      | SHUTOFF | -          | Shutdown    | vlan_26=10.57.26.20 |
+--------------------------------------+--------------+---------+------------+-------------+---------------------+
```
4. 执行重启nova reboot 78c45430-a49f-4383-b8fd-e83910387000
Cannot 'stop' instance 78c45430-a49f-4383-b8fd-e83910387000 while it is in task_state rebooting (HTTP 409) (Request-ID: req-ad8a13e5-f895-4f79-9d82-0fd988553cf6)
5. 执行硬重启，问题解决，机器启动了
nova reboot --hard 78c45430-a49f-4383-b8fd-e83910387000
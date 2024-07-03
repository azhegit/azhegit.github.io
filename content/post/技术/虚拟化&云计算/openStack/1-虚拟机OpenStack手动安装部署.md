---
categories:
- 技术
- 虚拟化&云计算
date: '2019-06-05 13:53:04+08:00'
tags:
- openStack
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725100954649.png
title: 1-虚拟机OpenStack手动安装部署
---
在虚拟中部署OpenStack
<!--more-->

## 虚拟机手动部署
### 环境准备
查看selinux状态
`[root@tdh19 ~]# sestatus -v`
>SELinux status:                 disabled

如果enabled即为开启状态，需要关闭selinux，下面的命令是需要重启生效
`sed -i s#SELINUX=enforcing#SELINUX=disabled# /etc/selinux/config`
立即生效通过执行命令：`setenforce 0`

查看防火墙状态
`systemctl status firewalld.service`

如果需要关闭防火墙
启动： `systemctl start firewalld`
关闭： `systemctl stop firewalld`
查看状态： `systemctl status firewalld`
开机禁用  ： `systemctl disable firewalld`
开机启用  ： `systemctl enable firewalld`

### 部署
#### 1.安装Openstack包
```bash
yum install centos-release-openstack-ocata
yum install https://rdoproject.org/repos/rdo-release.rpm
yum install python-openstackclient
yum install openstack-selinux
```

#### 2.SQL DB
`yum install mariadb mariadb-server python2-PyMySQL`

`vim etc/my.cnf.d/openstack.cnf`
```ini
[mysqld]
default-storage-engine = innodb
innodb_file_per_table
collation-server = utf8_general_ci
init-connect = 'SET NAMES utf8'
character-set-server = utf8
```

```bash
systemctl enable mariadb.service
systemctl start mariadb.service
mysql_secure_installation
```
密码 jkl，一路 y 回车


#### 3.Message Queue
```bash
yum install rabbitmq-server
systemctl enable rabbitmq-server.service
systemctl start rabbitmq-server.service
#添加用户及密码
rabbitmqctl add_user openstack openstack
#允许配置、写、读访问 openstack                     
rabbitmqctl set_permissions openstack ".*" ".*" ".*"
#查看支持的插件
rabbitmq-plugins list                                 
.........
[ ] rabbitmq_management 3.6.2
#使用此插件实现 web 管理
.........
#启动插件
rabbitmq-plugins enable rabbitmq_management 
    The following plugins have been enabled:
    mochiweb
    webmachine
    rabbitmq_web_dispatch
    amqp_client
    rabbitmq_management_agent
    rabbitmq_management
    Plugin configuration has changed. Restart RabbitMQ for changes to take effect.
systemctl restart rabbitmq-server.service

lsof -i:15672
```

访问RabbitMQ,访问地址是http://10.57.244.174:15672/
默认用户名密码都是guest，浏览器添加openstack用户到组并登陆测试，连不上情况一般是防火墙没有关闭所致！

![](https://www.azheimage.top/markdown-img-paste-20190521133408913.png)
![](https://www.azheimage.top/markdown-img-paste-20190521133723754.png)

#### 4.安装Memcached
```bash
yum -y install memcached python-memcached
/etc/sysconfig/memcached
systemctl enable memcached.service
systemctl start memcached.service
```

#### 5.keystone设置
```sql
mysql -u root -pjkl
drop database keystone;

CREATE DATABASE keystone;
GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' IDENTIFIED BY 'keystone';
GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' IDENTIFIED BY 'keystone';
 CREATE DATABASE glance;
GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'localhost' IDENTIFIED BY 'glance';
GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' IDENTIFIED BY 'glance';
CREATE DATABASE nova;
GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'localhost' IDENTIFIED BY 'nova';
GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'%' IDENTIFIED BY 'nova';
CREATE DATABASE nova_api;
GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'localhost' IDENTIFIED BY 'nova';
GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'%' IDENTIFIED BY 'nova';
CREATE DATABASE nova_cell0
GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'localhost' IDENTIFIED BY 'nova';
GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'%' IDENTIFIED BY 'nova';
CREATE DATABASE neutron;
GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'localhost' IDENTIFIED BY 'neutron';
GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'%' IDENTIFIED BY 'neutron';
CREATE DATABASE cinder;
GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'localhost' IDENTIFIED BY 'cinder';
GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'%' IDENTIFIED BY 'cinder';
flush privileges;
show databases;
+--------------------+
| Database           |
+--------------------+
| cinder             |
| glance             |
| information_schema |
| keystone           |
| mysql              |
| neutron            |
| nova               |
| performance_schema |
+--------------------+
8 rows in set (0.000 sec)
```

#### 6. 安装keystone
1. yum安装
```bash
yum -y install openstack-keystone httpd mod_wsgi
openssl rand -hex 10
>a188ab27240714029cec

123456789

vim /etc/keystone/keystone.conf
```
```ini
[DEFAULT]
 #设置 token，和上面产生的随机数值一致
admin_token = 84940c8359e90532abfd  
verbose = true
[database]
connection = mysql+pymysql://keystone:keystone@10.57.244.174/keystone
[memcache]
servers = 10.57.244.174:11211
[revoke]
driver = sql
[token]
provider = uuid
driver = memcache
```
2. 创建数据库表， 使用命令同步
[root@linux-node1 ~]# su -s /bin/sh -c "keystone-manage db_sync" keystone
No handlers could be found for logger "oslo_config.cfg"                                          #出现这个信息，不影响后续操作！忽略~
tailf /var/log/keystone/keystone.log
mysql -u keystone -pkeystone

3. 创建 keystone 用户
```bash
#创建 keystone 用户
keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
keystone-manage credential_setup --keystone-user keystone --keystone-group keystone
keystone-manage bootstrap --bootstrap-password admin \
   --bootstrap-admin-url http://10.57.244.174:35357/v3/ \
   --bootstrap-internal-url http://10.57.244.174:5000/v3/ \
   --bootstrap-public-url http://10.57.244.174:5000/v3/ \
   --bootstrap-region-id RegionOne
ln -s /usr/share/keystone/wsgi-keystone.conf /etc/httpd/conf.d/
systemctl enable httpd
systemctl start httpd
```
4. 创建域/项目/用户和角色
```bash
#加载环境变量
export OS_TOKEN=84940c8359e90532abfd  
export OS_URL=http://10.57.244.174:35357/v3
export OS_IDENTITY_API_VERSION=3

openstack project create --domain default --description "Admin Project" admin

keystone-manage bootstrap --bootstrap-password admin \
  --bootstrap-admin-url http://10.57.244.174:35357/v3/ \
  --bootstrap-internal-url http://10.57.244.174:5000/v3/ \
  --bootstrap-public-url http://10.57.244.174:5000/v3/ \
  --bootstrap-region-id RegionOne

echo "
export OS_TOKEN=123456789
export OS_USERNAME=admin
export OS_PASSWORD=keystone
export OS_AUTH_URL=http://10.57.244.174:35357/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2
">./admin-openstack.sh

source ./admin-openstack.sh

openstack token issue
openstack project create --domain default --description "Service Project" service

openstack project create --domain default --description "Admin Project" admin


yum -y autoremove openstack-keystone

yum -y install openstack-keystone


fc55025e5a6ab82d333d

history
62  keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
63  keystone-manage bootstrap --bootstrap-password admin   --bootstrap-admin-url http://10.57.244.174:35357/v3/   --bootstrap-internal-url http://10.57.244.174:5000/v3/   --bootstrap-public-url http://10.57.244.174:5000/v3/   --bootstrap-region-id RegionOne
64  vim admin-openstack.sh
65  source ./admin-openstack.sh
66  openstack token issue
67  openstack project create --domain default --description "Service Project" service
68  openstack user create --domain default --password=glance glance
69   openstack user list
70  openstack project create --domain default --description "Admin Project" admin
71   openstack user list
72  openstack user create --domain default --password-prompt admin
73  openstack role create admin
74  openstack role add --project admin --user admin admin
75  openstack project create --domain default --description "Demo Project" demo
76  openstack user create --domain default --password=demo demo
77  openstack role create user
78  openstack role add --project demo --user demo user
79  openstack project create --domain default --description "Service Project" service
80   openstack user list
81  openstack project list
82  openstack service create --name keystone --description "OpenStack Identity" identity
83  openstack endpoint create --region RegionOne identity public http://10.57.244.174:5000/v2.0
84   openstack endpoint list
```

#### 7. 安装glance
```bash
yum install openstack-glance
vim /etc/glance/glance-api.conf
```
```ini
[database]
connection = mysql+pymysql://glance:glance@10.57.244.174/glance
[glance_store]
filesystem_store_datadir=/var/lib/glance/images/
[keystone_authtoken]
auth_uri = http://10.57.244.174:5000
auth_url = http://10.57.244.174:35357
auth_plugin = password
project_domain_id = default
user_domain_id = default
project_name = service
username = glance
password = glance
[paste_deploy]
flavor=keystone
```
vim /etc/glance/glance-registry.conf
```ini
[database]
connection = mysql+pymysql://glance:glance@10.57.244.174/glance
[keystone_authtoken]
auth_uri = http://10.57.244.174:5000
auth_url = http://10.57.244.174:35357
auth_plugin = password
project_domain_id = default
user_domain_id = default
project_name = service
username = glance
password = glance
[paste_deploy]
flavor=keystone
```
`cat /etc/glance/glance-registry.conf|grep -v "^#"|grep -v "^$"`
`cat /etc/glance/glance-api.conf|grep -v "^#"|grep -v "^$"`

```bash
su -s /bin/sh -c "glance-manage db_sync" glance

#在 keystone 上注册
openstack user create --domain default --password-prompt glance glance
openstack role add --project service --user glance admin
openstack service create --name glance --description "OpenStack Image" image
openstack endpoint create --region RegionOne image public http://10.57.244.174:9292
openstack endpoint create --region RegionOne image internal http://10.57.244.174:9292
openstack endpoint create --region RegionOne image admin http://10.57.244.174:9292
systemctl enable openstack-glance-api.service openstack-glance-registry.service
systemctl start openstack-glance-api.service openstack-glance-registry.service

#验证
wget http://download.cirros-cloud.net/0.3.5/cirros-0.3.5-x86_64-disk.img
openstack image create "cirros" \
  --file cirros-0.3.5-x86_64-disk.img \
  --disk-format qcow2 --container-format bare \
  --public
openstack image list
openstack image delete "cirros"
ll /var/lib/glance/images/
```
>下载ios格式镜像，需要用OZ工具制造openstack镜像，具体操作请见另一篇博客：
实际生产环境下，肯定要使用ios镜像进行制作了
http://www.cnblogs.com/kevingrace/p/5821823.html
或者直接下载centos的qcow2格式镜像进行上传，qcow2格式镜像直接就可以在openstack里使用，不需要进行格式转换！
下载地址：http://cloud.centos.org/centos，可以到里面下载centos5/6/7的qcow2格式的镜像

4、启动 glance
systemctl enable openstack-glance-api
systemctl enable openstack-glance-registry
systemctl start openstack-glance-api
systemctl start openstack-glance-registry
netstat -lnutp |grep 9191 #registry
>tcp 0 0 0.0.0.0:9191 0.0.0.0:* LISTEN 24890/python2

netstat -lnutp |grep 9292 #api
>tcp 0 0 0.0.0.0:9292 0.0.0.0:* LISTEN 24877/python2

#### 8. 安装nova
```bash
openstack user create --domain default --password-prompt nova nova
openstack role add --project service --user nova admin
openstack service create --name nova --description "OpenStack Compute" compute

openstack endpoint create --region RegionOne compute public http://10.57.244.174:8774/v2.1
openstack endpoint create --region RegionOne compute internal http://10.57.244.174:8774/v2.1

openstack user create --domain default --password-prompt placement
openstack role add --project service --user placement admin
openstack service create --name placement --description "Placement API" placement
openstack endpoint create --region RegionOne placement public http://10.57.244.174:8778
openstack endpoint create --region RegionOne placement internal http://10.57.244.174:8778

yum install openstack-nova-api \
  openstack-nova-conductor \
  openstack-nova-console \
  openstack-nova-novncproxy \
  openstack-nova-scheduler \
  openstack-nova-placement-api

vim /etc/nova/nova.conf
```
```ini
[DEFAULT]
rpc_backend=rabbit
my_ip=10.57.244.174
debug=true
allow_resize_to_same_host=True
connection = mysql+pymysql://nova:nova@10.57.244.174/nova
[api_database]
connection = mysql+pymysql://nova:nova@10.57.244.174/nova_api
[cache]
backend = oslo_cache.memcache_pool
enabled = True
memcache_servers = 10.57.244.174:11211

[keystone_authtoken]
auth_uri = http://10.57.244.174:5000
auth_url = http://10.57.244.174:35357
auth_plugin = password
project_domain_id = default
user_domain_id = default
project_name = service
username = nova
password = nova
[libvirt]
virt_type=kvm                                  #如果控制节点也作为计算节点（单机部署的话），这一行也添加上（这行是计算节点配置的）
[neutron]
url = http://10.57.244.174:9696
auth_url = http://10.57.244.174:35357
auth_plugin = password
project_domain_id = default
user_domain_id = default
region_name = RegionOne
project_name = service
username = neutron
password = neutron
service_metadata_proxy = True
metadata_proxy_shared_secret = neutron
lock_path=/var/lib/nova/tmp
[oslo_messaging_rabbit]
rabbit_host=10.57.244.174
rabbit_port=5672
rabbit_userid=openstack
rabbit_password=openstack
[vnc]
novncproxy_base_url=http://10.57.244.174:6080/vnc_auto.html      #如果控制节点也作为计算节点（单机部署的话），这一行也添加上（这行是计算节点配置的），配置控制节点的公网ip
vncserver_listen= $my_ip
vncserver_proxyclient_address= $my_ip
keymap=en-us           #如果控制节点也作为计算节点（单机部署的话），这一行也添加上（这行是计算节点配置的）
```
```bash
su -s /bin/sh -c "nova-manage api_db sync" nova
su -s /bin/sh -c "nova-manage cell_v2 map_cell0" nova
su -s /bin/sh -c "nova-manage cell_v2 create_cell --name=cell1 --verbose" nova
su -s /bin/sh -c "nova-manage db sync" nova
nova-manage cell_v2 list_cells

systemctl enable openstack-nova-api.service \
  openstack-nova-consoleauth.service openstack-nova-scheduler.service \
  openstack-nova-conductor.service openstack-nova-novncproxy.service

systemctl start openstack-nova-api.service \
  openstack-nova-consoleauth.service openstack-nova-scheduler.service \
  openstack-nova-conductor.service openstack-nova-novncproxy.service

openstack hypervisor list

su -s /bin/sh -c "nova-manage cell_v2 discover_hosts --verbose" nova # 这一步也也可在nova.conf中配置 discover_hosts_in_cells_interval 自动发信compute node
yum install openstack-nova-compute

systemctl enable libvirtd.service openstack-nova-compute.service

systemctl start libvirtd.service openstack-nova-compute.service

openstack compute service list # 应该有四个服务时up的(conductor, consoleauth, scheduler, compute)
openstack catalog list # 应该有4中类型的endpoint(compute,placement, image, identity)

### 网络服务（neutron）
openstack user create --domain default --password-prompt neutron
openstack service create --name neutron --description "OpenStack Networking" network

openstack endpoint create --region RegionOne network public http://10.57.244.174:9696
openstack endpoint create --region RegionOne network internal http://10.57.244.174:9696
openstack endpoint create --region RegionOne network admin http://10.57.244.174:9696

yum install openstack-neutron openstack-neutron-ml2 openstack-neutron-linuxbridge python-neutronclient ebtables ipset
vim /etc/neutron/neutron.conf
```
```ini
[DEFAULT]
state_path = /var/lib/neutron
core_plugin = ml2
auth_strategy = keystone
nova_url = http://10.57.244.174:8774/v2
rpc_backend=rabbit
[keystone_authtoken]
auth_uri = http://10.57.244.174:5000
auth_url = http://10.57.244.174:35357
auth_plugin = password
project_domain_id = default
user_domain_id = default
project_name = service
username = neutron
password = neutron
memcached_servers = 10.57.244.174:11211
[database]
connection = mysql+pymysql://neutron:neutron@10.57.244.174/neutron
[nova]
auth_url = http://10.57.244.174:35357
auth_plugin = password
project_domain_id = default
user_domain_id = default
region_name = RegionOne
project_name = service
username = nova
password = nova
[oslo_concurrency]
lock_path = /var/lib/neutron/tmp
[oslo_messaging_rabbit]
rabbit_host = 10.57.244.174
rabbit_port = 5672
rabbit_userid = openstack
rabbit_password = openstack
```
vim /etc/neutron/plugins/ml2/ml2_conf.ini
```ini
[ml2]
type_drivers = flat,vlan,gre,vxlan,geneve
tenant_network_types = vlan,gre,vxlan,geneve
mechanism_drivers = openvswitch,linuxbridge
extension_drivers = port_security
[ml2_type_flat]
flat_networks = physnet1
[ml2_type_vlan]
[ml2_type_gre]
[ml2_type_vxlan]
[ml2_type_geneve]
[securitygroup]
enable_ipset = True
```

vim /etc/neutron/plugins/ml2/linuxbridge_agent.ini
```ini
[linux_bridge]
physical_interface_mappings = physnet1:enp0s3
[vxlan]
enable_vxlan = false
[agent]
prevent_arp_spoofing = True
[securitygroup]
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver
enable_security_group = True
```
vim /etc/neutron/dhcp_agent.ini
```ini
interface_driver = neutron.agent.linux.interface.BridgeInterfaceDriver
dhcp_driver = neutron.agent.linux.dhcp.Dnsmasq
enable_isolated_metadata = true
```
```bash
ln -s /etc/neutron/plugins/ml2/ml2_conf.ini /etc/neutron/plugin.ini
openstack user create --domain default --password=neutron neutron
openstack role add --project service --user neutron admin

su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head" neutron

systemctl restart openstack-nova-api.service

systemctl enable neutron-server.service \
  neutron-linuxbridge-agent.service neutron-dhcp-agent.service \
  neutron-metadata-agent.service
systemctl start neutron-server.service \
  neutron-linuxbridge-agent.service neutron-dhcp-agent.service \
  neutron-metadata-agent.service
#option 2 网络才执行下
systemctl enable neutron-l3-agent.service
systemctl start neutron-l3-agent.service

systemctl restart openstack-nova-compute.service
systemctl enable neutron-linuxbridge-agent.service
systemctl start neutron-linuxbridge-agent.service


openstack extension list --network

 Option 1: Provider networks

openstack network agent list
```

#### 9. 安装WEB
```bash
yum -y install openstack-dashboard
vim /etc/openstack-dashboard/local_settings
```
```ini
OPENSTACK_HOST = "127.0.0.1"                                 #更改为keystone机器地址
OPENSTACK_KEYSTONE_DEFAULT_ROLE = "user"              #默认的角色
ALLOWED_HOSTS = ['*']                                                 #允许所有主机访问
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '10.57.244.174:11211',
    },
}
TIME_ZONE = "Asia/Shanghai"                        #设置时区
```
systemctl restart httpd


### 错误
[root@localhost ~]#   source ./admin-openstack.sh
[root@localhost ~]# openstack project create --domain default --description "Admin Project" admin
The request you have made requires authentication. (HTTP 401) (Request-ID: req-723d9e6f-fddd-40bc-a7f0-222b46beb2e5)

tailf /var/log/keystone/keystone.log
>2019-05-21 18:00:45.816 21702 WARNING keystone.auth.plugins.core [req-723d9e6f-fddd-40bc-a7f0-222b46beb2e5 - - - - -] Could not find domain: default.: DomainNotFound: Could not find domain: default.
2019-05-21 18:00:45.819 21702 WARNING keystone.server.flask.application [req-723d9e6f-fddd-40bc-a7f0-222b46beb2e5 - - - - -] Authorization failed. The request you have made requires authentication. from 10.57.244.174: Unauthorized: The request you have made requires authentication


echo "
export OS_PROJECT_DOMAIN_NAME=default
export OS_USER_DOMAIN_NAME=default 
export OS_PROJECT_NAME=admin 
export OS_USERNAME=admin
export OS_PASSWORD=admin
export OS_AUTH_URL=http://10.57.244.174:35357/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2
">./admin-openstack.sh



yum安装dashboard的时候
错误：软件包：python-django-1.8.14-1.el7.noarch (centos-openstack-ocata)
          需要：python-django-bash-completion = 1.8.14-1.el7
          可用: python-django-bash-completion-1.8.14-1.el7.noarch (centos-openstack-ocata)
              python-django-bash-completion = 1.8.14-1.el7
          正在安装: python-django-bash-completion-1.11.20-1.el7.noarch (openstack-stein)
              python-django-bash-completion = 1.11.20-1.el7
 您可以尝试添加 --skip-broken 选项来解决该问题
 您可以尝试执行：rpm -Va --nofiles --nodigest

删除openstack-stein的yum源


Target WSGI script '/usr/bin/keystone-wsgi-public' cannot be loaded as Python module.




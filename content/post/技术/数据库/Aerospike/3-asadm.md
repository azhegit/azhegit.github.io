---
categories:
- 技术
- 数据库
date: '2021-09-28 12:15:25+08:00'
tags:
- Aerospike
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725102054110.png
title: 3-asadm
---
管理工具

1. 创建索引

2. 删除索引

<!--more-->

查看配置信息： show config


Aerospike Admin
  - enable:
    Enters privileged mode, which allows a you to issue manage
    and asinfo commands.
      Options:
        --warn:    Use this option to receive a prompt to confirm
                   that you want to run the command.
  - exit:
    Terminate session
  - help:
    Displays the documentation for the specified command.
    For example, to see the documentation for the 'info' command,
    use the command 'help info'.
  - watch:
    Runs a command for a specified pause and iterations.
    Usage: watch [pause] [iterations] [--no-diff] command
       pause:      The duration between executions.
                   [default: 2 seconds]
       iterations: Number of iterations to execute command.
                   [default: until keyboard interrupt]
      Options:
       --no-diff:  Do not highlight differences
    Example 1: Show 'info network' 3 times and pause for 1 second each time.
               watch 1 3 info network
    Example 2: Show "info namespace" with 5 seconds pause until
               interrupted
               watch 5 info namespace
  - summary:
    Displays summary of Aerospike cluster.
      Options:
        -l                        - Enable to display namespace output in List view. Default: Table view
        --enable-ssh              - Enables the collection of system statistics from a remote server.
        --ssh-user   <string>     - Default user ID for remote servers. This is the ID of a user of the
                                    system, not the ID of an Aerospike user.
        --ssh-pwd    <string>     - Default password or passphrase for key for remote servers. This is the
                                    user's password for logging into the system, not a password for logging
                                    into Aerospike.
        --ssh-port   <int>        - Default SSH port for remote servers. Default: 22
        --ssh-key    <string>     - Default SSH key (file path) for remote servers.
        --ssh-cf     <string>     - Remote System Credentials file path.
                                    If the server credentials are not in the credentials file, then
                                    authentication is attempted with the default credentials.
                                    File format : each line should contain <IP[:PORT]>,<USER_ID>,
                                    <PASSWORD or PASSPHRASE>,<SSH_KEY>
                                    Example:  1.2.3.4,uid,pwd
                                              1.2.3.4:3232,uid,pwd
                                              1.2.3.4:3232,uid,,key_path
                                              1.2.3.4:3232,uid,passphrase,key_path
                                              [2001::1234:10],uid,pwd
                                              [2001::1234:10]:3232,uid,,key_path
    Modifiers: with
  - features:
    Lists the features in use in a running Aerospike cluster.
    Modifiers: like, with
  - pager:
    Set pager for output
      - off:
        Removes pager and prints output normally
      - on:
        Displays output with vertical and horizontal paging for each output table same as linux 'less'
        command.
        Use arrow keys to scroll output and 'q' to end page for table.
        All linux less commands can work in this pager option.
      - scroll:
        Display output in scrolling mode
  - collectinfo:
    "collectinfo" is used to collect cluster info, aerospike conf file and system stats.
    Modifiers: with
    Default: Collects cluster info, aerospike conf file for local node and system stats from all nodes if
    remote server credentials provided. If credentials are not available then it will collect system
    stats from
    local node only.
      Options:
        -n              <int>        - Number of snapshots. Default: 1
        -s              <int>        - Sleep time in seconds between each snapshot. Default: 5 sec
        --enable-ssh                 - Enables the collection of system statistics from the remote server.
        --ssh-user      <string>     - Default user ID for remote servers. This is the ID of a user of the
                                       system not the ID of an Aerospike user.
        --ssh-pwd       <string>     - Default password or passphrase for key for remote servers. This is
                                       the user's password for logging into the system, not a password for
                                       logging into Aerospike.
        --ssh-port      <int>        - Default SSH port for remote servers. Default: 22
        --ssh-key       <string>     - Default SSH key (file path) for remote servers.
        --ssh-cf        <string>     - Remote System Credentials file path.
                                       If the server credentials are not in the credentials file, then
                                       authentication is attempted with the default credentials.
                                       File format : each line must contain <IP[:PORT]>,<USER_ID>
                                       <PASSWORD or PASSPHRASE>,<SSH_KEY>
                                       Example:  1.2.3.4,uid,pwd
                                                 1.2.3.4:3232,uid,pwd
                                                 1.2.3.4:3232,uid,,key_path
                                                 1.2.3.4:3232,uid,passphrase,key_path
                                                 [2001::1234:10],uid,pwd
                                                 [2001::1234:10]:3232,uid,,key_path
        --output-prefix <string>     - Output directory name prefix.
        --asconfig-file <string>     - Aerospike config file path to collect.
                                       Default: /etc/aerospike/aerospike.conf
  - asinfo:
    "asinfo" provides raw access to the info protocol.
      Options:
        -v <command>   - The command to execute
        -p <port>      - Port to use in the case of an XDR info command and XDR is
                         not in asd
        -l             - Replace semicolons ";" with newlines. If output does
                         not contain semicolons "-l" will attempt to use
                         colons ":" followed by commas ",".
        --no_node_name - Force to display output without printing node names.
    Modifiers: like, with
    Default: Executes an info command.
  - manage:
    "manage" is used for administrative tasks like managing users, roles, udf, and sindexes
      - acl:
        "manage acl" is used to manage users and roles.
          - create:
              - user:
                Usage: create user <username> [password <password>] [roles <role1> <role2> ...]
                   username        - Name of the new user.
                   password        - Password for the new user. User will be prompted if no
                                     password is provided.
                   roles           - Roles to be granted to the user.
                                     [default: None]
                Modifiers: password, roles
              - role:
                Usage: create role <role-name> priv <privilege> [ns <namespace> [set <set>]] [allow <addr1> [<addr2> [...]]] [read <read-quota>] [write <write-quota>]
                  role-name     - Name of the new role.
                  priv          - Privilege for the new role. Some privileges are not
                                  limited to a global scope. Scopes are either global, per
                                  namespace, or per namespace and set. For more
                                  information:
                                  https://www.aerospike.com/docs/operations/configure/security/access-control/#privileges-permissions-and-scopes
                                  [default: None]
                  ns            - Namespace scope of privilege.
                                  [default: None]
                  set           - Set scope of privilege. Namespace scope is required.
                                  [default: None]
                  allow         - Addresses of nodes that a role will be allowed to connect
                                  to a cluster from.
                                  [default: None]
                  read          - Quota for read transaction (TPS).
                  write         - Quota for write transaction (TPS).
                Required: priv
                Modifiers: allow, ns, read, set, write
          - delete:
              - user:
                Usage: delete user <username>
                  username           - User to delete.
              - role:
                Usage: delete role <role-name>
                  role-name     - Role to delete.
          - grant:
              - user:
                Usage: grant user <username> roles <role1> [<role2> [...]]
                  username        - User to have roles granted.
                  roles           - Roles to add to the user.
                Required: roles
              - role:
                Usage: grant role <role-name> priv <privilege> [ns <namespace> [set <set>]]>
                  role-name     - Role to have the privilege granted.
                  priv          - Privilege to be added to the role.
                  ns            - Namespace scope of privilege.
                                  [default: None]
                  set           - Set scope of privilege. Namespace scope is required.
                                  [default: None]
                Required: priv
                Modifiers: ns, set
          - revoke:
              - user:
                Usage: revoke user <username> roles <role1> [<role2> [...]]
                  username        - User to have roles revoked.
                  roles           - Roles to delete from the user.
                Required: roles
              - role:
                Usage: revoke role <role-name> priv <privilege> [ns <namespace> [set <set>]]>
                  role-name     - Role to have privilege revoked.
                  priv          - Privilege to delete from the role.
                  ns            - Namespace scope of privilege
                                  [default: None]
                  set           - Set scope of privilege. Namespace scope is required.
                                  [default: None]
                Required: priv
                Modifiers: ns, set
          - set-password:
            Usage: set-password user <username> [password <password>]
              username           - User to have password set.
              password           - Password for the user.  A prompt will appear if no
                                   password is provided.
            Modifiers: password
          - change-password:
            Usage: change-password user <username> [old <old-password>] [new <new-password>]
              username           - User that needs a new password.
              old                - Current password for the user. User will be
                                   prompted if no password is provided.
              new                - New password for the user. User will be prompted
                                   if no password is provided.
            Required: user
            Modifiers: new, old
          - allowlist:
            Usage: allowlist role <role-name> allow <addr1> [<addr2> [...]]
              role-name     - Role that will have the new allowlist.
              allow         - Addresses of nodes that a role will be allowed to connect
                              from. This command erases and re-assigns the allowlist
            Usage: allowlist role <role-name> clear
              role-name     - Role that will have the allowlist cleared.
              clear         - Clears allowlist from the role. Either 'allow' or 'clear' is
                              required.
            Required: role
            Modifiers: allow, clear
          - quotas:
            Usage: quotas role <role-name> [read <read-quota>]|[write <write-quota>]
              role-name     - Role to assign a quota
              read          - Quota for read transaction (TPS). To give a role
                              an unlimited quota enter 0
              write         - Quota for write transaction (TPS).
              Note: A read or write quota is required. Not providing a quota will
                    leave it unchanged.
            Required: role
            Modifiers: read, write
      - udfs:
        "manage udfs" is used to add and remove user defined functions.
          - add:
            Usage: add <module-name> path <module-path>
              module-name   - Name of module to be stored in the server.  Can be different
                              from file in path but must end with an extension.
              path          - Path to the udf module.  Can be either absolute or relative
                              to the current working directory.
            Required: path
          - remove:
            Usage: remove <module-name>
              module-name   - Name of module to remove as stored in the server.
      - sindex:
        "manage sindex" is used to create and delete secondary indexes.
          - create:
            Usage: create <bin-type> <index-name> ns <ns> [set <set>] bin <bin-name> [in <index-type>]
              bin-type    - The bin type of the provided <bin-name>. Should be one of the following values:
                              numeric, string, or geo2dsphere
              index-name    - Name of the secondary index to be created. Should be 20 characters
                              or less and not contain ":" or ";".
              ns            - Name of namespace to create the secondary index on.
              set           - Name of set to create the secondary index on.
              bin           - Name of bin to create secondary index on.
              in            - Specifies how the secondary index is to collect keys:
                              list: Specifies to use the elements of a list as keys.
                              mapkeys: Specifies to use the keys of a map as keys.
                              mapvalues: Specifies to use the values of a map as keys.
                              [default: Specifies to use the contents of a bin as keys.]
            Required: bin, ns
            Modifiers: in, set
          - delete:
            Usage: delete <index-name> ns <ns> [set <set>]
              index-name    - Name of the secondary index to be deleted.
              ns            - Namespace where the sindex resides.
              set           - Set where the sindex resides.
            Required: ns
            Modifiers: set
  - show:
    "show" is used to display Aerospike Statistics configuration.
      - config:
        "show config" is used to display Aerospike configuration settings
        Modifiers: diff, for, like, with
        Default: Displays service, network, and namespace configuration
          Options:
            -r           - Repeat output table title and row header after every <terminal width> columns.
                           [default: False, no repetition]
            -flip        - Flip output table to show Nodes on Y axis and config on X axis.
          - cluster:
            Displays Cluster configuration
          - dc:
            Displays datacenter configuration.
            Replaced by "show config xdr" for server >= 5.0.
          - namespace:
            Displays namespace configuration
          - network:
            Displays network configuration
          - service:
            Displays service configuration
          - xdr:
            Displays XDR configuration
      - statistics:
        "show statistics" is used to display statistics for Aerospike components.
        Modifiers: for, like, with
        Default: Displays bin, set, service, and namespace statistics
          Options:
            -t           - Set to show total column at the end. It contains node wise sum for statistics.
            -r           - Repeat output table title and row header after every <terminal width> columns.
                           [default: False, no repetition]
            -flip        - Flip output table to show Nodes on Y axis and stats on X axis.
          - bins:
            Displays bin statistics
          - dc:
            Displays datacenter statistics.
            Replaced by "show statistics xdr" for server >= 5.0.
          - namespace:
            Displays namespace statistics
          - service:
            Displays service statistics
          - sets:
            Displays set statistics
          - sindex:
            Displays sindex statistics
          - xdr:
            Displays XDR statistics
      - latencies:
        "show latencies" is used to show the server latency histograms
        Modifiers: for, like, with
        Default: Displays latency information for the Aerospike cluster.
          Options:
            -e           - Exponential increment of latency buckets, i.e. 2^0 2^(e) ... 2^(e * i)
                           [default: 3]
            -b           - Number of latency buckets to display.
                           [default: 3]
            -v           - Set to display verbose output of optionally configured histograms.
      - distribution:
        "show distribution" is used to show the distribution of object sizes
        and time to live for node and a namespace.
        Modifiers: for, with
        Default: Shows the distributions of Time to Live and Object Size
          - eviction:
            Shows the distribution of namespace Eviction TTLs for server version 3.7.5 and below
          - object_size:
            Shows the distribution of Object sizes for namespaces
              Options:
                -b               - Force to show byte wise distribution of Object Sizes.
                                   Default is rblock wise distribution in percentage
                -k <buckets>     - Maximum number of buckets to show if -b is set.
                                   It distributes objects in same size k buckets and
                                   displays only buckets that have objects in them.
                                   [default is 5].
          - time_to_live:
            Shows the distribution of TTLs for namespaces
      - mapping:
        "show mapping" is used to display Aerospike mapping from IP to Node_id and Node_id to IPs
        Modifiers: like
        Default: Displays mapping IPs to Node_id and Node_id to IPs
          - ip:
            Displays IP to Node_id mapping
          - node:
            Displays Node_id to IPs mapping
      - pmap:
        "show pmap" displays partition map analysis of the Aerospike cluster.
      - users:
        "show users" displays users and their assigned roles, connections, and quota metrics
        for the Aerospike cluster.
        Modifiers: like
      - roles:
        "show roles" displays roles and their assigned privileges, allowlist, and quotas
        for the Aerospike cluster.
        Modifiers: like
      - udfs:
        "show udfs" displays UDF modules along with metadata.
        Modifiers: like
      - sindex:
        "show sindex" displays secondary indexes and static metadata.
        Modifiers: like
  - info:
    The "info" command provides summary tables for various aspects
    of Aerospike functionality.
    Modifiers: for, with
    Default: Displays network, namespace, and XDR summary information.
      - dc:
        "info dc" displays summary information for each datacenter.
        Replaced by "info xdr" for server >= 5.0.
      - network:
        "info network" displays network information for Aerospike.
      - set:
        "info set" displays summary information for each set.
      - sindex:
        "info sindex" displays summary information for Secondary Indexes (SIndex).
      - xdr:
        "info xdr" displays summary information for each datacenter.
      - namespace:
        "info namespace" command provides summary tables for various aspects
        of Aerospike namespaces.
        Modifiers: with
        Default: Displays usage and objects information for namespaces
          - object:
            Displays object information for each namespace.
          - usage:
            Displays usage information for each namespace.
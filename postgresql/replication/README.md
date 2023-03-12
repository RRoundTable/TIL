# Postgresql Replication

## Prerequisites

- Minikube
- Helm

## Objective

CP(Consistency-Partition Tolerance) Postgresql Replication Tutorial

![](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/CAP_Theorem_Venn_Diagram.png/440px-CAP_Theorem_Venn_Diagram.png)

The CAP theorem, also named Brewer's theorem after computer scientist Eric Brewer, states that any distributed data store can provide only two of the following three guarantees:

- Consistency: Every read receives the most recent write or an error.
- Availability: Every request receives a (non-error) response, without the guarantee that it contains the most recent write.
- Partition Tolerance: The system continues to operate despite an arbitrary number of messages being dropped (or delayed) by the network between nodes.

When a network partition failure happens, it must be decided whether to do one of the following:
- CP: cancel the operation and thus decrease the availability but ensure consistency
- AP: proceed with the operation and thus provide availability but risk inconsistency.


## Replication

### Sending Servers

These parameters can be set on any server that is to send replication data to one or more standby servers. The primary is always a sending server, so these parameters must always be set on the primary. 

- `max_wal_senders`(integer: 10): Specifies the maximum number of concurrent connections from standby servers or streaming base backup clients (i.e., the maximum number of simultaneously running WAL sender processes).  
- `max_replication_slots` (integer: 10): Specifies the maximum number of replication slots (see Section 27.2.6) that the server can support.
- `wal_keep_size` (integer: 10): Specifies the minimum size of past log file segments kept in the pg_wal directory, in case a standby server needs to fetch them for streaming replication.
- `max_slot_wal_keep_size` (integer: -1): Specify the maximum size of WAL files that replication slots are allowed to retain in the pg_wal directory at checkpoint time. If max_slot_wal_keep_size is -1 (the default), replication slots may retain an unlimited amount of WAL files.
- `wal_sender_timeout` (integer: 60): Terminate replication connections that are inactive for longer than this amount of time. This is useful for the sending server to detect a standby crash or network outage.
- `track_commit_timestamp` (boolean: false): Record commit time of transactions. This parameter can only be set in postgresql.conf file or on the server command line. The default value is off.

### Primary Servers
These parameters can be set on the primary server that is to send replication data to one or more standby servers.

- `synchronous_standby_names` (string): Specifies a list of standby servers that can support synchronous replication, as described in [Section 27.2.8](https://www.postgresql.org/docs/current/warm-standby.html#SYNCHRONOUS-REPLICATION). Specifying more than one synchronous standby can allow for very high availability and protection against data loss.
- `vacuum_defer_cleanup_age` (integer): Specifies the number of transactions by which VACUUM and HOT updates will defer cleanup of dead row versions. The default is zero transactions, meaning that dead row versions can be removed as soon as possible, that is, as soon as they are no longer visible to any open transaction.


### Standby Servers

These settings control the behavior of a standby server that is to receive replication data. Their values on the primary server are irrelevant.

- `primary_conninfo` (string): Specifies a connection string to be used for the standby server to connect with a sending server. 
- `primary_slot_name` (string): Optionally specifies an existing replication slot to be used when connecting to the sending server via streaming replication to control resource removal on the upstream node
- `promote_trigger_file` (string): Specifies a trigger file whose presence ends recovery in the standby.
- `hot_standby` (boolean): Specifies whether or not you can connect and run queries during recovery, as described in Section [27.4](https://www.postgresql.org/docs/current/hot-standby.html)
- `max_standby_archive_delay` (integer: 30): When hot standby is active, this parameter determines how long the standby server should wait before canceling standby queries that conflict with about-to-be-applied WAL entries [27.4.2](https://www.postgresql.org/docs/current/hot-standby.html#HOT-STANDBY-CONFLICT)
- `max_standby_streaming_delay` (integer: 30):When hot standby is active, this parameter determines how long the standby server should wait before canceling standby queries that conflict with about-to-be-applied WAL entries [27.4.2](https://www.postgresql.org/docs/current/hot-standby.html#HOT-STANDBY-CONFLICT)
- `wal_receiver_create_temp_slot` (boolean: false): Specifies whether the WAL receiver process should create a temporary replication slot on the remote instance when no permanent replication slot to use has been configured 
- `wal_receiver_status_interval` (integer: 10): Specifies the minimum frequency for the WAL receiver process on the standby to send information about replication progress to the primary or upstream standby, where it can be seen using the pg_stat_replication view
- `hot_standby_feedback` (boolean: false): Specifies whether or not a hot standby will send feedback to the primary or upstream standby about queries currently executing on the standby. 
- `wal_receiver_timeout` (integer: 60): Terminate replication connections that are inactive for longer than this amount of time.
- `wal_retrieve_retry_interval` (integer: 5): Specifies how long the standby server should wait when WAL data is not available from any sources (streaming replication, local pg_wal or WAL archive) before trying again to retrieve WAL data. 
- `recovery_min_apply_delay` (integer: 0): By default, a standby server restores WAL records from the sending server as soon as possible. It may be useful to have a time-delayed copy of the data, offering opportunities to correct data loss errors. 


## Setup

Create K8s cluster with 3 nodes.

```
make cluster
```

Check the nodes. (3 nodes)

```
kubectl get nodes
```

```
NAME             STATUS   ROLES           AGE     VERSION
postgresql       Ready    control-plane   5m11s   v1.26.1
postgresql-m02   Ready    <none>          4m43s   v1.26.1
postgresql-m03   Ready    <none>          4m19s   v1.26.1
```

Create configmap for postgres init script.

```
kubectl apply -f config/configamp.yaml
```

Create secret for postgres auth.

```
kubectl apply -f config/secret.yaml
```

Create local storageclass for postgresql.

```
kubectl apply -f volume/storageclass.yaml
```


Deploy postgresql chart.

```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm dependency build charts
helm install postgresql ./charts --values values.yaml
```

## Checklist

- [] 

## References
- https://en.wikipedia.org/wiki/CAP_theorem
- https://www.postgresql.org/docs/current/runtime-config-replication.html
- https://www.postgresql.org/docs/9.4/logicaldecoding-explanation.html#AEN67208
- https://www.postgresql.org/docs/current/warm-standby.html#SYNCHRONOUS-REPLICATION
- https://www.postgresql.org/docs/current/hot-standby.html
- https://www.postgresql.org/docs/current/hot-standby.html#HOT-STANDBY-CONFLICT

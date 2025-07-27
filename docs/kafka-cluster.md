# Kafka KRaft Architecture and Roles

In KRaft mode, metadata management is coordinated by a controller quorum, with a single elected leader managing operations and others replicating the metadata log for high availability.

## Important Concepts

**Controller Quorum and KRaft:** Kafka operates in KRaft mode (Kafka Raft Metadata mode), which removes the need for ZooKeeper by using a quorum of controller nodes. These controllers maintain the cluster metadata log, which stores: **Topic Definitions, Partition Assignments, Broker Registration & Leadership Elections**.
Once the Controller Quorum is setup:
 - One controller node is elected as **Leader**.
 - Other controller nodes act as **Followers**, replicating the **Leader's** metadata log.
The Raft consensus ensures that metadata is consistently replicated and fault-tolerant. If the leader fails, a new one is elected among the remaining voters.

**Roles: Controller & Broker:** A node can be a **Controller** &/or a **Broker** node.
 - **Controller Nodes:** 
    - Handle cluster-wide metadata.
    - Accept broker registrations.
    - Assign topic partitions and replicas.
    - Monitor broker health and reassign responsibilities on failure.
    - Metadata log replication (in case of being a **Follower** controller).
 - **Broker Nodes:** 
    - Host actual topic data (logs).
    - Receive and serve client read(**Consumers**)/write(**Producers**) requests.
    - Maintain replicas of partitions assigned to them.
    - Communicate with the controller to receive leadership/replication updates.
Each node has a defined role (process.roles) and a unique ID (node.id). Only brokers serve client traffic; controllers are strictly internal.

**Replication & ISR:** Kafka replicates partitions to ensure data availability. For each partition:
 - One broker is the **Leader**.
 - Others are **Replicas**
The ISR (In-Sync Replicas) is the set of brokers that are fully synchronized with the leader. Only ISR members can be promoted to leader if a failure occurs. Partition replication ensures data durability, while Raft consensus ensures metadata consistency. Although both involve replication and failover, they operate over distinct data types and follow different protocols.

**Topics & Partitioning:** Kafka topics are logical streams of messages. Each topic is divided into partitions, which are distributed across broker nodes. Partitioning enables:
 - Parallel consumption.
 - Horizontal scaling.
 - Independent log storage.
Each partition is hosted by exactly one leader broker, while zero or more other brokers maintain replicas (followers) for redundancy. Example:

```yaml
Topic: example-topic
Partitions: 3
Replication Factor: 2
```
This means each of the 3 partitions is hosted by one broker and replicated on another.

### Summary - Responsibilities and Failover
 - Controllers manage:
    - Metadata consistency.
    - Elections of partition leaders.
    - Broker failure detection.
    - Metadata log replication.
 - Brokers are responsible for:
    - Persisting log data for assigned partitions.
    - Responding to producers and consumers.
    - Synchronizing partition replicas.
On failure:
 - **Broker crash:** Replicas ensure availability, and the controller reassigns leadership.
 - **Controller crash:** Raft quorum elects a new leader, preserving metadata continuity.
This mechanism ensures that partition data remains available even during broker outages, maintaining cluster consistency and client availability.

### Operational Flow Summary

1. Controllers are started and form a quorum.
2. Brokers register with the controller leader.
3. Topics are created via CLI or API.
4. The controller assigns partitions and replicas.
5. **Producers** send messages to broker leaders.
6. Broker Followers replicate messages from leaders & the Controller ensures that ISRs are updated to maintain consistency before re-elections.
7. Consumers read from brokers.

## System Arcitecture

![Arquitectura](./arch.svg)










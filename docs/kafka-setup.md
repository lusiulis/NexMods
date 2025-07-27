# Kafka Deployment & Setup

This document outlines the deployment sequence and configuration of a Kafka cluster running in KRaft mode. It includes initialization steps, format operations, and the role of each service in the orchestration.

## Docker-compose Services & Structure

1. Initialization: init-perms
This step ensures proper directory permissions for the Kafka nodes (controllers and brokers) before any metadata is written or processes are started. It typically executes a script to set ownership and access rights for mounted volumes.
Example:

```yaml
# init-perms.sh
chown -R appuser:appuser /tmp/kraft-node-logs
```

This step is critical to avoid permission errors during snapshot writes or log access.

2. Format Phase
Before a controller or broker can join the cluster, it must initialize its metadata log using the kafka-storage.sh tool. This generates the meta.properties and initial metadata structures using the server.properties file for each respective node (ubicated in config/{node_name}).
Example:

```yaml
kafka-storage.sh format \
  --config /etc/kafka/kraft/server.properties \
  --cluster-id "$(kafka-storage.sh random-uuid)" \
  --ignore-formatted
```

Controller node server.properties example:

```properties
process.roles=controller
node.id=1
controller.quorum.voters=1@kafka-controller:9093,5@kafka-controller-2:9095,6@kafka-controller-3:9097 #Quorum controller's list
controller.listener.names=CONTROLLER
listeners=CONTROLLER://:9093
listener.security.protocol.map=CONTROLLER:PLAINTEXT
log.dirs=/tmp/kraft-node-logs
```

Broker node server.properties example:

```properties
process.roles=broker
node.id=2
controller.quorum.voters=1@kafka-controller:9093,5@kafka-controller-2:9095,6@kafka-controller-3:9097 #Quorum controller's list
listeners=PLAINTEXT://:9092
log.dirs=/tmp/kraft-node-logs
controller.listener.names=CONTROLLER
listener.security.protocol.map=PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT
```

3. Service Startup Sequence
Once the metadata log is setup & ready for each node the respective service is started. To make this services wait for the format to complete we use **wait-for-meta.sh** script, wich checks for **/tmp/kraft-node-logs/meta.properties** to be setup & ready to use. Give permissions to this .sh with **chmod +x wait-for-meta.sh**.

 - Controllers: Controllers start up & form a Raft quorum. The consensus will elect the controller leader & followers between the connected controllers & then it will be ready for re-elections in case of failure from any of the nodes. Now the controllers are setup & ready to listen for new brokers registrations & assign role responsibilities.
 - Brokers: Once the controller quorum is established, the brokers register with the controller leader & receive their role assignments. Once setup they will listen for any new topics, topics messages, replications & other responsibilities.

Check [Kafka KRaft Cluster Architecture and Roles](docs/kafka-cluster.md) for more information about roles & responsibilities.

4. Verification & Operational Checks
After deployment, check in the container logs for controller quorum's leader election & possible errors. Look for "Completed transition to LeaderState(...)", "Recorded new KRaft controller, from now on will use node" or any other related INFO logs.
Create topics and then describe topics & partitions from a broker container, Example:

Create:

```bash
/opt/kafka/bin/kafka-topics.sh \
  --create \
  --topic nombre-del-topic \
  --bootstrap-server kafka-broker:9092 \
  --partitions 3 \
  --replication-factor 2
```

Describe:

```bash
/opt/kafka/bin/kafka-topics.sh \
  --describe --topic example-topic \
  --bootstrap-server localhost:9092
```

Observe Raft replication:
Controllers log state transitions, leadership changes, and voter activity.

5. Notes on Recovery & Persistence
 - If a controller fails, the remaining controllers elect a new leader and preserve metadata continuity.
 - Nodes re-register automatically on restart.
 - Topics and their partition-leader assignments are preserved across restarts due to the persisted metadata log.

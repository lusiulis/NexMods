#!/bin/sh
echo "Waiting for meta.properties..."
until [ -f /tmp/kraft-node-logs/meta.properties ]; do
  sleep 1
done
echo "meta.properties found. Starting Kafka..."
exec /opt/kafka/bin/kafka-server-start.sh /etc/kafka/kraft/server.properties

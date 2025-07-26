-#!/bin/bash

set -e

BOOTSTRAP_SERVER="kafka-broker1:9092"

echo "Esperando a que Kafka esté disponible en $BOOTSTRAP_SERVER..."

# Esperar activamente a que el broker esté listo
until kafka-topics.sh --bootstrap-server "$BOOTSTRAP_SERVER" --list >/dev/null 2>&1; do
  echo "Kafka no disponible aún. Esperando..."
  sleep 2
done

echo "Kafka disponible. Creando topics..."

# Crear los topics (solo si no existen)
create_topic() {
  local topic=$1
  local partitions=$2
  local replication=$3

  if kafka-topics.sh --bootstrap-server "$BOOTSTRAP_SERVER" --list | grep -q "^$topic$"; then
    echo "Topic '$topic' ya existe. Saltando..."
  else
    kafka-topics.sh \
      --bootstrap-server "$BOOTSTRAP_SERVER" \
      --create \
      --topic "$topic" \
      --partitions "$partitions" \
      --replication-factor "$replication"
    echo "Topic '$topic' creado."
  fi
}

create_topic "order_created" 3 1
create_topic "order_canceled" 2 1
create_topic "low_stock" 2 1

echo "Todos los topics fueron verificados o creados correctamente."

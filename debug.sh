#!/bin/bash

function debug_produce() {
  data=$1
  sleep "0.00$((5 + RANDOM % 5))"
  echo "${data}" | kafkacat -b localhost:9092 -P -t payment.tx
  echo "${data}"
}

for ((i = 0; i < 1000; i++)); do
  debug_produce '{"user": 1234, "operation": "deposit", "amount": 87983.23}'
  debug_produce '{"user": 1235, "operation": "withdraw", "amount": 298387.34}'
  debug_produce '{"user": 1236, "operation": "transfer", "amount": 837920.53}'
  debug_produce '{"user": 1237, "operation": "deposit", "amount": 9836.94}'
  debug_produce '{"user": 1238, "operation": "withdraw", "amount": 6537.94}'
done

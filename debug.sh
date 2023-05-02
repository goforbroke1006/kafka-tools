#!/bin/bash

function debug_produce_payment() {
  data=$1
  sleep "0.00$((5 + RANDOM % 5))"
  echo "${data}" | kafkacat -b localhost:9092 -P -t payment.tx
  echo "${data}"
}

function debug_produce_user_data() {
  data=$1
  sleep "0.00$((5 + RANDOM % 5))"
  echo "${data}" | kafkacat -b localhost:9092 -P -t user.data
  echo "${data}"
}

for ((i = 0; i < 1000; i++)); do
  debug_produce_payment '{"user": 1234, "operation": "deposit", "amount": 87983.23}'
  debug_produce_user_data '{"user": 1235, "first_name": "Ivan", "birth_date": "1980-05-30"}'
  debug_produce_payment '{"user": 1236, "operation": "transfer", "amount": 837920.53}'
  debug_produce_payment '{"user": 1237, "operation": "deposit", "amount": 9836.94}'
  debug_produce_user_data '{"user": 1235, "last_name": "Ivanov"}'
  debug_produce_payment '{"user": 1238, "operation": "withdraw", "amount": 6537.94}'
done


echo '{"xxxxxxxxxxxxx": "7aef25f8-94e4-431b-879b-b8ff2dcd8107", "yyy": "", "zzz": "", "uuu": ""}' | kafkacat -b localhost:49092 -P -t topic_1
#!/bin/bash

function get_kafka_stat() {
  kafkaBrokers=$1
  kafkaTopic=$2

  kafkaTsFromMillis=$(date +%s%N -d "6 hours ago" | cut -b1-13)
  kafkaTsTillMillis=$(date +%s%N | cut -b1-13)

  # shellcheck disable=SC2207
  timestampsArr=(
    $(
      kafkacat -C \
        -b "${kafkaBrokers}" -t "${kafkaTopic}" -o s@"${kafkaTsFromMillis}" -o e@"${kafkaTsTillMillis}" \
        -q -e -f '%T '
    )
  )

  messagesCount=${#timestampsArr[@]}
  if [[ $messagesCount -lt 2 ]]; then
    echo "0 0 0 0"
    return
  fi

  timeFrom=${timestampsArr[0]}
  timeTill=${timestampsArr[${#timestampsArr[@]} - 1]}

  timeRange=$((timeTill - timeFrom))

  echo "${timeFrom} ${timeTill} ${timeRange} ${messagesCount}"
}

function print_dt_range() {
  kafkaTsFromMillis=$1
  kafkaTsTillMillis=$2

  timeFromStr=$(date -d "@$((kafkaTsFromMillis / 1000))")
  timeTillStr=$(date -d "@$((kafkaTsTillMillis / 1000))")
  echo "${timeFromStr} - ${timeTillStr}"
}

set -e

if [ $# -eq 1 ] && [ "$1" == '-h' ]; then
  echo "Script returns messages count rate per second."
  echo "It takes messages from topic for last 6 hours."
  echo "Arguments:"
  echo "  -b localhost:9092"
  echo "  -t <topic>"
  exit 1
fi

kafkaBrokers="localhost:9092"
kafkaTopic=""

while getopts b:t: flag; do
  case "${flag}" in
  b) kafkaBrokers=${OPTARG} ;;
  t) kafkaTopic=${OPTARG} ;;
  *) echo "Invalid flag ${flag}" && exit 1 ;;
  esac
done

[ -z "$kafkaBrokers" ] && printf "ERROR:\n  -b argument (brokers addresses) required\n" && exit 1
[ -z "$kafkaTopic" ] && printf "ERROR:\n  -t argument (topic name) required\n" && exit 1

read -r timeFrom timeTill timeRange msgCount <<<"$(get_kafka_stat "${kafkaBrokers}" "${kafkaTopic}")"

messagesRatePerSec=$(bc <<<"scale=12; ${msgCount}/${timeRange}*1000")

echo "Count rate: ${messagesRatePerSec} messages per second"

print_dt_range "${timeFrom}" "${timeTill}"

from datetime import datetime, timedelta
import argparse
import uuid

from kafka import KafkaConsumer, TopicPartition
from kafka.consumer.fetcher import ConsumerRecord

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='kafka-kowalski')
    parser.add_argument('-b', dest="bootstrap_servers", default='localhost:9092')
    parser.add_argument('-t', dest="topics", action='append', nargs=1, help='help:')
    args = parser.parse_args()

    topics_list = args.topics
    if topics_list is None or len(topics_list) == 0:
        consumer = KafkaConsumer(bootstrap_servers=args.bootstrap_servers,
                                 group_id=str(uuid.uuid4()),
                                 )
        topics_list = consumer.topics()
        topics_list = [tn for tn in topics_list if not len(tn) == 1]
    else:
        topics_list = [tt[0] for tt in topics_list]

    for topic_name in topics_list:
        consumer = KafkaConsumer(bootstrap_servers=args.bootstrap_servers,
                                 group_id=str(uuid.uuid4()),
                                 )
        tp = TopicPartition(topic_name, 0)
        consumer.assign([tp])

        d = datetime.today() - timedelta(hours=1, minutes=0)
        offset_from = consumer.offsets_for_times({tp: d.timestamp() * 1000})[tp].offset
        offset_till = consumer.offsets_for_times({tp: datetime.today().timestamp() * 1000})[tp].offset \
            if consumer.offsets_for_times({tp: datetime.today().timestamp() * 1000})[tp] is not None \
            else consumer.end_offsets([tp])[tp]
        consumer.seek_to_beginning(tp)
        consumer.seek(tp, offset_from)

        samples = 0
        timestamps = []
        byte_sizes = []

        for m in consumer:
            message = m  # type: ConsumerRecord
            samples += 1
            timestamps.append(int(message.timestamp) / 1000)
            byte_sizes.append(len(message.value))
            if message.offset == offset_till - 1:
                break

        if samples < 3:
            raise Exception('not enough messages')

        dt_from = datetime.fromtimestamp(min(timestamps)).strftime("%Y-%m-%d %H:%M:%S")
        dt_till = datetime.fromtimestamp(max(timestamps)).strftime("%Y-%m-%d %H:%M:%S")
        time_range = max(timestamps) - min(timestamps)
        msg_per_sec = float(samples) / time_range
        bytes_per_sec = sum(byte_sizes) / time_range
        print(topic_name, dt_from, dt_till, msg_per_sec, "msg/s", bytes_per_sec, "byte/s")

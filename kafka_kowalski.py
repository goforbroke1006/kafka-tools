from datetime import datetime, timedelta
import argparse
import uuid

from kafka import KafkaConsumer, TopicPartition
from kafka.consumer.fetcher import ConsumerRecord


def main():
    parser = argparse.ArgumentParser(prog='kafka-kowalski')
    parser.add_argument('-b', dest="bootstrap_servers", default='localhost:9092')
    parser.add_argument('-t', dest="topics", action='append', nargs=1, help='help:')
    parser.add_argument('--verbose', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    consumer = KafkaConsumer(
        bootstrap_servers=args.bootstrap_servers,
        group_id=str(uuid.uuid4()),
    )

    topics_list = args.topics
    if topics_list is None or len(topics_list) == 0:
        topics_list = consumer.topics()
        topics_list = [tn for tn in topics_list if not len(tn) == 1]
    else:
        topics_list = [tt[0] for tt in topics_list]

    for topic_name in topics_list:
        partitions = consumer.partitions_for_topic(topic_name)

        partition_num = next(iter(partitions))
        tp = TopicPartition(topic_name, partition_num)
        consumer.assign([tp])

        d = datetime.today() - timedelta(hours=1, minutes=0)
        offset_from = consumer.offsets_for_times({tp: d.timestamp() * 1000})[tp].offset \
            if consumer.offsets_for_times({tp: d.timestamp() * 1000})[tp] is not None \
            else 0
        offset_till = consumer.offsets_for_times({tp: datetime.today().timestamp() * 1000})[tp].offset \
            if consumer.offsets_for_times({tp: datetime.today().timestamp() * 1000})[tp] is not None \
            else consumer.end_offsets([tp])[tp]
        consumer.seek_to_beginning(tp)
        consumer.seek(tp, offset_from)

        samples = 0
        timestamps = []
        byte_sizes = []

        if args.verbose is not None:
            print(f'Check offsets {offset_from} .. {offset_till}')

        for m in consumer:
            samples += 1
            printProgressBar(samples, offset_till - 1, offset_from)

            message = m  # type: ConsumerRecord
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


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


if __name__ == '__main__':
    main()

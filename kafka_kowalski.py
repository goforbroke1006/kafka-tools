import argparse
from datetime import datetime

from kafka import KafkaConsumer, TopicPartition
from kafka.consumer.fetcher import ConsumerRecord


def main():
    parser = argparse.ArgumentParser(prog='kafka-kowalski')
    parser.add_argument('-b', dest="bootstrap_servers", default=None, help='server1:9092;server2:9092')
    parser.add_argument('-t', dest="topics", action='append', nargs=1, help='topic name (multiple allowed)')
    parser.add_argument('--verbose', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    topics_list = args.topics

    if topics_list is None or len(topics_list) == 0:
        consumer = KafkaConsumer(bootstrap_servers=args.bootstrap_servers.split(";"))
        topics_list = consumer.topics()
        topics_list = [tn for tn in topics_list if not len(tn) == 1]
        consumer.close()
    else:
        topics_list = [tt[0] for tt in topics_list]

    for topic_name in topics_list:
        consumer = KafkaConsumer(
            bootstrap_servers=args.bootstrap_servers.split(";"),
            group_id="kafwalski",
        )
        partitions = consumer.partitions_for_topic(topic_name)

        topic_partitions = []
        for p in partitions:
            tp = TopicPartition(topic=topic_name, partition=p)
            topic_partitions.append(tp)
        consumer.assign(topic_partitions)
        for tp in topic_partitions:
            consumer.seek_to_beginning(tp)

        offsets_res = consumer.end_offsets(topic_partitions)
        poll_res = consumer.poll(timeout_ms=5000, max_records=1000, update_offsets=False)

        for tp in poll_res:  # type: TopicPartition
            samples = 0
            timestamps = []
            byte_sizes = []

            for cr in poll_res[tp]:  # type: ConsumerRecord
                samples += 1
                timestamps.append(int(cr.timestamp / 1000))
                byte_sizes.append(len(cr.value))

            dt_from = datetime.fromtimestamp(min(timestamps)).isoformat('T') if len(timestamps) > 0 else None
            dt_till = datetime.fromtimestamp(max(timestamps)).isoformat('T') if len(timestamps) > 0 else None
            time_range = max(timestamps) - min(timestamps) if len(timestamps) > 0 else 0
            msg_per_sec = (float(samples) / time_range) if time_range > 0 else 0
            bytes_per_sec = (sum(byte_sizes) / time_range) if time_range > 0 else 0

            offset = offsets_res[tp]

            print(
                f"{tp.topic} {tp.partition} {offset} "
                f"{dt_from} {dt_till} "
                f"{samples} {round_float(msg_per_sec, 4)} msg/s {round_float(bytes_per_sec, 4)} bytes/s")

        consumer.close()


def round_float(f: float, n: int) -> float:
    m = pow(10, n)
    return int(f * m) / m


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
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
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()


if __name__ == '__main__':
    main()

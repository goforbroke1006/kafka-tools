# kafka-tools

Scripts for kafka. Bash wrappers over [kafkacat](https://github.com/edenhill/kcat).

### Usage

Analyze topic with Kowalski:

```shell
# without topics list (all topics analyze)
python3 kafka-kowalski.py -b localhost:9092
```

```shell
# or specify topics
python3 kafka-kowalski.py -b localhost:9092 -t payment.tx -t user.data
```

Kowalski's result:

```text
payment.tx 2022-11-26 01:29:14 2022-11-26 01:47:29 7.307811411881565 msg/s 425.68001474210115 byte/s
user.data 2022-11-26 01:29:14 2022-11-26 01:47:29 3.654082614727265 msg/s 184.53117204372688 byte/s
```

Messages count per second:

```shell
bash ./kafka-messages-count-rate.sh -b localhost:9092 -t payment.tx
```

Messages data size (in bytes) per seconds:

```shell
bash ./kafka-messages-data-rate.sh -b localhost:9092 -t payment.tx
```

### Useful links

* https://medium.com/@coderunner/debugging-with-kafkacat-df7851d21968

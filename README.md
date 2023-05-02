# kafka-tools

Scripts for kafka.
* Bash wrappers over [kafkacat](https://github.com/edenhill/kcat).
* Python-based script.

### Requirements

* Ubuntu
* Python 3

### Installation

```shell
pip uninstall -y gfb-kafka-tools
pip install git+https://github.com/goforbroke1006/kafka-tools.git
```

### Usage

Analyze topic with Kowalski:

```shell
# without topics list (all topics analyze)
kafwalski -b localhost:9092
```

```shell
# or specify topics
kafwalski -b localhost:9092 -t payment.tx -t user.data
```

Kowalski's result:

```text
user_registered 1 21 2023-05-02T11:52:47 2023-05-02T15:15:04 21 0.0017 msg/s 0.2381 bytes/s
user_registered 0 17 2023-05-02T11:50:53 2023-05-02T15:15:04 17 0.0013 msg/s 0.1692 bytes/s
...
<topic> <partition> <offset> <first ts> <last ts> <samples count> <message rate> msg/s <avg bytes per second> bytes/s

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

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
kafwalski
```

```shell
# or specify topics
kafwalski -b localhost:9092 -t payment.tx -t user.data
```

Kowalski's result:

```text
<topic 1> <first msg time> <last msg time> <avg msg per second> msg/s <avg bytes per second> byte/s
<topic 2> <first msg time> <last msg time> <avg msg per second> msg/s <avg bytes per second> byte/s
...
<topic N> <first msg time> <last msg time> <avg msg per second> msg/s <avg bytes per second> byte/s

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

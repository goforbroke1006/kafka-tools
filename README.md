# kafka-tools

Scripts for kafka. Bash wrappers over [kafkacat](https://github.com/edenhill/kcat).

### Usage

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

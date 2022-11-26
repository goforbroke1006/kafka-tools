#!/bin/bash

sudo apt update
sudo apt-get install -y librdkafka-dev libyajl-dev
sudo apt install -y kafkacat

pip install setuptools --upgrade
pip install kafka-python==2.0.2

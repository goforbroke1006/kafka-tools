#!/bin/bash

sudo apt update
sudo apt-get install -y librdkafka-dev libyajl-dev
sudo apt install -y kafkacat

pip install --upgrade pip
pip install --upgrade setuptools
pip install kafka-python==2.0.2

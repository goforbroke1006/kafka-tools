all: deps

deps:
	pip install -r requirements.txt

install:
	python3 -m pip install ./

uninstall:
	python3 -m pip uninstall gfb-kafka-tools

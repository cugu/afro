.PHONY: all install test unzip

all: install unzip test

install:
	python3 setup.py install

unzip:
	unzip -d test test/wsdf.dmg

test:
	pytest afro/afro_test.py

#!/bin/bash

pushd ~/light-maestro
git pull
python3 lightmaestro.py -c DmxUsbPro -p /dev/tty.usbserial-*
popd

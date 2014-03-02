#!/bin/bash

pushd ~/light-maestro
python3 lightmaestro.py -c DmxUsbPro -p /dev/tty.usbserial-*
popd

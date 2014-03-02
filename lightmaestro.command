#!/bin/bash

pushd ~/light-maestro
arch -i386 python3 lightmaestro.py -c DmxUsbPro -p /dev/tty.usbserial-*
popd

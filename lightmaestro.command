#!/bin/bash

pushd ~/light-maestro
arch -i386 python3 lightmaestro.py -c DmxUsbPro -p /dev/tty.usbserial-* --wavetrigger
#arch -i386 python3 lightmaestro.py -c ElationMagic -p USB --wavetrigger
popd

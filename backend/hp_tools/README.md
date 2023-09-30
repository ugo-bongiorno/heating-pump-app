# hp_tools

This folder contains an implementation of a modbus-RTU service, with basic functionalities :
- get the current water temperature
- get the current target water temperature
- set the target water temperature


## Setup

### Dependencies
This program requires [libmodbus](https://github.com/stephane/libmodbus/).
Install it on your machine, [following the instructions](https://github.com/stephane/libmodbus/#installation).

### Compile the .c program

Run ```make``` to compile the code on your machine.

N.B. : You can run ```make clean``` to remove the compiled code.


## Some settings that could be updated
Some values are hard-coded, at the beginning of ``hp_tools.c`` such as :
- some modbus RTU settings (baud rate, parity, etc.)
- the heat pump address on the modbus "network"
- the usb device to which the messages will be sent

As of now, I have no need to make these parameterizable.


## Connection errors handling
In case of connection issues with the heat pump, the functions described above will return ``-1``.


## A note on "testing"
Since I'm not very experienced in C, so I don't really know how to unit test this code.
I added a small script, under ``manual_test/``, that calls our functions one by one, after setting up the
connection with the pump. It should be executed with the USB-modbus adapter connected to your device and your heat pump.

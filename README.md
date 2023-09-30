# Heat pump remote control app

This repo contains a small web-app to remotely control my pool's heat pump.

My heat pump has a modbus port (in RTU mode), which allows to control it from a connected device.
My work is based on [this manual](https://gestor-doc-s3.s3.eu-west-1.amazonaws.com/documents/category/MAN10_54068-MB_ASTRALPOOLHEAT%20II%20-%20MODBUS_AP_v02_2015-.pdf) (direct download),
for a different model, which documents all the modbus messages for each functionality.
Luckily, the registers and associated values are the same for my model.


## Installation

TBD

## Developer Setup

TBD
 
### Set up the backend

In this section, we will assume your current working directory is ``backend/``

#### Install prerequisites for the modbus communications module
Since modbus is a very old protocol, I didn't find any good python libraries that work with RTU mode.
Yet, I found this nice modbus C library, that works with RTU mode : [libmodbus](https://github.com/stephane/libmodbus/). That's what we are gonna be using

##### [Install libmodbus](https://github.com/stephane/libmodbus/#installation)

#### Prepare environment variables

An easy way to set up "permanent" environment variables is to add them at the end of `~/.profile` :

Open your file `~/.profile`, and add the following line at the end

```
export LIBMODBUS_INSTALL_PATH=/absolute/path/to/your/local/install/install/of/libmodbus/
```

#### Compile the .c modbus-RTU communication program

```
cd hp_tools && make clean && make && cd ..
```



### Set up the frontend

TBD


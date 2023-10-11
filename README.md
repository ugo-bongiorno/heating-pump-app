# Heat pump remote control app

This repo contains a small web-app to remotely control my swimming pool's heat pump.

My heat pump has a modbus port (in RTU mode), which allows to control it from a connected device.
My work is based on [this manual (direct download)](https://gestor-doc-s3.s3.eu-west-1.amazonaws.com/documents/category/MAN10_54068-MB_ASTRALPOOLHEAT%20II%20-%20MODBUS_AP_v02_2015-.pdf),
for a different model of the same brand, which documents all the modbus messages for each functionality.
Luckily, the registers and associated values are the same for my heat pump model.


The backend is built using Python, and the code to communicate with a modbus device connected via USB is written in C. 

The frontend is built using Angular. It is my first time doing frontend, so it is clearly not perfect.

## Installation

The installation and run of the project require Docker. See the [official documentation](https://docs.docker.com/engine/install/) to install it.

### Local installation

In this section, we will describe how to run this project locally, on a desktop.

#### Set required environment variables

The following environment variable is required for the docker compose : ``MODBUS_USB_DEVICE``

You can set it automatically on session startup by adding the following line at the end of the file ``~/.profile``:

```shell
export MODBUS_USB_DEVICE="/dev/ttyUSB0"
```

After updating the file ``~/.profile``, you have to load it again (or restart your session) :

```shell
$ source ~/.profile
```

#### run the docker compose

To run the project, simply run

```shell
$ docker compose build && docker compose run
```

The project should be accessible at http://localhost:8000 

## Developer Setup

This section will guide you through all the steps to set up the project as a developer.

### Set up the backend

In this section, we will assume your current working directory is ``backend/``

#### Install prerequisites for the modbus communications module
Since modbus is a very old protocol, I didn't find any good python libraries that work with RTU mode.
Yet, I found this nice modbus C library, that works with RTU mode : [libmodbus](https://github.com/stephane/libmodbus/). That's what we are gonna be using

##### [Install libmodbus](https://github.com/stephane/libmodbus/#installation)

Install libmodbus dependencies :

```shell
$ sudo apt-get update && sudo apt-get install pkg-config autoconf libtool
```

Download and extract the source code, then run (from the extracted source code folder)

```shell
$ /autogen.sh && ./configure && make && make install
```

N.B. : you can customize the installation path by adding ``--prefix=/custom/install/path/`` after configure (example : ``./configure --prefix=/usr/local/``)

Finally, run 

```shell
$ ldconfig
```

#### Compile the .c modbus-RTU communication program

```shell
$ cd hp_tools && make clean && make && cd ..
```

#### Create a virtual env and activate it
```shell
$ python3 -m venv env
```

```shell
$ source env/bin/activate
```

#### Install python dependencies

```shell
(env) $ pip install --upgrade pip && pip install -r requirements.txt
```

#### Run unit tests

```shell
(env) $ pytest
```

#### Start the backend server

```shell
(env) $ uvicorn heat_pump_backend:app
```

### Set up the frontend

In this section, we will assume your current working directory is ``frontend/heat-pump-app/``

#### install node and angular

Follow the installation steps to install [node (and npm)](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) and [angular](https://angular.io/guide/setup-local#install-the-angular-cli)

#### Install the dependencies

Run 
```shell
$ npm install
```

#### Run the frontend development server

Run 
```shell
$ ng serve
```

Navigate to http://localhost:4200/. The app will automatically reload if you change any of the source files.

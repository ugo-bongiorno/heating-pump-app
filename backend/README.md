# Backend of the heat pump app

This is the backend of the swimming pool heat pump app.

It contains 2 main parts :
 - a very simple REST API, built in python, using [FastAPI](https://github.com/tiangolo/fastapi)
 - a Modbus communications module, built in C, using [libmodbus](https://github.com/stephane/libmodbus/)


## Setup

See [the setup in the main readme](../README.md)

## Some things that could be improved

- This API is very unsecure : anyone can send requests to the backend. There is no authentication or authorizations.
Yet, for my use case, this is suitable, since the server will be hosted on my local network only.
If I wanted to make this tool 100% remote (accessible from outside my local network), I would need to add
a login system, and authorizations.

## Run the tests

The tests are located in ``backend/tests``. They only test our API endpoints :
the `.c` functions are mocked. To read more about the `.c` functions and how
to 'test' them, refer to [hp_tools/README.md](./hp_tools/README.md).

To run the tests, make sure your working directory is ``backend/``, then simply run

```shell
(env) $ pytest
```

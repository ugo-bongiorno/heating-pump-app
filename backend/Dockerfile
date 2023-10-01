FROM python:3.9

WORKDIR /usr/src/heat-pump-app-backend/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy, and compile .c source code
COPY ./hp_tools ./hp_tools

WORKDIR /usr/src/heat-pump-app-backend/hp_tools

RUN curl -LO https://github.com/stephane/libmodbus/archive/refs/tags/v3.1.10.tar.gz

RUN mkdir libmodbus && tar -xvf v3.1.10.tar.gz -C ./libmodbus

WORKDIR /usr/src/heat-pump-app-backend/hp_tools/libmodbus/libmodbus-3.1.10

RUN ./autogen.sh

ENV LIBMODBUS_INSTALL_PATH /usr/src/heat-pump-app-backend/hp_tools/libmodbus/libmodbus-3.1.10/src/

RUN ./configure && make install

WORKDIR /usr/src/heat-pump-app-backend/hp_tools

RUN make all

# update pip
WORKDIR /usr/src/heat-pump-app-backend/

RUN pip install --upgrade pip

# copy only the requirements and install them, so that docker can
# cache these steps
COPY ./requirements.txt .

RUN pip install -r requirements.txt

# now, copy all the source code
COPY . .

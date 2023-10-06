FROM debian:bullseye-slim

WORKDIR /usr/src/heat-pump-app-backend/

RUN apt update

RUN apt install python3 python3-pip -y

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install libmodbus dependencies
RUN apt install curl -y

RUN apt install pkg-config -y

RUN apt install autoconf -y

RUN apt install libtool -y

# install libmodbus
RUN mkdir /usr/src/libmodbus/

WORKDIR /usr/src/

RUN curl -LO https://github.com/stephane/libmodbus/archive/refs/tags/v3.1.10.tar.gz

RUN tar -xvf v3.1.10.tar.gz -C ./libmodbus

WORKDIR /usr/src/libmodbus/libmodbus-3.1.10

RUN ./autogen.sh

RUN ./configure --prefix=/usr/local/ && make && make install

RUN ldconfig

# copy, and compile my .c source code
WORKDIR /usr/src/heat-pump-app-backend

RUN mkdir -p /usr/src/heat-pump-app-backend/hp_tools

COPY ./hp_tools ./hp_tools

WORKDIR /usr/src/heat-pump-app-backend/hp_tools

RUN make all

# update pip
WORKDIR /usr/src/heat-pump-app-backend

RUN pip install --upgrade pip

# copy only the requirements and install them, so that docker can
# cache these steps
COPY ./requirements.txt .

RUN pip install -r requirements.txt

# now, copy all the source code
COPY . .

CMD ["uvicorn", "heat_pump_backend:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.9

WORKDIR /usr/src/heat-pump-app-backend/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# copy only the requirements and install them, so that docker can
# cache these steps
copy ./requirements.txt .

RUN pip install -r requirements.txt

# now, copy all the source code
COPY . .

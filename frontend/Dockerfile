# 1st step : build the minified codebase
FROM node:16.20.2-bullseye as build-stage
WORKDIR /app

# copy the dependencies and install them
COPY ./heat-pump-app/package*.json ./
RUN npm ci

# copy the whole code base, and build the frontend
COPY ./heat-pump-app/ .
RUN npm run build

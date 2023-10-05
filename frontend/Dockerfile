FROM node:16.20.2-bullseye
WORKDIR /app

# copy the dependencies and install them
COPY ./heat-pump-app/package*.json ./
RUN npm ci

# copy the whole code base, and build the frontend
COPY ./heat-pump-app/ .

# build the minified code base
RUN npm run build

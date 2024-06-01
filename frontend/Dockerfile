FROM node:16.20.2-bullseye as build
WORKDIR /app

# copy the dependencies and install them
COPY ./heat-pump-app/package*.json ./

RUN npm ci

# copy the whole code base, and build the frontend
COPY ./heat-pump-app/ .

RUN npm run build

# build a reverse proxy, that will contain the minified codebase
FROM nginx:latest

COPY --from=build /app/dist/heat-pump-app/ /usr/share/nginx/html

COPY ./nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

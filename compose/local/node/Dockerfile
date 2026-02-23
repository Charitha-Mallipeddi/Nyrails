FROM docker.io/node:24.7.0-bookworm-slim

WORKDIR /app

COPY ./package.json /app

RUN npm install && npm cache clean --force

EXPOSE 5173

ENV PATH=./node_modules/.bin/:$PATH

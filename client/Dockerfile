FROM node:latest

WORKDIR /app

COPY /atom_chat/package*.json ./
RUN npm install

COPY ./atom_chat .

FROM node:23.4.0-alpine

WORKDIR /app

COPY package.json .
COPY next.config.mjs .

RUN npm install

ARG DISCORD_BOT_URL="http://localhost:7546"
ARG BASE_URL="http://localhost:3000"

COPY . .

RUN npm run build


EXPOSE 3000

CMD [ "npm", "start" ]
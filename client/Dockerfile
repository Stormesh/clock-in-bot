FROM node:23.4.0-alpine

WORKDIR /app

COPY package.json .
COPY next.config.mjs .

RUN npm install

COPY . .

RUN npm run build


EXPOSE 3000

CMD [ "npm", "start" ]
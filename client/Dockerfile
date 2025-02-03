FROM node:23.4.0-alpine

WORKDIR /app

COPY package.json .
COPY next.config.mjs .

RUN npm install

ENV NODE_ENV production
ARG NEXT_PUBLIC_DISCORD_BOT_URL="https://c8k0os0gwksk484w8skkwgkc.boom-va.com"

ENV NEXT_PUBLIC_DISCORD_BOT_URL $NEXT_PUBLIC_DISCORD_BOT_URL

COPY . .

RUN npm run build


EXPOSE 3000

CMD [ "npm", "start" ]
FROM node:lts-alpine

WORKDIR /app

COPY . /app

RUN yarn

ENTRYPOINT [ "node" ]

CMD [ "index.js" ]
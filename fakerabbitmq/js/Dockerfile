FROM node:14.15.4-alpine3.12

WORKDIR /app

COPY . /app

RUN npm install

ENTRYPOINT [ "node" ]

CMD [ "index.js" ]
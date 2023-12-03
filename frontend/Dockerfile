FROM node:current-alpine
COPY ./src /app

WORKDIR /app

RUN npm install
CMD ["npm","run", "build"]
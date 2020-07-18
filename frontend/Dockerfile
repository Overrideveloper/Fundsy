FROM node:lts-alpine

RUN npm install -g yarn --force

WORKDIR /frontend

COPY package.json /frontend/package.json
COPY yarn.lock /frontend/yarn.lock
COPY tsconfig.json /frontend/tsconfig.json

RUN yarn install
RUN yarn global add @vue/cli@3.7.0

COPY . /frontend/

RUN yarn serve
FROM node:12.16.2-alpine as bundler

RUN mkdir -p /usr/app/src
WORKDIR /usr/app/src
COPY package.json yarn.lock /usr/app/src/
RUN yarn

COPY . /usr/app/src/

RUN yarn build

FROM nginx:1.17.9

COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=bundler /usr/app/src/public /usr/share/nginx/html

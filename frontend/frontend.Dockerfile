FROM node:16 as build
WORKDIR /opt/alldaydj

COPY ./frontend/ .

RUN yarn
RUN yarn run build

FROM nginx:stable-alpine
COPY --from=build /opt/alldaydj/build /usr/share/nginx/html
COPY ./frontend/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
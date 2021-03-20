FROM node:14.16-alpine as build
WORKDIR /opt/alldaydj

COPY ./frontend/ .

RUN yarn
RUN yarn run build

FROM nginx:stable-alpine
COPY --from=build /opt/alldaydj/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
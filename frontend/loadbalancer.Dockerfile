FROM nginx:stable-alpine
COPY ./frontend/loadbalancer.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
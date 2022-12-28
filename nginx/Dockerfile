FROM nginx:1.23.3-alpine-slim

RUN rm /etc/nginx/conf.d/default.conf
# Copy the nginx configuration file
COPY nginx.conf /etc/nginx/conf.d

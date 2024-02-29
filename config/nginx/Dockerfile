#FROM node:16-buster as builder
#WORKDIR /app
#COPY ./frontend/ ./
#RUN yarn install && yarn build

FROM nginx:1.20.1
#COPY --from=builder /app/build /etc/nginx/html/
CMD ["nginx", "-g", "daemon off;"]
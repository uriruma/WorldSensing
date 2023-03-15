# FRONTEND
FROM node:alpine

WORKDIR /my-api

COPY my-api/package*.json ./

RUN npm install

COPY my-api ./

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]

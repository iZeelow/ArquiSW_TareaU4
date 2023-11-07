FROM node:18-alpine

WORKDIR /app

COPY package.json ./

RUN npm install

COPY . .

COPY .next ./.next

EXPOSE 50002

CMD [ "npm", "run","dev" ]
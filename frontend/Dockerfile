FROM node:18

WORKDIR /app

COPY package.json ./

RUN npm install

COPY . .

EXPOSE 3000

RUN npm run build

CMD ["npm", "run", "dev:watch"]

# RUN npm install -g serve
# CMD ["serve", "-s", "build"]

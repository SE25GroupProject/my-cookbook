FROM node:18

WORKDIR /app

COPY package.json ./

RUN npm install --force

COPY . .

EXPOSE 3000


CMD ["npm", "run", "start"]

# RUN npm run build

# RUN npm install -g serve
# CMD ["serve", "-s", "build"]

FROM	node:21.1 AS build

WORKDIR	/app

COPY	package.json ./

RUN		npm install

#copie tout le dossier
COPY	. .

EXPOSE 3333

RUN npm update

RUN npm run start:dev
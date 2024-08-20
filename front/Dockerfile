# Define a imagem base
FROM node:18-alpine

# Cria um diretório para o aplicativo
WORKDIR /app

RUN chown node:node /app

# Instala o Next.js globalmente
RUN npm install -g next

# Copia os arquivos do projeto
COPY ["package.json", "package-lock.json*", "./"]

# Instala as dependências
RUN npm install

COPY . .

# Expõe a porta na imagem
EXPOSE ${PORT}

# Inicia o aplicativo
CMD ["npm", "run", "dev"]
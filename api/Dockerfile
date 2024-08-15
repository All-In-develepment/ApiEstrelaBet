# Use a imagem base do Python
FROM python:3.10-alpine

# Definindo o diretório de trabalho dentro do contêiner
WORKDIR /app

ARG FLASK_PORT
# Copiando o arquivo de requisitos para o contêiner
COPY requirements.txt .

# Instalar dependências do sistema
RUN apk update && \
    apk add --no-cache tzdata

ENV TZ=America/Sao_Paulo
# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação para o contêiner
COPY . .

EXPOSE $FLASK_PORT

# Definir o ponto de entrada padrão para o contêiner
CMD ["flask", "run", "--host=0.0.0.0"]

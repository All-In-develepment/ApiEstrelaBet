# Usa uma imagem oficial do Python como base
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos e instala as dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação e os arquivos de conexão para o diretório de trabalho
# COPY app.py ./
# COPY mongo_connection_v2.py ./
COPY . .
# ENV FLASK_ENV=development
# ENV FLASK_DEBUG=1
# Expõe a porta 5000 para acessar a API Flask
EXPOSE $FLASK_PORT

# Comando para rodar a aplicação
# CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["python", "app.py"]
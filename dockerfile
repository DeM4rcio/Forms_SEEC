# ----- ESTÁGIO 1: Imagem de Build -----
# Usa uma imagem oficial do Python como base
FROM python:3.11-slim as build

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instala as dependências de sistema necessárias
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos de dependência
COPY requirements.txt .

# Instala as dependências do Python
# O flag --no-cache-dir garante que o pip não armazene arquivos de cache, economizando espaço
RUN pip install --no-cache-dir -r requirements.txt


# ----- ESTÁGIO 2: Imagem Final (Produção) -----
# Usa a mesma imagem base, mas sem as ferramentas de build
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia as bibliotecas instaladas do estágio de build
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copia todo o código da sua aplicação para o contêiner
COPY . .

# Define as variáveis de ambiente (ajuste conforme necessário)
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=app.settings  

# Expõe a porta que o Gunicorn/Django irá ouvir (a porta padrão é 8000)
EXPOSE 8888

# Comando para rodar a aplicação usando Gunicorn, um servidor WSGI para produção
# Substitua 'seu_projeto.wsgi' pelo caminho correto do seu arquivo WSGI
CMD ["gunicorn", "--bind", "0.0.0.0:8888", "app.wsgi"]
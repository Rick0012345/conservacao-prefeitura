FROM python:3.11-slim

# Variáveis de ambiente para otimização do Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /code

# Install system dependencies em uma única camada
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Upgrade pip para versão mais recente
RUN pip install --upgrade pip

# Copy requirements first para melhor cache
COPY requirements.txt /code/

# Install Python dependencies com cache otimizado
RUN pip install --no-cache-dir -r requirements.txt

# Copy entrypoint script antes do código para melhor cache
COPY entrypoint.sh /code/
RUN chmod +x /code/entrypoint.sh

# Copy project por último para aproveitar cache das camadas anteriores
COPY . /code/

ENTRYPOINT ["/code/entrypoint.sh"]
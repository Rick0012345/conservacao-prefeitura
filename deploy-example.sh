#!/bin/bash
# Exemplo de script de deploy para produção

# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar variáveis de ambiente de produção
# Copie o arquivo .env-prod e configure as variáveis necessárias
cp dotenv/.env-prod dotenv/.env

# 3. Executar migrações
python manage.py migrate

# 4. Coletar arquivos estáticos
python manage.py collectstatic --noinput

# 5. Verificar configurações de deploy
python manage.py check --deploy

# 6. Criar superusuário (opcional)
# python manage.py createsuperuser

echo "Deploy configurado! Lembre-se de:"
echo "1. Configurar SECRET_KEY de produção"
echo "2. Definir ALLOWED_HOSTS corretos"
echo "3. Configurar HTTPS quando disponível"
echo "4. Verificar conexão com banco PostgreSQL do Render"
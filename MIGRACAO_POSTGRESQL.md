# Migração para PostgreSQL - Sistema de Conservação da Prefeitura

## Pré-requisitos

1. **PostgreSQL instalado** no seu sistema
2. **Python 3.8+** com pip
3. **Dependências atualizadas**

## Passos para Migração

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar PostgreSQL

#### Criar Banco de Dados
```sql
-- Conecte ao PostgreSQL como superusuário
psql -U postgres

-- Criar banco de dados
CREATE DATABASE conservacao_prefeitura;

-- Criar usuário (opcional, mas recomendado)
CREATE USER conservacao_user WITH PASSWORD 'sua_senha_segura';

-- Dar permissões ao usuário
GRANT ALL PRIVILEGES ON DATABASE conservacao_prefeitura TO conservacao_user;

-- Sair do psql
\q
```

#### Atualizar Configurações
Edite o arquivo `project/settings.py` e atualize as configurações do banco:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'conservacao_prefeitura',
        'USER': 'conservacao_user',  # ou 'postgres'
        'PASSWORD': 'sua_senha_segura',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Migrar Dados (se necessário)

Se você já tem dados no SQLite que deseja preservar:

#### Opção A: Usando django-extensions (Recomendado)
```bash
# Instalar django-extensions
pip install django-extensions

# Adicionar 'django_extensions' ao INSTALLED_APPS em settings.py

# Exportar dados do SQLite
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > dados_backup.json

# Após configurar PostgreSQL, importar dados
python manage.py loaddata dados_backup.json
```

#### Opção B: Migração Manual
```bash
# Fazer backup do SQLite atual
cp db.sqlite3 db.sqlite3.backup

# Criar novas migrações
python manage.py makemigrations

# Aplicar migrações no PostgreSQL
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
```

### 4. Configurar Upload de Imagens

#### Criar Diretórios Necessários
```bash
# Criar diretório para uploads
mkdir -p media/relatorios

# Criar diretório temporário
mkdir -p temp_uploads

# Dar permissões adequadas (Linux/Mac)
chmod 755 media temp_uploads
```

### 5. Testar a Instalação

```bash
# Executar servidor de desenvolvimento
python manage.py runserver

# Acessar http://localhost:8000/admin
# Fazer login e testar upload de imagens
```

## Configurações de Produção

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
DEBUG=False
SECRET_KEY=sua_chave_secreta_aqui
DATABASE_URL=postgresql://usuario:senha@localhost:5432/conservacao_prefeitura
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
```

### Configurações de Segurança
```python
# Em settings.py
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Servidor Web
Para produção, use um servidor web como Nginx + Gunicorn:

```bash
pip install gunicorn
```

## Solução de Problemas

### Erro de Conexão com PostgreSQL
- Verifique se o PostgreSQL está rodando
- Confirme as credenciais no settings.py
- Teste a conexão: `psql -U usuario -d conservacao_prefeitura`

### Erro de Permissões
- Verifique se o usuário tem permissões no banco
- Confirme se o diretório media tem permissões de escrita

### Erro de Upload de Imagens
- Verifique se o diretório media existe
- Confirme as configurações de MAX_UPLOAD_SIZE
- Teste com imagens menores primeiro

## Backup e Restauração

### Backup do Banco
```bash
pg_dump -U usuario -d conservacao_prefeitura > backup_$(date +%Y%m%d).sql
```

### Restauração
```bash
psql -U usuario -d conservacao_prefeitura < backup_20241201.sql
```

### Backup de Imagens
```bash
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
``` 
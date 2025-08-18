# Guia de Deploy para Produção

## Configuração do Banco de Dados PostgreSQL (Render)

O projeto está configurado para usar PostgreSQL em produção através do Render. As configurações estão no arquivo `dotenv/.env-prod`.

### Variáveis de Ambiente de Produção

As seguintes variáveis devem ser configuradas no seu serviço de hosting:

```bash
# Database Configuration - Render PostgreSQL
POSTGRES_DB=db_prod_chmg
POSTGRES_USER=db_prod_chmg_user
POSTGRES_PASSWORD=wP6JeOaHE9AlLmTwnCBc7sokJkzo3Ygo
POSTGRES_HOST=dpg-d2t4ojripnbc739ns1f0-a
POSTGRES_PORT=5432

# Django Configuration
DEBUG=0
SECRET_KEY=your-production-secret-key-here-change-this
DJANGO_SETTINGS_MODULE=settings.prod
ALLOWED_HOSTS=your-domain.com,your-app.onrender.com

# Python Environment
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1
```

## Passos para Deploy

### 1. Configurar Variáveis de Ambiente

**IMPORTANTE**: Antes do deploy, você deve:

1. **Gerar uma nova SECRET_KEY** para produção:
   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

2. **Configurar ALLOWED_HOSTS** com seus domínios reais:
   ```bash
   ALLOWED_HOSTS=seudominio.com,seuapp.onrender.com
   ```

### 2. Configurações de Segurança

Quando tiver HTTPS configurado, descomente as seguintes linhas em `settings/prod.py`:

```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 3. Migrações do Banco de Dados

Após o deploy, execute as migrações:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 4. Configurações Opcionais

#### Email (Gmail)
```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=1
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
```

#### Sentry (Monitoramento de Erros)
```bash
SENTRY_DSN=sua-dsn-do-sentry
```

#### Redis (Cache)
```bash
REDIS_URL=redis://localhost:6379/1
```

## Diferenças entre Desenvolvimento e Produção

| Configuração | Desenvolvimento | Produção |
|--------------|-----------------|----------|
| DEBUG | True | False |
| Database | PostgreSQL local (Docker) | PostgreSQL Render |
| ALLOWED_HOSTS | ['*'] | Domínios específicos |
| SECRET_KEY | Desenvolvimento | Produção (diferente) |
| HTTPS | Não obrigatório | Recomendado |
| Logging | Console simples | Estruturado |
| Static Files | Django padrão | WhiteNoise |

## Comandos Úteis

### Testar configurações de produção localmente:
```bash
# Copie .env-prod para .env temporariamente
cp dotenv/.env-prod dotenv/.env

# Execute com configurações de produção
python manage.py check --deploy

# Restaure o arquivo original
cp dotenv/.env-dev dotenv/.env  # se você tiver um arquivo de dev
```

### Verificar configurações:
```bash
python manage.py diffsettings
```

## Checklist de Deploy

- [ ] SECRET_KEY de produção configurada
- [ ] ALLOWED_HOSTS configurado com domínios corretos
- [ ] Variáveis de banco de dados do Render configuradas
- [ ] DEBUG=0 em produção
- [ ] HTTPS configurado (se disponível)
- [ ] Migrações executadas
- [ ] Arquivos estáticos coletados
- [ ] Monitoramento configurado (Sentry)
- [ ] Backup do banco de dados configurado

## Troubleshooting

### Erro de conexão com banco:
- Verifique se as credenciais do Render estão corretas
- Confirme se o host do banco está acessível
- Verifique se a porta 5432 está aberta

### Erro 500 em produção:
- Verifique os logs do servidor
- Confirme se DEBUG=0
- Verifique se ALLOWED_HOSTS está configurado
- Execute `python manage.py check --deploy`

### Arquivos estáticos não carregam:
- Execute `python manage.py collectstatic`
- Verifique configurações de STATIC_URL e STATIC_ROOT
- Confirme se WhiteNoise está instalado
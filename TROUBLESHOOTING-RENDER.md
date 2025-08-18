# Troubleshooting - Erro 128 no Deploy do Render

## ❌ Erro Atual
```
==> Deploying... 
==> Exited with status 128 
==> Common ways to troubleshoot your deploy: https://render.com/docs/troubleshooting-deploys
```

## 🔍 Diagnóstico do Problema

O **status 128** no Render geralmente indica um dos seguintes problemas:

### 1. Problemas de Configuração (Mais Comum)
- ❌ Variáveis de ambiente não configuradas
- ❌ Comando de build ou start incorreto
- ❌ Versão do Python incompatível
- ❌ Dependências faltando

### 2. Problemas de Código
- ❌ Erro de sintaxe no código
- ❌ Imports incorretos
- ❌ Arquivos não encontrados

## ✅ Soluções Implementadas

Já foram criados os seguintes arquivos para resolver os problemas mais comuns:

### 📁 Arquivos de Configuração:
- `render.yaml` - Configuração automática do Render
- `runtime.txt` - Especifica Python 3.11.0
- `requirements.txt` - Atualizado com gunicorn
- `settings/prod.py` - Configurações de produção

### 🔧 Configurações Implementadas:

**Build Command:** `pip install -r requirements.txt`
**Start Command:** `gunicorn project.wsgi:application`
**Python Version:** `3.11.0`

## 🚀 Passos para Resolver

### Passo 1: Verificar Logs Detalhados
1. Acesse o **Render Dashboard**
2. Clique no seu serviço
3. Vá em **Events** → clique em **Deploy** (falhou)
4. Procure por mensagens de erro específicas

### Passo 2: Configurar Variáveis de Ambiente
No Render Dashboard, configure estas variáveis:

```bash
# Obrigatórias
DJANGO_SETTINGS_MODULE=settings.prod
DEBUG=0
POSTGRES_DB=db_prod_chmg
POSTGRES_USER=db_prod_chmg_user
POSTGRES_PASSWORD=wP6JeOaHE9AlLmTwnCBc7sokJkzo3Ygo
POSTGRES_HOST=dpg-d2t4ojripnbc739ns1f0-a
POSTGRES_PORT=5432

# Gerar nova SECRET_KEY
SECRET_KEY=[GERAR_NOVA_CHAVE]

# Configurar domínio
ALLOWED_HOSTS=seu-app.onrender.com

# Python
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1
```

### Passo 3: Gerar Nova SECRET_KEY
```python
# Execute localmente:
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Passo 4: Configurar Comandos no Render
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn project.wsgi:application`

### Passo 5: Usar o arquivo render.yaml
1. Faça commit do arquivo `render.yaml`
2. No Render, use "Deploy from Blueprint"
3. Aponte para o repositório com o `render.yaml`

## 🔍 Erros Comuns e Soluções

### ModuleNotFoundError
```bash
# Solução: Verificar se todas as dependências estão no requirements.txt
pip freeze > requirements.txt
```

### SyntaxError
```bash
# Solução: Verificar compatibilidade do Python
# Usar Python 3.11.0 (especificado no runtime.txt)
```

### Database Connection Error
```bash
# Solução: Verificar variáveis do banco PostgreSQL
# Confirmar se o host do Render está correto
```

### Static Files Error
```bash
# Solução: WhiteNoise já está configurado
# Executar collectstatic após deploy
python manage.py collectstatic --noinput
```

## 📋 Checklist de Verificação

- [ ] Logs do deploy verificados
- [ ] Todas as variáveis de ambiente configuradas
- [ ] SECRET_KEY de produção gerada
- [ ] ALLOWED_HOSTS configurado com domínio correto
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `gunicorn project.wsgi:application`
- [ ] Python version: 3.11.0
- [ ] Gunicorn instalado no requirements.txt
- [ ] WhiteNoise configurado para static files
- [ ] Banco PostgreSQL acessível

## 🆘 Se o Problema Persistir

1. **Verifique os logs específicos** no Render Dashboard
2. **Teste localmente** com as configurações de produção:
   ```bash
   # Copie .env-prod para .env temporariamente
   cp dotenv/.env-prod dotenv/.env
   
   # Teste com configurações de produção
   python manage.py check --deploy
   python manage.py collectstatic --noinput
   gunicorn project.wsgi:application
   ```

3. **Procure o erro específico** nos logs e pesquise no Stack Overflow

4. **Verifique a documentação** do Render para Django: https://render.com/docs/deploy-django

## 📞 Próximos Passos

1. Implemente as configurações acima
2. Faça um novo deploy
3. Se ainda houver erro, compartilhe os logs específicos para diagnóstico mais detalhado

---

**Nota:** O arquivo `render.yaml` automatiza a maioria dessas configurações. Use-o para deploys mais simples e consistentes.
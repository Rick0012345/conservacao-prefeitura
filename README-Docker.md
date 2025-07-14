# 🐳 Configuração Docker - Sistema de Conservação

Este projeto agora suporta Docker para facilitar o desenvolvimento, especialmente no Windows onde há problemas com PostgreSQL.

## 📋 Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e rodando
- Git (para clonar o projeto)

## 🚀 Como usar

### 1. Primeiro uso (build inicial)
```bash
# Construir e iniciar os containers
docker-compose up --build

# Ou executar em background
docker-compose up --build -d
```

### 2. Uso normal (após primeira vez)
```bash
# Iniciar os containers
docker-compose up

# Ou executar em background
docker-compose up -d
```

### 3. Parar os containers
```bash
# Parar containers
docker-compose down

# Parar e remover volumes (⚠️ apaga dados do banco)
docker-compose down -v
```

## 🌐 Acessos

- **Aplicação Django**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin
  - Usuário: `admin`
  - Senha: `admin123`
- **PostgreSQL**: localhost:5432
  - Banco: `conservacao_prefeitura`
  - Usuário: `postgres`
  - Senha: `postgres`

## 🛠️ Comandos úteis

### Executar comandos Django no container
```bash
# Executar migrações
docker-compose exec web python manage.py migrate

# Criar superusuário
docker-compose exec web python manage.py createsuperuser

# Abrir shell Django
docker-compose exec web python manage.py shell

# Executar testes
docker-compose exec web python manage.py test
```

### Logs e debugging
```bash
# Ver logs de todos os serviços
docker-compose logs

# Ver logs apenas do Django
docker-compose logs web

# Ver logs apenas do PostgreSQL
docker-compose logs db

# Seguir logs em tempo real
docker-compose logs -f web
```

### Banco de dados
```bash
# Conectar ao PostgreSQL
docker-compose exec db psql -U postgres -d conservacao_prefeitura

# Fazer backup do banco
docker-compose exec db pg_dump -U postgres conservacao_prefeitura > backup.sql

# Restaurar backup
docker-compose exec -T db psql -U postgres conservacao_prefeitura < backup.sql
```

## 🔧 Estrutura dos arquivos Docker

- `docker-compose.yml` - Orquestra PostgreSQL + Django
- `Dockerfile` - Configura container Linux com Django
- `entrypoint.sh` - Script que aguarda DB e executa migrações
- `.dockerignore` - Otimiza build ignorando arquivos desnecessários

## 💡 Vantagens da configuração Docker

✅ **Sem problemas de psycopg2 no Windows**
✅ **PostgreSQL real (não SQLite)**
✅ **Ambiente idêntico entre desenvolvedores**
✅ **Fácil deploy para produção**
✅ **Isolamento de dependências**
✅ **Superuser criado automaticamente**

## 🔄 Alternando entre Docker e desenvolvimento local

### Para usar Docker:
- Execute `docker-compose up`
- O sistema usará PostgreSQL automaticamente

### Para usar desenvolvimento local:
- Pare o Docker: `docker-compose down`
- Ative o venv: `.venv\Scripts\Activate.ps1`
- Execute: `python manage.py runserver`
- O sistema usará SQLite automaticamente

## 🚨 Troubleshooting

### Docker não inicia
```bash
# Reconstruir containers
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Erro de porta já em uso
```bash
# Verificar se há processos usando a porta 8000
netstat -ano | findstr :8000

# Matar processo se necessário
taskkill /PID <numero_do_pid> /F
```

### Problemas com banco de dados
```bash
# Resetar banco de dados (⚠️ apaga todos os dados)
docker-compose down -v
docker-compose up --build
``` 
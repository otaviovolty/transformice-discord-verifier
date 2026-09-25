# 🚀 Guia de Deploy - Deixar o Bot Ativo 24/7

## Opção 1: Heroku (Recomendado para Iniciantes)

### Passo 1: Preparar o Projeto

1. Crie uma conta em [Heroku](https://www.heroku.com)
2. Instale o [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. Crie um arquivo `Procfile` na raiz do projeto:

```
worker: python bot.py
```

4. Crie um arquivo `runtime.txt` na raiz:

```
python-3.11.0
```

### Passo 2: Deploy no Heroku

```bash
# Login no Heroku
heroku login

# Crie uma app no Heroku
heroku create seu-app-nome

# Configure as variáveis de ambiente
heroku config:set DISCORD_TOKEN=seu_novo_token_aqui
heroku config:set GUILD_ID=seu_guild_id
heroku config:set VERIFIED_ROLE_ID=id_da_role
heroku config:set VERIFICATION_CHANNEL_ID=id_do_canal

# Deploy
git push heroku main

# Ative o worker dyno
heroku ps:scale worker=1

# Veja os logs
heroku logs --tail
```

## Opção 2: Replit (Mais Fácil)

### Passo 1: Setup no Replit

1. Acesse [Replit](https://replit.com)
2. Clique em "Create Repl"
3. Selecione "Import from GitHub"
4. Cole: `https://github.com/otaviovolty/transformice-discord-verifier`

### Passo 2: Configurar

1. Clique em "Secrets" (chave 🔑) na sidebar esquerda
2. Adicione as variáveis:
   - `DISCORD_TOKEN` = seu novo token
   - `GUILD_ID` = id do servidor
   - `VERIFIED_ROLE_ID` = id da role
   - `VERIFICATION_CHANNEL_ID` = id do canal

### Passo 3: Executar

```bash
pip install -r requirements.txt
python bot.py
```

## Opção 3: VPS (DigitalOcean, Linode, AWS)

### Passo 1: Conectar via SSH

```bash
ssh root@seu_ip_vps
```

### Passo 2: Instalar Dependências

```bash
apt update && apt upgrade -y
apt install python3 python3-pip git -y

# Clone o repositório
git clone https://github.com/otaviovolty/transformice-discord-verifier.git
cd transformice-discord-verifier

# Instale as dependências
pip3 install -r requirements.txt
```

### Passo 3: Criar .env

```bash
nano .env
```

Adicione:
```env
DISCORD_TOKEN=seu_novo_token_aqui
GUILD_ID=seu_guild_id
VERIFIED_ROLE_ID=id_da_role
VERIFICATION_CHANNEL_ID=id_do_canal
DATABASE_URL=sqlite:///verification.db
```

Salve com `CTRL+X`, depois `Y` e `ENTER`.

### Passo 4: Usar PM2 (Recomendado)

```bash
# Instale PM2
npm install -g pm2

# Inicie o bot
pm2 start bot.py --name "transformice-verifier" --interpreter python3

# Configure para iniciar na boot
pm2 startup
pm2 save

# Veja status
pm2 status

# Ver logs
pm2 logs transformice-verifier
```

## Opção 4: Windows Service (Seu PC)

### Passo 1: Instale o NSSM

1. Baixe [NSSM](https://nssm.cc/download)
2. Extraia em `C:\nssm`

### Passo 2: Configure

```cmd
cd C:\nssm\win64
nssm install TransmiceVerifier "C:\caminho\para\python.exe" "C:\caminho\para\bot.py"
```

### Passo 3: Inicie o Serviço

```cmd
nssm start TransmiceVerifier
```

## ⚠️ Segurança Importante

✅ **Regenere seu Token do Discord**

1. Acesse [Discord Developer Portal](https://discord.com/developers/applications)
2. Selecione sua aplicação
3. Vá para "Bot" → "TOKEN"
4. Clique em "Regenerate"
5. Use este novo token nos comandos acima

**NUNCA compartilhe seu token!**

## 🧪 Testando o Bot

Depois que o bot estiver ativo:

1. No Discord, use `/verify`
2. O bot deve gerar um código
3. Adicione o código ao seu perfil do Transformice
4. Use `/confirm username` para validar
5. Você deve receber a role automaticamente

## 📊 Monitorando o Bot

### Logs importantes:
- Verifique os logs regularmente
- Se o bot desconectar, os logs dirão por quê
- Use essas informações para diagnosticar problemas

### Problemas Comuns:

**Bot não responde**
- Verifique se o token está correto
- Confirme que as permissões estão configuradas
- Reinicie o bot

**Erro de permissão**
- Certifique-se que o bot tem: `Manage Roles`, `Send Messages`, `Embed Links`

**Database locked**
- O bot pode estar rodando em múltiplas instâncias
- Verifique os processos em execução

## 🆘 Suporte

Se algo não funcionar:
1. Verifique os logs
2. Teste localmente primeiro
3. Abra uma [issue](https://github.com/otaviovolty/transformice-discord-verifier/issues)

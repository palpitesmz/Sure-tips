# Sure Tips Predictions

Bot automático que atualiza palpites de futebol usando GitHub Actions.

## Como funciona
- Roda todo dia às 18:40 em Maputo
- Busca dados da API e salva em `dados.json`
- Faz commit automático no repositório

## Configuração
1. Cria um secret no GitHub chamado `API_KEY` com a tua chave da API
2. Garante que o arquivo `update.py` está na raiz do projeto
3. O workflow roda sozinho pelo arquivo `.github/workflows/update.yml`

## Rodar manualmente
Vai em Actions > Update Predictions > Run workflow

## Arquivos principais
- `update.py` - Script que busca e processa os dados
- `dados.json` - Arquivo com os palpites atualizados
- `.github/workflows/update.yml` - Configuração do agendamento

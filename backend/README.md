# AI Film Studio — backend

Backend inicial de pré-produção cinematográfica usando FastAPI e OpenAI Agents SDK.

## Requisitos

- Python 3.11+
- Uma chave da OpenAI API com faturamento/configuração habilitados
- Um modelo disponível para sua conta API

## Instalação no Windows PowerShell

Na raiz do repositório:

```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edite `.env` e informe `OPENAI_API_KEY` e `OPENAI_MODEL`.

## Executar

```powershell
uvicorn app.main:app --reload --port 8000
```

- Saúde: http://localhost:8000/health
- Documentação interativa: http://localhost:8000/docs

## Endpoint inicial

`POST /api/films/plan`

Exemplo de corpo:

```json
{
  "title": "A travessia",
  "premise": "Um curta histórico sobre a travessia do Mar Vermelho.",
  "target_duration_minutes": 3,
  "language": "pt-BR",
  "visual_style": "cinematográfico realista",
  "audience": "público geral",
  "budget_mode": "baixo custo"
}
```

Este MVP gera o plano textual. Ainda não gera clipes nem consome APIs de vídeo. A próxima etapa é ligar o plano ao storyboard, à biblioteca de personagens e aos adaptadores de geração.

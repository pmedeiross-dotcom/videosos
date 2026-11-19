# AI Film Studio — backend local e gratuito

Este backend usa **Ollama** para executar um modelo de linguagem no seu próprio computador. Não usa OpenAI API, não exige chave de API e não gera cobrança por requisição.

## Requisitos

- Windows 10/11
- Python 3.11+
- [Ollama](https://ollama.com/download)
- Modelo local baixado pelo Ollama

Modelo inicial sugerido para computadores com pouca memória: `qwen2.5:3b`. A velocidade dependerá do processador e da memória disponível.

## 1. Instalar e baixar o modelo

Instale o Ollama pelo site oficial. Depois, abra o PowerShell e execute:

```powershell
ollama pull qwen2.5:3b
```

O download do modelo usa internet e ocupa espaço no SSD. Depois de baixado, a inferência roda localmente.

Verifique se o modelo está disponível:

```powershell
ollama list
```

## 2. Preparar o backend

Na raiz do repositório:

```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

O arquivo `.env` já aponta para o Ollama local e não precisa de chave secreta.

## 3. Iniciar

Confirme que o Ollama está em execução e rode:

```powershell
uvicorn app.main:app --reload --port 8000
```

- Saúde: http://localhost:8000/health
- Documentação: http://localhost:8000/docs

## 4. Iniciar o frontend

Na raiz do projeto, crie `.env.local`:

```env
NEXT_PUBLIC_FILM_STUDIO_API_URL=http://localhost:8000
```

Depois:

```powershell
npm install
npm run dev
```

Acesse http://localhost:3000/pt/studio (ou o prefixo de idioma configurado).

## Privacidade e custos

- O texto do briefing é enviado ao Ollama no próprio computador.
- Não é enviada chave de API para terceiros.
- Não há cobrança por token ou por geração.
- O download inicial do modelo requer internet.
- O computador, a energia elétrica e o espaço em disco continuam sendo recursos necessários.

## Limitações

Este estágio gera planejamento textual. Não gera automaticamente vídeos realistas. Geração local de vídeo exige GPU e memória muito superiores às de um notebook básico. O projeto seguirá priorizando ferramentas locais gratuitas e edição com FFmpeg/Remotion, sem integrar serviços pagos como requisito.

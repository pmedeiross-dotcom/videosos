# AI Film Studio — integração inicial

A interface de pré-produção foi adicionada em:

- `/[locale]/studio` (por exemplo, `/pt/studio` ou `/en/studio`).

## Executar localmente

1. Inicie o backend conforme as instruções em [backend/README.md](../backend/README.md).
2. Na raiz do frontend, crie um arquivo `.env.local` (não o versione) com:

```env
NEXT_PUBLIC_FILM_STUDIO_API_URL=http://localhost:8000
```

3. Inicie o Next.js:

```bash
npm install
npm run dev
```

4. Abra `http://localhost:3000/pt/studio` (ou o prefixo de idioma configurado).

A variável `NEXT_PUBLIC_FILM_STUDIO_API_URL` contém somente o endereço público do backend. Nunca coloque `OPENAI_API_KEY` em variáveis `NEXT_PUBLIC_*` ou no frontend.

## Limites desta etapa

A tela envia o briefing para `POST /api/films/plan` e exibe o Markdown retornado. Ainda não cria imagens ou vídeos, não salva projetos no banco do editor e não adiciona cenas à timeline.

# AI Film Studio — arquitetura inicial

## Objetivo

Evoluir o VideoSOS para um estúdio de produção cinematográfica assistido por agentes, usando a API da OpenAI como cérebro de planejamento. A geração de vídeo, imagem e áudio continuará desacoplada e será feita por provedores selecionáveis.

## Estratégia

- Preservar a aplicação VideoSOS existente como interface de geração e edição.
- Desenvolver o backend de orquestração em Python/FastAPI, separado do frontend Next.js.
- Usar OpenAI Agents SDK para coordenar agentes especializados.
- Não chamar provedores de vídeo diretamente a partir do navegador.
- Guardar chaves de API somente no backend/ambiente seguro.
- Manter aprovação humana antes de gerar grandes lotes de cenas ou consumir créditos relevantes.

## Fluxo de produção

1. Briefing: ideia, duração, idioma, público e estilo.
2. Pesquisa e roteiro: premissa, estrutura dramática, cenas e diálogos.
3. Bíblia visual: fichas de personagens, figurino, cenários, paleta e referências.
4. Storyboard: planos, enquadramentos, movimento de câmera e duração estimada.
5. Produção: gerar imagens de referência, clipes, vozes, música e efeitos por adaptadores de provedores.
6. Montagem: organizar os clipes na timeline já existente; usar Remotion/FFmpeg onde fizer sentido.
7. Controle de qualidade: validar continuidade, duração, áudio, legendas e arquivos ausentes.
8. Exportação: renderizar MP4 e registrar custos e proveniência dos ativos.

## Arquitetura

- Frontend: Next.js/React já existente no VideoSOS.
- API de orquestração: Python + FastAPI.
- Agentes: OpenAI Agents SDK (diretor, roteirista, diretor de fotografia, continuidade e editor).
- Contratos: Pydantic/JSON para briefing, cenas, personagens e planos.
- Estado inicial: SQLite em desenvolvimento; PostgreSQL quando houver execução multiusuário.
- Fila futura: Redis + worker para tarefas demoradas.
- Mídia: armazenamento local em desenvolvimento; object storage compatível com S3 em produção.
- Renderização: Remotion e FFmpeg.
- Geração visual: adaptadores para fal.ai, Runware, ComfyUI e outros provedores compatíveis.

## Regras de custo e segurança

- Estimar custo antes de iniciar geração.
- Exigir confirmação antes de executar lotes pagos.
- Permitir modelos locais/gratuitos quando o hardware permitir.
- Nunca expor OPENAI_API_KEY, FAL_KEY ou RUNWARE_API_KEY no frontend.
- Salvar prompts, modelo, parâmetros, custo estimado/real e IDs dos ativos.
- Respeitar licenças dos repositórios e dos modelos integrados.

## Fases

### Fase 1 — MVP de pré-produção
- API FastAPI.
- Agente diretor/roteirista.
- Briefing estruturado.
- Plano de filme com cenas, personagens e planos.
- Persistência simples e testes.

### Fase 2 — Bíblia visual e storyboard
- Fichas persistentes de personagens.
- Referências visuais.
- Storyboard editável e aprovação humana.

### Fase 3 — Geração audiovisual
- Adaptadores de imagem, vídeo, voz e música.
- Orçamento e controle de créditos.
- Retentativas e retomada de tarefas.

### Fase 4 — Montagem e QA
- Integração com timeline VideoSOS.
- Renderização e validação automática.
- Exportação MP4.

### Fase 5 — Autonomia controlada
- Fila de trabalhos.
- Agentes especializados.
- Revisão de cenas e regeneração seletiva.
- Painel de custos e histórico.

## Limites do MVP

A primeira versão não promete gerar um longa-metragem completo gratuitamente. Ela transforma um briefing em um plano de produção estruturado. A geração de vídeo realista depende de modelos, hardware e/ou APIs externas, frequentemente cobrados por uso.

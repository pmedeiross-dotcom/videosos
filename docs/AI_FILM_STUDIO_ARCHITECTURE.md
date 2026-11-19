# AI Film Studio — arquitetura particular, local e sem serviços pagos

## Objetivo

Evoluir o VideoSOS para um estúdio cinematográfico de uso particular, sem monetização, assinaturas, APIs pagas ou dependência obrigatória de serviços em nuvem.

## Regra de projeto

**Nenhuma funcionalidade essencial pode exigir pagamento por uso.** Priorizar execução local, software livre/open source e modelos com pesos disponíveis para download. Não integrar provedores pagos como fal.ai, Runware ou OpenAI API no fluxo padrão. Se existirem integrações antigas no editor, elas não devem ser necessárias para o AI Film Studio.

## Arquitetura local

- Interface: Next.js/React já existente no VideoSOS.
- Orquestração: Python + FastAPI no computador do usuário.
- Modelo de linguagem: Ollama, com modelo local (inicialmente Qwen 2.5 3B).
- Persistência: SQLite e arquivos locais.
- Imagens: ComfyUI com modelos locais compatíveis com o hardware.
- Edição e renderização: FFmpeg e Remotion.
- Áudio: ferramentas locais e bibliotecas open source.
- Vídeo: priorizar montagem de imagens, clipes próprios e movimentos de câmera simulados quando a geração de vídeo local não for viável.

## Pipeline

1. Briefing local.
2. Roteiro e estrutura dramática com LLM local.
3. Bíblia visual de personagens e cenários.
4. Storyboard com imagens de referência.
5. Produção com recursos locais, sem APIs pagas obrigatórias.
6. Montagem de cenas na timeline.
7. Trilha, narração, legendas e efeitos com ferramentas locais.
8. Renderização MP4 via FFmpeg/Remotion.

## Custos e privacidade

- Sem OpenAI API, fal.ai, Runware ou outros serviços pagos no fluxo essencial.
- Sem chaves de API pagas.
- Prompts, roteiros e projetos permanecem no computador.
- Downloads iniciais de modelos podem exigir internet e espaço em disco.
- O uso do computador e energia elétrica não é custo de serviço, mas continua sendo recurso físico.

## Limitação de hardware

A geração de vídeo realista local exige GPU dedicada e memória considerável. Em computadores sem GPU adequada, a produção deve usar imagens, movimento de câmera simulado, clipes próprios e renderização tradicional. Não prometer geração ilimitada de vídeo realista em hardware insuficiente.

## Etapas de desenvolvimento

1. Pré-produção com LLM local.
2. Persistência local de projetos, personagens e cenas.
3. Storyboard e referências visuais.
4. Montagem automática de imagens/clipes usando FFmpeg/Remotion.
5. Integração opcional com ComfyUI para geração de imagens local.
6. Testes e otimização para o hardware disponível.

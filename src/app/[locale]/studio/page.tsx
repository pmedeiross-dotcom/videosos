"use client";

import { useState } from "react";
import Link from "next/link";
import { useLocale } from "next-intl";

type FilmBrief = {
  title: string;
  premise: string;
  target_duration_minutes: number;
  language: string;
  visual_style: string;
  audience: string;
  budget_mode: string;
};

const API_URL = process.env.NEXT_PUBLIC_FILM_STUDIO_API_URL || "http://localhost:8000";

export default function FilmStudioPage() {
  const locale = useLocale();
  const [brief, setBrief] = useState<FilmBrief>({
    title: "",
    premise: "",
    target_duration_minutes: 3,
    language: "pt-BR",
    visual_style: "Cinematográfico realista",
    audience: "Público geral",
    budget_mode: "baixo custo",
  });
  const [plan, setPlan] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function update<K extends keyof FilmBrief>(key: K, value: FilmBrief[K]) {
    setBrief((current) => ({ ...current, [key]: value }));
  }

  async function generatePlan(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setPlan("");

    try {
      const response = await fetch(`${API_URL}/api/films/plan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(brief),
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.detail || `Falha na API (HTTP ${response.status})`);
      }
      setPlan(data.plan_markdown || "A API não retornou um plano.");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Não foi possível conectar ao backend. Verifique se a API está em execução.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-neutral-950 text-neutral-100">
      <header className="border-b border-neutral-800 px-6 py-4">
        <div className="mx-auto flex max-w-6xl items-center justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.28em] text-amber-400">AI Film Studio</p>
            <h1 className="mt-1 text-xl font-semibold">Pré-produção cinematográfica</h1>
          </div>
          <Link href={`/${locale}/app`} className="rounded-lg border border-neutral-700 px-4 py-2 text-sm hover:bg-neutral-800">
            Abrir editor de vídeo
          </Link>
        </div>
      </header>

      <div className="mx-auto grid max-w-6xl gap-8 px-6 py-10 lg:grid-cols-[minmax(0,0.9fr)_minmax(0,1.1fr)]">
        <section>
          <p className="text-sm font-medium text-amber-400">ETAPA 01 · BRIEFING</p>
          <h2 className="mt-3 text-3xl font-semibold tracking-tight">Vamos transformar sua ideia em um filme.</h2>
          <p className="mt-3 leading-7 text-neutral-400">
            Descreva a história. O diretor de IA organizará a proposta em logline,
            sinopse, direção criativa, personagens e cenas. Nesta etapa, o sistema
            produz o planejamento, não os arquivos de vídeo.
          </p>

          <form onSubmit={generatePlan} className="mt-8 space-y-5">
            <div>
              <label htmlFor="title" className="mb-2 block text-sm text-neutral-300">Título provisório</label>
              <input id="title" required minLength={2} maxLength={120} value={brief.title}
                onChange={(e) => update("title", e.target.value)}
                placeholder="Ex.: A última travessia"
                className="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-4 py-3 outline-none focus:border-amber-400" />
            </div>

            <div>
              <label htmlFor="premise" className="mb-2 block text-sm text-neutral-300">Conte a ideia do filme</label>
              <textarea id="premise" required minLength={10} maxLength={6000} rows={7}
                value={brief.premise} onChange={(e) => update("premise", e.target.value)}
                placeholder="Descreva a história, os acontecimentos, o período histórico, os personagens ou a mensagem que deseja transmitir..."
                className="w-full resize-y rounded-xl border border-neutral-700 bg-neutral-900 px-4 py-3 outline-none focus:border-amber-400" />
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <label htmlFor="duration" className="mb-2 block text-sm text-neutral-300">Duração desejada</label>
                <select id="duration" value={brief.target_duration_minutes}
                  onChange={(e) => update("target_duration_minutes", Number(e.target.value))}
                  className="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-4 py-3">
                  {[1, 3, 5, 10, 15, 20, 30].map((n) => <option key={n} value={n}>{n} minuto{n > 1 ? "s" : ""}</option>)}
                </select>
              </div>
              <div>
                <label htmlFor="budget" className="mb-2 block text-sm text-neutral-300">Orçamento de produção</label>
                <select id="budget" value={brief.budget_mode}
                  onChange={(e) => update("budget_mode", e.target.value)}
                  className="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-4 py-3">
                  <option value="gratuito">Priorizar ferramentas gratuitas</option>
                  <option value="baixo custo">Baixo custo</option>
                  <option value="moderado">Moderado</option>
                  <option value="flexível">Flexível, priorizar qualidade</option>
                </select>
              </div>
            </div>

            <div>
              <label htmlFor="style" className="mb-2 block text-sm text-neutral-300">Estilo visual</label>
              <select id="style" value={brief.visual_style}
                onChange={(e) => update("visual_style", e.target.value)}
                className="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-4 py-3">
                <option>Cinematográfico realista</option>
                <option>Épico histórico</option>
                <option>Documentário</option>
                <option>Drama intimista</option>
                <option>Animação 3D</option>
                <option>Fantasia cinematográfica</option>
                <option>Suspense / thriller</option>
              </select>
            </div>

            <div>
              <label htmlFor="audience" className="mb-2 block text-sm text-neutral-300">Público-alvo</label>
              <input id="audience" value={brief.audience}
                onChange={(e) => update("audience", e.target.value)}
                className="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-4 py-3 outline-none focus:border-amber-400" />
            </div>

            <button type="submit" disabled={loading}
              className="w-full rounded-xl bg-amber-400 px-5 py-4 font-semibold text-neutral-950 transition hover:bg-amber-300 disabled:cursor-not-allowed disabled:opacity-60">
              {loading ? "O diretor está desenvolvendo o projeto..." : "Gerar plano cinematográfico"}
            </button>
            <p className="text-xs text-neutral-500">
              A geração utiliza a API configurada no backend e pode gerar cobrança conforme o modelo escolhido.
            </p>
          </form>
        </section>

        <section className="min-h-[520px] rounded-2xl border border-neutral-800 bg-neutral-900/60 p-6">
          <div className="flex items-center justify-between border-b border-neutral-800 pb-4">
            <div>
              <p className="text-xs uppercase tracking-[0.2em] text-neutral-500">Sala de roteiro</p>
              <h2 className="mt-1 text-lg font-semibold">Plano de produção</h2>
            </div>
            <span className="rounded-full border border-neutral-700 px-3 py-1 text-xs text-neutral-400">
              {plan ? "Plano gerado" : loading ? "Em criação" : "Aguardando briefing"}
            </span>
          </div>

          {error && (
            <div role="alert" className="mt-6 rounded-xl border border-red-900 bg-red-950/40 p-4 text-sm text-red-200">
              <strong className="block">Não foi possível gerar o plano</strong>
              <span className="mt-1 block">{error}</span>
              <p className="mt-3 text-red-300/80">Confira se o backend está iniciado, se a chave da OpenAI está configurada e se o endereço da API está correto.</p>
            </div>
          )}

          {!plan && !error && (
            <div className="flex min-h-[390px] flex-col items-center justify-center text-center">
              <div className="mb-5 flex h-16 w-16 items-center justify-center rounded-2xl border border-neutral-700 bg-neutral-800 text-2xl">🎬</div>
              <h3 className="text-lg font-medium">{loading ? "Analisando sua ideia..." : "Seu filme começa aqui"}</h3>
              <p className="mt-2 max-w-sm text-sm leading-6 text-neutral-500">
                {loading
                  ? "O agente está estruturando a narrativa e organizando as cenas. Isso pode levar alguns instantes."
                  : "Depois de enviar o briefing, o plano completo aparecerá nesta área."}
              </p>
            </div>
          )}

          {plan && (
            <article className="prose prose-invert mt-6 max-w-none whitespace-pre-wrap text-sm leading-7">
              {plan}
            </article>
          )}
        </section>
      </div>
    </main>
  );
}

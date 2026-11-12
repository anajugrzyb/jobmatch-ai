"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type Job = {
  id: number; title: string; company: string; source: string;
  source_url: string | null; description: string | null;
  location: string; remote: boolean; tags: string;
  published_at: string | null;
};
type Source = "remotive" | "arbeitnow";

export default function JobsPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [query, setQuery] = useState("");
  const [location, setLocation] = useState("");
  const [remoteOnly, setRemoteOnly] = useState(false);
  const [source, setSource] = useState<Source>("remotive");
  const [status, setStatus] = useState("Carregando vagas locais...");
  const [loading, setLoading] = useState(false);
  const [offset, setOffset] = useState(0);
  const limit = 20;

  const search = useCallback(async (nextOffset: number) => {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        q: query, location, remote_only: String(remoteOnly),
        limit: String(limit), offset: String(nextOffset),
      });
      const res = await fetch(`${API}/api/v1/jobs?${params}`);
      if (!res.ok) throw new Error("Falha ao consultar vagas no banco local.");
      const data = await res.json() as Job[];
      setJobs(data);
      setOffset(nextOffset);
      setStatus(`${data.length} vaga(s) nesta página. Importe uma fonte para atualizar.`);
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Erro inesperado.");
    } finally {
      setLoading(false);
    }
  }, [query, location, remoteOnly]);

  useEffect(() => {
    // Carrega a primeira página ao abrir a tela, sem importar fontes externas.
    const controller = new AbortController();
    fetch(`${API}/api/v1/jobs?limit=20`, { signal: controller.signal })
      .then(async (res) => {
        if (!res.ok) throw new Error("API indisponível.");
        return await res.json() as Job[];
      })
      .then((data) => { setJobs(data); setStatus(`${data.length} vaga(s) nesta página.`); })
      .catch((error: unknown) => {
        if (error instanceof Error && error.name === "AbortError") return;
        setStatus("API indisponível. Confira o Docker.");
      });
    return () => controller.abort();
  }, []);

  async function importJobs() {
    setLoading(true);
    setStatus("Consultando API pública...");
    try {
      const res = await fetch(`${API}/api/v1/jobs/import`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source, query: source === "remotive" ? query : "" }),
      });
      const data = await res.json() as {
        fetched?: number; inserted?: number; updated?: number; detail?: string
      };
      if (!res.ok) throw new Error(data.detail ?? "Não foi possível importar.");
      const params = new URLSearchParams({
        q: query, location, remote_only: String(remoteOnly), limit: String(limit), offset: "0",
      });
      const searchRes = await fetch(`${API}/api/v1/jobs?${params}`);
      if (!searchRes.ok) throw new Error("Importação concluída, mas a listagem falhou.");
      setJobs(await searchRes.json() as Job[]);
      setOffset(0);
      setStatus(`Importação concluída: ${data.inserted} nova(s), ${data.updated} atualizada(s), ${data.fetched} recebida(s).`);
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Erro inesperado.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-5xl px-5 py-12">
      <Link href="/" className="text-sm text-cyan-400 hover:underline">← Voltar ao perfil</Link>
      <p className="mt-8 text-sm font-semibold tracking-widest text-cyan-400">SEMANA 03 · OPORTUNIDADES</p>
      <h1 className="mt-2 text-4xl font-bold">Buscar vagas</h1>
      <p className="mt-3 text-slate-300">Importe oportunidades de fontes públicas e filtre as vagas salvas no seu banco local.</p>
      <p className="mt-3 text-sm text-amber-200">Apenas para uso local. Confirme detalhes e disponibilidade no site da vaga.</p>

      <section className="mt-8 rounded-xl border border-slate-700 bg-slate-900 p-5">
        <h2 className="text-xl font-semibold">Importar oportunidades</h2>
        <div className="mt-4 flex flex-wrap items-end gap-3">
          <label className="text-sm">Fonte
            <select value={source} onChange={(event) => setSource(event.target.value as Source)}
              className="mt-2 block rounded-lg border border-slate-600 bg-slate-950 p-3">
              <option value="remotive">Remotive (remotas)</option>
              <option value="arbeitnow">Arbeitnow</option>
            </select>
          </label>
          <button disabled={loading} onClick={() => void importJobs()}
            className="rounded-lg bg-cyan-400 px-5 py-3 font-semibold text-slate-950 disabled:opacity-50">
            Importar vagas
          </button>
        </div>
        <p className="mt-3 text-xs text-slate-400">Remotive usa o termo de busca na fonte; Arbeitnow importa a primeira página e filtra localmente.</p>
      </section>

      <section className="mt-6 rounded-xl border border-slate-700 bg-slate-900 p-5">
        <h2 className="text-xl font-semibold">Filtros locais</h2>
        <form onSubmit={(event) => { event.preventDefault(); void search(0); }}
          className="mt-4 flex flex-wrap items-end gap-3">
          <label className="flex-1 text-sm">Cargo, empresa ou tecnologia
            <input value={query} onChange={(event) => setQuery(event.target.value)} maxLength={100}
              placeholder="Ex.: Python, Data Analyst" className="mt-2 block w-full rounded-lg border border-slate-600 bg-slate-950 p-3"/>
          </label>
          <label className="flex-1 text-sm">Localização
            <input value={location} onChange={(event) => setLocation(event.target.value)} maxLength={100}
              placeholder="Ex.: Brazil, Worldwide" className="mt-2 block w-full rounded-lg border border-slate-600 bg-slate-950 p-3"/>
          </label>
          <label className="flex items-center gap-2 text-sm">
            <input type="checkbox" checked={remoteOnly} onChange={(event) => setRemoteOnly(event.target.checked)}/>
            Apenas remotas
          </label>
          <button disabled={loading} type="submit" className="rounded-lg border border-cyan-400 px-5 py-3 font-semibold text-cyan-300 disabled:opacity-50">Pesquisar</button>
        </form>
      </section>

      <p role="status" aria-live="polite" className="my-6 text-cyan-300">{status}</p>
      <div className="space-y-4">
        {jobs.map((job) => (
          <article key={job.id} className="rounded-xl border border-slate-700 bg-slate-900 p-5">
            <div className="flex flex-wrap justify-between gap-3">
              <div><h3 className="text-lg font-semibold">{job.title}</h3>
                <p className="text-slate-300">{job.company} · {job.location || "Localização não informada"}</p>
              </div>
              <span className="text-sm text-cyan-300">{job.remote ? "Remota" : "Modalidade não confirmada"} · {job.source}</span>
            </div>
            {job.tags && <p className="mt-3 text-sm text-slate-400">{job.tags}</p>}
            {job.description && <p className="mt-3 line-clamp-3 text-sm text-slate-300">{job.description}</p>}
            {job.source_url && <a href={job.source_url} target="_blank" rel="noopener noreferrer"
              className="mt-4 inline-block text-sm font-semibold text-cyan-400 hover:underline">Ver vaga original ↗</a>}
          </article>
        ))}
      </div>
      <div className="mt-7 flex items-center gap-4">
        <button disabled={loading || offset === 0} onClick={() => void search(Math.max(0, offset - limit))}
          className="rounded-lg border border-slate-600 px-4 py-2 disabled:opacity-40">Anterior</button>
        <span className="text-sm text-slate-300">Página {Math.floor(offset / limit) + 1}</span>
        <button disabled={loading || jobs.length < limit} onClick={() => void search(offset + limit)}
          className="rounded-lg border border-slate-600 px-4 py-2 disabled:opacity-40">Próxima</button>
      </div>
    </main>
  );
}

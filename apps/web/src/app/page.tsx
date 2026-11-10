"use client";
import { useEffect, useState } from "react";

type Health = { status: string; service: string };
export default function Home() {
  const [health, setHealth] = useState("Verificando...");
  useEffect(() => {
    const controller = new AbortController();
    fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/api/v1/health`, { signal: controller.signal })
      .then(async (res) => { if (!res.ok) throw new Error("API indisponível"); return res.json() as Promise<Health>; })
      .then((data) => setHealth(data.status === "ok" ? "API conectada" : "API indisponível"))
      .catch((err: unknown) => { if (!(err instanceof DOMException && err.name === "AbortError")) setHealth("API indisponível"); });
    return () => controller.abort();
  }, []);
  return <main className="mx-auto max-w-4xl px-6 py-20">
    <p className="mb-3 text-sm font-semibold tracking-widest text-cyan-400">SEMANA 01 · FUNDAÇÃO</p>
    <h1 className="text-5xl font-bold tracking-tight">JobMatch <span className="text-cyan-400">AI</span></h1>
    <p className="mt-5 max-w-2xl text-lg text-slate-300">Seu assistente de candidaturas: descubra oportunidades, avalie compatibilidade e aprove currículos personalizados.</p>
    <section className="mt-10 rounded-2xl border border-slate-700 bg-slate-900 p-6">
      <h2 className="text-xl font-semibold">Status do ambiente</h2>
      <p role="status" className="mt-3 text-cyan-300">{health}</p>
      <p className="mt-3 text-sm text-slate-400">Nesta primeira entrega, o painel valida a comunicação entre frontend e backend.</p>
      <a className="mt-5 inline-block rounded-lg bg-cyan-500 px-4 py-2 font-semibold text-slate-950" href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer">Abrir documentação da API</a>
    </section>
  </main>;
}

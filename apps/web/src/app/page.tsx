"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type Profile = {
  full_name: string; headline: string; location: string; email: string;
  skills: string; experience: string; education: string;
};
const emptyProfile: Profile = {
  full_name: "", headline: "", location: "", email: "",
  skills: "", experience: "", education: "",
};
type Field = { key: keyof Profile; label: string; multiline?: boolean; placeholder?: string };
const fields: Field[] = [
  { key: "full_name", label: "Nome completo", placeholder: "Seu nome" },
  { key: "headline", label: "Título profissional", placeholder: "Ex.: Analista de Dados" },
  { key: "location", label: "Localização", placeholder: "Ex.: São Paulo, SP" },
  { key: "email", label: "E-mail", placeholder: "voce@exemplo.com" },
  { key: "skills", label: "Habilidades", multiline: true, placeholder: "Python, SQL, Git..." },
  { key: "experience", label: "Experiências", multiline: true, placeholder: "Descreva experiências reais" },
  { key: "education", label: "Formação", multiline: true, placeholder: "Cursos, graduações e certificações" },
];

export default function Home() {
  const [profile, setProfile] = useState<Profile>(emptyProfile);
  const [resumeText, setResumeText] = useState("");
  const [status, setStatus] = useState("Carregando perfil...");
  const [busy, setBusy] = useState(false);
  const [pages, setPages] = useState<number | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    fetch(`${API}/api/v1/profile`, { signal: controller.signal })
      .then(async (res) => {
        if (!res.ok) throw new Error("Falha ao carregar perfil");
        return (await res.json()) as Profile | null;
      })
      .then((data) => {
        if (data) setProfile({
          full_name: data.full_name, headline: data.headline, location: data.location,
          email: data.email, skills: data.skills, experience: data.experience,
          education: data.education,
        });
        setStatus(data ? "Perfil carregado." : "Preencha seu primeiro perfil.");
      })
      .catch((error: unknown) => {
        if (error instanceof Error && error.name === "AbortError") return;
        setStatus("API indisponível. Confira os contêineres.");
      });
    return () => controller.abort();
  }, []);

  async function saveProfile(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    setStatus("Salvando...");
    try {
      const res = await fetch(`${API}/api/v1/profile`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(profile),
      });
      if (!res.ok) throw new Error("Falha ao salvar. Verifique os campos.");
      setStatus("Perfil salvo no banco de dados local.");
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Erro inesperado.");
    } finally {
      setBusy(false);
    }
  }

  async function uploadResume(file: File | undefined) {
    if (!file) return;
    if (file.size > 5 * 1024 * 1024 || !file.name.toLowerCase().endsWith(".pdf")) {
      setStatus("Escolha um PDF de até 5 MB.");
      return;
    }
    setBusy(true);
    setStatus("Extraindo texto do currículo...");
    const body = new FormData();
    body.append("file", file);
    try {
      const res = await fetch(`${API}/api/v1/resume/extract`, { method: "POST", body });
      const data = await res.json() as { text?: string; pages?: number; truncated?: boolean; detail?: string };
      if (!res.ok) throw new Error(data.detail ?? "Falha ao ler PDF.");
      setResumeText(data.text ?? "");
      setPages(data.pages ?? null);
      setStatus(data.truncated
        ? "Texto extraído parcialmente (limite de 30 mil caracteres). Revise antes de usar."
        : "Texto extraído. Revise e copie as informações relevantes para o perfil.");
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Erro inesperado.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="mx-auto max-w-5xl px-5 py-12">
      <p className="mb-2 text-sm font-semibold tracking-widest text-cyan-400">JOBMATCH AI · PERFIL PROFISSIONAL</p>
      <h1 className="text-4xl font-bold">JobMatch <span className="text-cyan-400">AI</span></h1>
      <p className="mt-4 text-slate-300">Cadastre suas informações reais e revise o texto extraído do currículo antes de salvar.</p>
      <Link href="/jobs" className="mt-5 inline-block rounded-lg bg-cyan-400 px-5 py-3 font-semibold text-slate-950">Buscar vagas →</Link>
      <p className="mt-5 rounded-lg border border-amber-700 bg-amber-950/30 p-3 text-sm text-amber-200">
        MVP local de usuário único, sem autenticação. Não publique esta API na internet nem utilize dados sensíveis.
      </p>
      <p role="status" aria-live="polite" className="mt-5 text-cyan-300">{status}</p>
      <div className="mt-8 grid gap-8 lg:grid-cols-2">
        <section className="rounded-xl border border-slate-700 bg-slate-900 p-6">
          <h2 className="text-2xl font-semibold">Seu perfil</h2>
          <form onSubmit={saveProfile} className="mt-5 space-y-4">
            {fields.map((field) => (
              <label key={field.key} className="block text-sm font-medium">
                <span>{field.label}</span>
                {field.multiline ? (
                  <textarea
                    value={profile[field.key]}
                    onChange={(event) => setProfile((prev) => ({ ...prev, [field.key]: event.target.value }))}
                    placeholder={field.placeholder}
                    rows={4}
                    className="mt-2 w-full rounded-lg border border-slate-600 bg-slate-950 p-3 text-white"
                  />
                ) : (
                  <input
                    type={field.key === "email" ? "email" : "text"}
                    value={profile[field.key]}
                    onChange={(event) => setProfile((prev) => ({ ...prev, [field.key]: event.target.value }))}
                    placeholder={field.placeholder}
                    className="mt-2 w-full rounded-lg border border-slate-600 bg-slate-950 p-3 text-white"
                  />
                )}
              </label>
            ))}
            <button disabled={busy} className="rounded-lg bg-cyan-400 px-5 py-3 font-semibold text-slate-950 disabled:opacity-50">
              Salvar perfil
            </button>
          </form>
        </section>
        <section className="h-fit rounded-xl border border-slate-700 bg-slate-900 p-6">
          <h2 className="text-2xl font-semibold">Ler currículo em PDF</h2>
          <p className="mt-3 text-sm text-slate-300">PDF de até 5 MB e 20 páginas, com texto selecionável. O arquivo não é armazenado.</p>
          <label className="mt-5 block text-sm font-medium">
            Escolher currículo
            <input
              type="file"
              accept=".pdf,application/pdf"
              disabled={busy}
              onChange={(event) => {
                void uploadResume(event.target.files?.[0]);
                event.target.value = "";
              }}
              className="mt-2 block w-full text-sm text-slate-200 file:mr-3 file:rounded-lg file:border-0 file:bg-cyan-400 file:px-3 file:py-2 file:font-semibold file:text-slate-950"
            />
          </label>
          {pages !== null && <p className="mt-4 text-sm text-slate-400">{pages} página(s) processada(s)</p>}
          {resumeText && (
            <label className="mt-5 block text-sm font-medium">
              Texto extraído (revise antes de copiar)
              <textarea
                readOnly
                value={resumeText}
                rows={18}
                className="mt-2 w-full rounded-lg border border-slate-600 bg-slate-950 p-3 text-sm text-slate-200"
              />
            </label>
          )}
          <p className="mt-4 text-xs text-slate-400">Nesta etapa, a extração não preenche nem salva o perfil automaticamente.</p>
        </section>
      </div>
    </main>
  );
}

"use client";

import LoadingState from "@/components/workspace/LoadingState";
import PaperCard from "@/components/workspace/PaperCard";
import WorkspaceHeader from "@/components/workspace/WorkspaceHeader";
import { deleteProject, getProject, listSavedPapers, removePaper, savePaper, searchPapers, updateProject } from "@/lib/api";
import type { ApiError, Paper, Project, SavedPaper } from "@/lib/types";
import { useAuth } from "@clerk/nextjs";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { FormEvent, useEffect, useState } from "react";

export default function ProjectPage() {
  const { getToken, isLoaded, isSignedIn } = useAuth();
  const router = useRouter();
  const params = useParams<{ projectId: string }>();
  const projectId = params.projectId;
  const [project, setProject] = useState<Project | null>(null);
  const [savedPapers, setSavedPapers] = useState<SavedPaper[]>([]);
  const [results, setResults] = useState<Paper[]>([]);
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isSearching, setIsSearching] = useState(false);
  const [busyPaperId, setBusyPaperId] = useState("");
  const [error, setError] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState("");
  const [editQuestion, setEditQuestion] = useState("");
  const [isSavingProject, setIsSavingProject] = useState(false);
  const [isDeletingProject, setIsDeletingProject] = useState(false);

  useEffect(() => {
    if (isLoaded && !isSignedIn) {
      router.replace("/auth/sign-in");
      return;
    }
    if (!isLoaded || !isSignedIn) return;

    async function loadProject() {
      try {
        const token = await getToken();
        const [loadedProject, loadedPapers] = await Promise.all([
          getProject(token, projectId),
          listSavedPapers(token, projectId),
        ]);
        setProject(loadedProject);
        setEditTitle(loadedProject.title);
        setEditQuestion(loadedProject.question);
        setSavedPapers(loadedPapers);
      } catch (loadError) {
        setError((loadError as ApiError).message ?? "Could not load this project.");
      } finally {
        setIsLoading(false);
      }
    }
    void loadProject();
  }, [getToken, isLoaded, isSignedIn, projectId, router]);

  async function handleSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!query.trim()) return;
    setIsSearching(true);
    setError("");
    try {
      const token = await getToken();
      setResults(await searchPapers(token, query.trim()));
    } catch (searchError) {
      setError((searchError as ApiError).message ?? "Search failed.");
    } finally {
      setIsSearching(false);
    }
  }

  async function handleSave(paper: Paper) {
    setBusyPaperId(paper.id);
    try {
      const token = await getToken();
      const saved = await savePaper(token, projectId, paper);
      setSavedPapers((current) => current.some((item) => item.id === saved.id) ? current : [...current, saved]);
    } catch (saveError) {
      setError((saveError as ApiError).message ?? "Could not save paper.");
    } finally {
      setBusyPaperId("");
    }
  }

  async function handleRemove(paper: SavedPaper) {
    setBusyPaperId(paper.id);
    try {
      const token = await getToken();
      await removePaper(token, projectId, paper.id);
      setSavedPapers((current) => current.filter((item) => item.id !== paper.id));
    } catch (removeError) {
      setError((removeError as ApiError).message ?? "Could not remove paper.");
    } finally {
      setBusyPaperId("");
    }
  }

  async function handleUpdateProject(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!editTitle.trim() || !editQuestion.trim()) {
      setError("Add a project title and research question.");
      return;
    }

    setIsSavingProject(true);
    setError("");
    try {
      const token = await getToken();
      const updatedProject = await updateProject(token, projectId, {
        title: editTitle.trim(),
        question: editQuestion.trim(),
      });
      setProject(updatedProject);
      setEditTitle(updatedProject.title);
      setEditQuestion(updatedProject.question);
      setIsEditing(false);
    } catch (updateError) {
      setError((updateError as ApiError).message ?? "Could not update this project.");
    } finally {
      setIsSavingProject(false);
    }
  }

  async function handleDeleteProject() {
    if (!project || !window.confirm(`Delete "${project.title}"? This cannot be undone.`)) return;

    setIsDeletingProject(true);
    setError("");
    try {
      const token = await getToken();
      await deleteProject(token, projectId);
      router.replace("/dashboard");
    } catch (deleteError) {
      setError((deleteError as ApiError).message ?? "Could not delete this project.");
      setIsDeletingProject(false);
    }
  }

  if (!isLoaded || !isSignedIn || isLoading) return <LoadingState label="Opening project" />;

  return (
    <div className="min-h-screen bg-[#f5f7f8] text-slate-950">
      <WorkspaceHeader />
      <main className="mx-auto max-w-6xl px-6 py-10">
        <Link href="/dashboard" className="text-sm font-semibold text-cyan-700 hover:text-cyan-900">← All projects</Link>
        {error && <div className="mt-6 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-800">{error}</div>}
        {project && (
          <div className="mt-8">
            {isEditing ? (
              <form onSubmit={handleUpdateProject} className="max-w-3xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <p className="text-xs font-semibold uppercase tracking-[0.18em] text-cyan-700">Edit project</p>
                <label className="mt-5 block text-sm font-medium text-slate-700">
                  Project title
                  <input value={editTitle} onChange={(event) => setEditTitle(event.target.value)} className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2.5 font-normal outline-none focus:border-cyan-600 focus:ring-2 focus:ring-cyan-100" />
                </label>
                <label className="mt-5 block text-sm font-medium text-slate-700">
                  Research question
                  <textarea value={editQuestion} onChange={(event) => setEditQuestion(event.target.value)} rows={4} className="mt-2 w-full resize-none rounded-lg border border-slate-300 px-3 py-2.5 font-normal outline-none focus:border-cyan-600 focus:ring-2 focus:ring-cyan-100" />
                </label>
                <div className="mt-5 flex gap-3">
                  <button type="submit" disabled={isSavingProject} className="rounded-lg bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white hover:bg-cyan-800 disabled:cursor-not-allowed disabled:opacity-50">{isSavingProject ? "Saving..." : "Save changes"}</button>
                  <button type="button" onClick={() => { setEditTitle(project.title); setEditQuestion(project.question); setIsEditing(false); }} className="px-4 py-2.5 text-sm font-semibold text-slate-600 hover:text-slate-950">Cancel</button>
                </div>
              </form>
            ) : (
              <div className="max-w-3xl">
                <span className="rounded-full bg-cyan-50 px-2.5 py-1 text-xs font-semibold capitalize text-cyan-800">{project.status}</span>
                <div className="mt-4 flex items-start justify-between gap-4">
                  <h1 className="text-4xl font-semibold tracking-tight">{project.title}</h1>
                  <div className="flex shrink-0 gap-2">
                    <button type="button" onClick={() => setIsEditing(true)} disabled={isDeletingProject} className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-semibold text-slate-700 hover:border-cyan-600 hover:text-cyan-800 disabled:cursor-not-allowed disabled:opacity-50">Edit project</button>
                    <button type="button" onClick={() => void handleDeleteProject()} disabled={isDeletingProject} className="rounded-lg border border-rose-200 px-3 py-2 text-sm font-semibold text-rose-700 hover:border-rose-400 hover:bg-rose-50 disabled:cursor-not-allowed disabled:opacity-50">{isDeletingProject ? "Deleting..." : "Delete project"}</button>
                  </div>
                </div>
                <p className="mt-4 text-lg leading-8 text-slate-600">{project.question}</p>
              </div>
            )}

            <div className="mt-10 grid gap-8 lg:grid-cols-[minmax(0,1.35fr)_minmax(300px,0.65fr)]">
              <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <p className="text-xs font-semibold uppercase tracking-[0.18em] text-cyan-700">Research</p>
                <h2 className="mt-2 text-xl font-semibold">Find academic papers</h2>
                <form onSubmit={handleSearch} className="mt-5 flex gap-3">
                  <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search by topic or question" className="min-w-0 flex-1 rounded-lg border border-slate-300 px-3 py-2.5 outline-none focus:border-cyan-600 focus:ring-2 focus:ring-cyan-100" />
                  <button type="submit" disabled={isSearching || !query.trim()} className="rounded-lg bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white hover:bg-cyan-800 disabled:cursor-not-allowed disabled:opacity-50">{isSearching ? "Searching..." : "Search"}</button>
                </form>
                <div className="mt-5">
                  {results.length === 0 ? <p className="py-8 text-sm text-slate-500">Search results will appear here.</p> : results.map((paper) => <PaperCard key={paper.id} paper={paper} actionLabel={savedPapers.some((item) => item.openalex_id === paper.openalex_id) ? "Saved" : "Save"} onAction={() => void handleSave(paper)} disabled={busyPaperId === paper.id || savedPapers.some((item) => item.openalex_id === paper.openalex_id)} />)}
                </div>
              </section>

              <aside className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <p className="text-xs font-semibold uppercase tracking-[0.18em] text-cyan-700">Collection</p>
                <h2 className="mt-2 text-xl font-semibold">Saved papers <span className="text-slate-400">{savedPapers.length}</span></h2>
                <div className="mt-5">
                  {savedPapers.length === 0 ? <p className="py-8 text-sm leading-6 text-slate-500">Save useful papers from your search results to build the evidence base for this project.</p> : savedPapers.map((paper) => <PaperCard key={paper.id} paper={paper} actionLabel="Remove" onAction={() => void handleRemove(paper)} disabled={busyPaperId === paper.id} />)}
                </div>
              </aside>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

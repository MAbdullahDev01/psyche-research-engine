"use client";

import LoadingState from "@/components/workspace/LoadingState";
import ProjectCard from "@/components/workspace/ProjectCard";
import ProjectForm from "@/components/workspace/ProjectForm";
import WorkspaceHeader from "@/components/workspace/WorkspaceHeader";
import { createProject, listProjects } from "@/lib/api";
import type { ApiError, CreateProjectInput, Project } from "@/lib/types";
import { useAuth } from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

export default function DashboardPage() {
  const { getToken, isLoaded, isSignedIn } = useAuth();
  const router = useRouter();
  const [projects, setProjects] = useState<Project[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);

  const loadProjects = useCallback(async () => {
    setError("");
    try {
      const token = await getToken();
      setProjects(await listProjects(token));
    } catch (loadError) {
      setError((loadError as ApiError).message ?? "Could not load projects.");
    } finally {
      setIsLoading(false);
    }
  }, [getToken]);

  useEffect(() => {
    if (isLoaded && !isSignedIn) {
      router.replace("/auth/sign-in");
      return;
    }
    if (isLoaded && isSignedIn) queueMicrotask(() => void loadProjects());
  }, [isLoaded, isSignedIn, loadProjects, router]);

  async function handleCreate(input: CreateProjectInput) {
    const token = await getToken();
    const project = await createProject(token, input);
    router.push(`/dashboard/projects/${project.id}`);
  }

  if (!isLoaded || !isSignedIn) {
    return <LoadingState label="Preparing your workspace" />;
  }

  return (
    <div className="min-h-screen bg-[#f5f7f8] text-slate-950">
      <WorkspaceHeader />
      <main className="mx-auto max-w-6xl px-6 py-12">
        <div className="flex flex-col justify-between gap-6 sm:flex-row sm:items-end">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.18em] text-cyan-700">Research workspace</p>
            <h1 className="mt-3 text-4xl font-semibold tracking-tight">Your projects</h1>
            <p className="mt-3 max-w-xl text-base leading-7 text-slate-600">
              Start with a question, gather the literature, and shape the evidence into something useful.
            </p>
          </div>
          <button
            type="button"
            onClick={() => setShowForm((visible) => !visible)}
            className="rounded-lg bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-cyan-800"
          >
            {showForm ? "Close form" : "New project"}
          </button>
        </div>

        {showForm && (
          <div className="mt-8 max-w-2xl">
            <ProjectForm onSubmit={handleCreate} onCancel={() => setShowForm(false)} />
          </div>
        )}

        {error && (
          <div className="mt-8 flex items-center justify-between rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-800">
            <span>{error}</span>
            <button type="button" onClick={() => { setIsLoading(true); void loadProjects(); }} className="font-semibold underline">Retry</button>
          </div>
        )}

        <section className="mt-10">
          {isLoading ? <LoadingState label="Loading projects" /> : projects.length === 0 ? (
            <div className="rounded-2xl border border-dashed border-slate-300 bg-white px-6 py-16 text-center">
              <h2 className="text-lg font-semibold">Your first question starts here.</h2>
              <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-600">Create a project to give your research a home.</p>
            </div>
          ) : (
            <div className="grid gap-5 md:grid-cols-2">
              {projects.map((project) => <ProjectCard key={project.id} project={project} />)}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

"use client";

import type { CreateProjectInput } from "@/lib/types";
import { FormEvent, useState } from "react";

type ProjectFormProps = {
  onSubmit: (input: CreateProjectInput) => Promise<void>;
  onCancel?: () => void;
};

export default function ProjectForm({ onSubmit, onCancel }: ProjectFormProps) {
  const [title, setTitle] = useState("");
  const [question, setQuestion] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!title.trim() || !question.trim()) {
      setError("Add a project title and research question.");
      return;
    }

    setError("");
    setIsSubmitting(true);
    try {
      await onSubmit({ title: title.trim(), research_question: question.trim() });
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Could not create project.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-cyan-700">New project</p>
        <h2 className="mt-2 text-xl font-semibold text-slate-950">Frame your question</h2>
      </div>
      <label className="block text-sm font-medium text-slate-700">
        Project title
        <input
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          placeholder="Sleep and academic performance"
          className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2.5 font-normal outline-none transition focus:border-cyan-600 focus:ring-2 focus:ring-cyan-100"
        />
      </label>
      <label className="block text-sm font-medium text-slate-700">
        Research question
        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="How does sleep quality affect university students?"
          rows={4}
          className="mt-2 w-full resize-none rounded-lg border border-slate-300 px-3 py-2.5 font-normal outline-none transition focus:border-cyan-600 focus:ring-2 focus:ring-cyan-100"
        />
      </label>
      {error && <p className="text-sm text-rose-700">{error}</p>}
      <div className="flex gap-3">
        <button
          type="submit"
          disabled={isSubmitting}
          className="rounded-lg bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-cyan-800 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isSubmitting ? "Creating..." : "Create project"}
        </button>
        {onCancel && (
          <button type="button" onClick={onCancel} className="px-4 py-2.5 text-sm font-semibold text-slate-600 hover:text-slate-950">
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}

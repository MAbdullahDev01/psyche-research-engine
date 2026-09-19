import type { Project } from "@/lib/types";
import Link from "next/link";

export default function ProjectCard({ project }: { project: Project }) {
  return (
    <Link
      href={`/dashboard/projects/${project.id}`}
      className="group block rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:border-cyan-500 hover:shadow-md"
    >
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="font-semibold text-slate-950 group-hover:text-cyan-800">{project.title}</h2>
          <p className="mt-2 line-clamp-2 text-sm leading-6 text-slate-600">{project.research_question}</p>
        </div>
        <span className="rounded-full bg-cyan-50 px-2.5 py-1 text-xs font-semibold capitalize text-cyan-800">
          {project.status}
        </span>
      </div>
      <p className="mt-5 text-xs text-slate-400">
        Updated {new Date(project.updated_at).toLocaleDateString()}
      </p>
    </Link>
  );
}

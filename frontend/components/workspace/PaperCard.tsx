import type { Paper, SavedPaper } from "@/lib/types";

type PaperCardProps = {
  paper: Paper | SavedPaper;
  actionLabel: string;
  onAction: () => void;
  disabled?: boolean;
};

export default function PaperCard({ paper, actionLabel, onAction, disabled }: PaperCardProps) {
  return (
    <article className="border-b border-slate-200 py-5 last:border-b-0">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <h3 className="font-semibold leading-6 text-slate-950">{paper.title}</h3>
          <p className="mt-1 text-sm text-slate-500">
            {paper.authors.join(", ") || "Unknown authors"}
            {paper.publication_year ? ` · ${paper.publication_year}` : ""}
          </p>
        </div>
        <button
          type="button"
          onClick={onAction}
          disabled={disabled}
          className="shrink-0 rounded-lg border border-slate-300 px-3 py-2 text-xs font-semibold text-slate-700 transition hover:border-cyan-600 hover:text-cyan-800 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {actionLabel}
        </button>
      </div>
      {paper.abstract && <p className="mt-3 text-sm leading-6 text-slate-600">{paper.abstract}</p>}
      {paper.landing_page_url && (
        <a
          href={paper.landing_page_url}
          target="_blank"
          rel="noreferrer"
          className="mt-3 inline-block text-xs font-semibold text-cyan-700 hover:text-cyan-900"
        >
          View source
        </a>
      )}
    </article>
  );
}

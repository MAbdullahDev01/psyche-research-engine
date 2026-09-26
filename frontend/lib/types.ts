export type ProjectStatus = "draft" | "active" | "completed";

export type PaperType =
  | "article"
  | "book"
  | "book-chapter"
  | "dataset"
  | "dissertation"
  | "editorial"
  | "letter"
  | "paratext"
  | "preprint"
  | "review"
  | "reference-entry"
  | "report"
  | "standard";

export type Project = {
  id: string;
  title: string;
  question: string;
  status: ProjectStatus;
  created_at: string;
  updated_at: string;
};

export type Paper = {
  id: string;
  openalex_id: string;
  title: string;
  authors: string[];
  publication_year: number | null;
  abstract: string | null;
  landing_page_url: string | null;
  doi: string | null;
};

export type SavedPaper = Paper & {
  saved_at: string;
};

export type CreateProjectInput = {
  title: string;
  question: string;
};

export type UpdateProjectInput = Partial<CreateProjectInput> & {
  status?: ProjectStatus;
};

export type ApiError = {
  message: string;
  status?: number;
};

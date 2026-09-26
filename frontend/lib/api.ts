import type {
  ApiError,
  CreateProjectInput,
  Paper,
  PaperType,
  Project,
  SavedPaper,
  UpdateProjectInput,
} from "@/lib/types";

const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const useMockApi = process.env.NEXT_PUBLIC_USE_MOCK_API !== "false";
const storageKey = "psyche-research-mock-state";

type MockState = {
  projects: Project[];
  papers: Record<string, SavedPaper[]>;
};

const initialState: MockState = {
  projects: [
    {
      id: "mock-project-1",
      title: "Sleep and academic performance",
      question:
        "How does sleep quality affect academic performance in university students?",
      status: "active",
      created_at: "2026-09-01T10:00:00.000Z",
      updated_at: "2026-09-01T10:00:00.000Z",
    },
  ],
  papers: {},
};

function getMockState(): MockState {
  if (typeof window === "undefined") return initialState;

  const stored = window.localStorage.getItem(storageKey);
  if (!stored) {
    window.localStorage.setItem(storageKey, JSON.stringify(initialState));
    return initialState;
  }

  try {
    return JSON.parse(stored) as MockState;
  } catch {
    window.localStorage.setItem(storageKey, JSON.stringify(initialState));
    return initialState;
  }
}

function saveMockState(state: MockState) {
  window.localStorage.setItem(storageKey, JSON.stringify(state));
}

function mockPaper(index: number, query: string): Paper {
  return {
    id: `mock-paper-${index}`,
    openalex_id: `https://openalex.org/mock-${index}`,
    title: `${query}: a systematic review of current evidence`,
    authors: ["Research Archive", `Author ${index}`],
    publication_year: 2024 - (index % 3),
    abstract:
      "This sample result is available in mock mode so the research workflow can be exercised before the API is connected.",
    landing_page_url: "https://openalex.org/",
    doi: null,
  };
}

async function request<T>(path: string, token: string | null, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiUrl}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...init?.headers,
    },
  });

  if (!response.ok) {
  let message = "Something went wrong. Please try again.";

  try {
    const body = await response.json();

    if (typeof body.detail === "string") {
      message = body.detail;
    } else if (Array.isArray(body.detail)) {
      message = body.detail
        .map((error: { msg?: string }) => error.msg ?? "Validation error")
        .join(", ");
    } else if (typeof body.message === "string") {
      message = body.message;
    }
  } catch {
    // Keep fallback message
  }

  const error: ApiError = {
    message,
    status: response.status,
  };

  throw error;
}

  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export async function listProjects(token: string | null): Promise<Project[]> {
  return request<Project[]>("/api/projects", token);
}

export async function getProject(token: string | null, projectId: string): Promise<Project> {
  return request<Project>(`/api/projects/${projectId}`, token);
}

export async function createProject(
  token: string | null,
  input: CreateProjectInput,
): Promise<Project> {
  return request<Project>("/api/projects/", token, {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function updateProject(
  token: string | null,
  projectId: string,
  input: UpdateProjectInput,
): Promise<Project> {
  return request<Project>(`/api/projects/${projectId}`, token, {
    method: "PATCH",
    body: JSON.stringify(input),
  });
}

export async function deleteProject(token: string | null, projectId: string): Promise<void> {
  return request<void>(`/api/projects/${projectId}`, token, { method: "DELETE" });
}

export async function searchPapers(
  token: string | null,
  query: string,
  fromPublicationDate: string,
  type: PaperType,
): Promise<Paper[]> {

  const body = {
    query,
    page: 1,
    per_page: 10,
    filters: {
      type,
      from_publication_date: fromPublicationDate,
    },
  };

  const result = await request<Paper[] | { results: Paper[] }>(
    `/api/papers/search/papers`,
    token,
    {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
      },
    }
  );

  return Array.isArray(result) ? result : result.results;
}

export async function listSavedPapers(
  token: string | null,
  projectId: string,
): Promise<SavedPaper[]> {
  if (useMockApi) return getMockState().papers[projectId] ?? [];
  return request<SavedPaper[]>(`/api/projects/${projectId}/papers`, token);
}

export async function savePaper(
  token: string | null,
  projectId: string,
  paper: Paper,
): Promise<SavedPaper> {
  if (useMockApi) {
    const state = getMockState();
    const existing = state.papers[projectId]?.find(
      (item) => item.openalex_id === paper.openalex_id,
    );
    if (existing) return existing;
    const saved = { ...paper, saved_at: new Date().toISOString() };
    saveMockState({
      ...state,
      papers: { ...state.papers, [projectId]: [...(state.papers[projectId] ?? []), saved] },
    });
    return saved;
  }
  return request<SavedPaper>(`/api/projects/${projectId}/papers`, token, {
    method: "POST",
    body: JSON.stringify(paper),
  });
}

export async function removePaper(
  token: string | null,
  projectId: string,
  paperId: string,
): Promise<void> {
  if (useMockApi) {
    const state = getMockState();
    saveMockState({
      ...state,
      papers: {
        ...state.papers,
        [projectId]: (state.papers[projectId] ?? []).filter((item) => item.id !== paperId),
      },
    });
    return;
  }
  return request<void>(`/api/projects/${projectId}/papers/${paperId}`, token, {
    method: "DELETE",
  });
}

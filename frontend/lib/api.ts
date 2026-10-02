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

async function request<T>(
  path: string,
  token: string | null,
  init?: RequestInit,
): Promise<T> {
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
      // Keep fallback message.
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

export async function getProject(
  token: string | null,
  projectId: string,
): Promise<Project> {
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

export async function deleteProject(
  token: string | null,
  projectId: string,
): Promise<void> {
  return request<void>(`/api/projects/${projectId}`, token, {
    method: "DELETE",
  });
}

export async function searchPapers(
  token: string | null,
  query: string,
  fromPublicationDate: string,
  type: PaperType,
): Promise<Paper[]> {
  const body = {
    query: query.trim(),
    page: 1,
    per_page: 20,
    filters: {
      type,
      from_publication_date: fromPublicationDate,
    },
  };

  const result = await request<{ papers: Paper[] }>(
    "/api/papers/search/papers",
    token,
    {
      method: "POST",
      body: JSON.stringify(body),
    },
  );

  return result.papers;
}

export async function listSavedPapers(
  token: string | null,
  projectId: string,
): Promise<SavedPaper[]> {
  return request<SavedPaper[]>(`/api/projects/${projectId}/papers`, token);
}

export async function savePaper(
  token: string | null,
  projectId: string,
  paper: Paper,
): Promise<SavedPaper> {
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
  return request<void>(
    `/api/projects/${projectId}/papers/${paperId}`,
    token,
    {
      method: "DELETE",
    },
  );
}

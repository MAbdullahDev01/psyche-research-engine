-- Index projects by owner.
CREATE INDEX idx_projects_user_id
ON public.projects(user_id);

-- Index project_papers by paper.
CREATE INDEX idx_project_papers_paper_id
ON public.project_papers(paper_id);
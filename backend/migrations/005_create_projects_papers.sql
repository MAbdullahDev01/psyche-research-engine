CREATE TABLE project_papers (
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    paper_id UUID NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    saved_at TIMESTAMPTZ DEFAULT NOW(),

    PRIMARY KEY (project_id, paper_id)
);
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..db import SessionLocal
from ..models_db import WorkspaceDB

router = APIRouter()


class WorkspaceCreate(BaseModel):
    title: str
    description: str | None = None


@router.post("/")
def create_workspace(body: WorkspaceCreate):
    session = SessionLocal()
    try:
        ws = WorkspaceDB(title=body.title, description=body.description)
        session.add(ws)
        session.commit()
        session.refresh(ws)
        return {"id": ws.id, "title": ws.title, "description": ws.description}
    finally:
        session.close()


@router.get("/{workspace_id}")
def get_workspace(workspace_id: int):
    session = SessionLocal()
    try:
        ws = session.query(WorkspaceDB).get(workspace_id)
        if not ws:
            raise HTTPException(status_code=404, detail="workspace not found")
        return {"id": ws.id, "title": ws.title, "description": ws.description}
    finally:
        session.close()

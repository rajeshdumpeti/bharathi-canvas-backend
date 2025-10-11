from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.project import Project
from app.models.column import BoardColumn

DEFAULT_COLS = [
    ("to_do", "To Do", 0),
    ("in_progress", "In Progress", 1),
    ("validation", "Validation", 2),
    ("done", "Done", 3),
]

def run():
    db: Session = SessionLocal()
    try:
        if not db.query(Project).first():
            p = Project(name="Sample Project")
            db.add(p); db.flush()
            for key, title, pos in DEFAULT_COLS:
                db.add(BoardColumn(project_id=p.id, key=key, title=title, pos=pos))
            db.commit()
            print("Seeded Sample Project")
        else:
            print("Data already present; skipping seed.")
    finally:
        db.close()

if __name__ == "__main__":
    run()

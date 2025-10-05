from sqlalchemy.orm import Session
from uuid import UUID
from app.models.story_seq import StorySeq

def next_story_id(db: Session, project_id: UUID) -> str:
    seq = db.get(StorySeq, project_id)
    if not seq:
        seq = StorySeq(project_id=project_id, next_num=234567)
        db.add(seq)
        db.flush()
    value = seq.next_num
    seq.next_num = value + 1
    db.flush()
    return f"US{value}"

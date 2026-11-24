import json, uuid
from app.models.models import Mastery
def update_mastery(db,course_id,performance):
    for concept,stats in performance.items():
        status="established" if stats.get("correct",0)>=2 else "uncertain" if stats.get("correct",0)>0 else "misconception"
        row=db.query(Mastery).filter_by(course_id=course_id,concept_id=str(concept)).first()
        evidence=json.dumps(stats)
        if row: row.status=status; row.evidence_json=evidence
        else: db.add(Mastery(id=str(uuid.uuid4()),course_id=course_id,concept_id=str(concept),status=status,evidence_json=evidence))
    db.commit()

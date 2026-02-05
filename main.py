from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated, List
import models
from database import engine, sessionlocal, Base
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/questions")
async def get_all_questions(db: db_dependency):
    return db.query(models.Questions).all()

@app.get("/questions/{question_id}")
async def read_question(question_id: int, db: db_dependency):
    result = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail='Question not found')
    return result

@app.get("/choices/{question_id}")
async def read_choices(question_id: int, db: db_dependency):
    result = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail='Choices not found')
    return result

@app.post("/questions")
async def create_questions(question: QuestionBase, db:db_dependency):
    db_question = models.Questions(question_text = question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(choice_text = choice.choice_text, is_correct = choice.is_correct, question_id = db_question.id)
        db.add(db_choice)
    db.commit()

@app.put("/update/questions/{question_id}")
async def update_question(question_id: int,question: QuestionBase, db: db_dependency):
    db_question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail='Question not found')
    db_question.question_text = question.question_text
    db.query(models.Choices).filter(models.Choices.question_id == question_id).delete()
    for choice in question.choices:
        db_choice = models.Choices(choice_text = choice.choice_text, is_correct = choice.is_correct, question_id = db_question.id)
        db.add(db_choice)
    db.commit()
    db.refresh(db_question)
    return {"message": "Question updated successfully", "question_id": question_id}
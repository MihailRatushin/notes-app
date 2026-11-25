"""
Точка входа FastAPI. Пока минимум — чтобы убедиться, что всё поднимается.
"""

from fastapi import FastAPI

from app.core.config import settings  # noqa: F401

app = FastAPI(
    title="Notes API",
    version="0.1.0",
    description="Учебный проект: заметки с папками.",
)


@app.get("/")
def root():
    return {"message": "ok"}
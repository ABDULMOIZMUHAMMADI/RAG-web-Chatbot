from fastapi import APIRouter,  Depends
from models import User, Website
from sqlalchemy.orm import Session
from scraper import scrape_website
from embedding_service import get_embedding
from vector_store import add_chunks
from rag_service import split_text
from pydantic import BaseModel
from security import current_user
from database import get_db
from schemas import WebsiteRequest



router = APIRouter()




@router.post("/add-website")
def add_website(data: WebsiteRequest,
                user: User = Depends(current_user),
                db: Session = Depends(get_db)
):

    text = scrape_website(data.url)

    chunks = split_text(text)

    embeddings = [get_embedding(chunk) for chunk in chunks]

    add_chunks(chunks, embeddings)

    web = Website(
            user_id=user.id,
            url=data.url,
            status="Done",
        )

    db.add(web)
    db.commit()



    return {
        "message": "Website processed successfully",
        "total_chunks": len(chunks)
    }
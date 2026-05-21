from sqlalchemy import Column, String, Boolean, DateTime, Integer, Float
from sqlalchemy.orm import declarative_base
from typing import Dict, Any
from datetime import datetime

Base = declarative_base()

class MovieDBModel(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    description = Column(String)
    image_url = Column(String)
    location = Column(String)
    published = Column(Boolean)
    rating = Column(Float, default = 0)
    genre_id = Column(Integer) # Тут вторичный ключ но пока пусто
    created_at = Column(DateTime, default = datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "image_url": self.image_url,
            "location": self.location,
            "published": self.published,
            'rating': self.rating,
            "genre_id": self.genre_id,
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<Movie(id='{self.id}', name='{self.name}')>"


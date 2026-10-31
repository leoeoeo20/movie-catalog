from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import CheckConstraint, Float, Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DATABASE_URL = "sqlite:///./movies.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class Movie(Base):
    __tablename__ = "movies"
    __table_args__ = (
        CheckConstraint("year >= 1888 AND year <= 2100", name="ck_movies_year"),
        CheckConstraint("rating >= 0 AND rating <= 10", name="ck_movies_rating"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    genre: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False, default=0)


class MovieCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    year: int = Field(ge=1888, le=2100)
    genre: str = Field(min_length=1, max_length=100)
    rating: float = Field(default=0, ge=0, le=10)


class MovieRead(MovieCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


app = FastAPI(title="Movie Catalog API", version="1.0.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/movies", response_model=list[MovieRead])
def list_movies(
    db: Session = Depends(get_db),
    genre: str | None = None,
    year: int | None = Query(default=None, ge=1888, le=2100),
    sort: str = Query(default="title", pattern="^(title|year|rating)$"),
    order: str = Query(default="asc", pattern="^(asc|desc)$"),
):
    stmt = select(Movie)
    if genre:
        stmt = stmt.where(Movie.genre == genre)
    if year is not None:
        stmt = stmt.where(Movie.year == year)
    column = getattr(Movie, sort)
    stmt = stmt.order_by(column.desc() if order == "desc" else column.asc())
    return db.scalars(stmt).all()


@app.get("/movies/{movie_id}", response_model=MovieRead)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.post("/movies", response_model=MovieRead, status_code=201)
def create_movie(data: MovieCreate, db: Session = Depends(get_db)):
    movie = Movie(**data.model_dump())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


@app.delete("/movies/{movie_id}", status_code=204)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(movie)
    db.commit()

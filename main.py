from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2008',
        'rating': 7.8,
        'category': 'Acción'    
    },
        {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    } 
]


app = FastAPI()
app.title = "Mi Aplicacion con FastAPI"
app.version = "0.0.3"

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default="Pelicula def", min_length=5, max_length = 15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(default=10, ge=1, le=10)
    category: str = Field(default='Categoría', min_length=5, max_length=15)
    class Config:
        schema_extra = {
            "exmaple":{
                "id": 1,
                "title": "Mi película",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 9.8,
                "category" : "Acción"
            }
        }



@app.get('/', tags = ['home'])
def message():
    return HTMLResponse("<h1>Hello Word </h1>")

@app.get('/movies', tags=['movies'])
def get_movies():
    return JSONResponse(content=movies)

@app.get('/movies/{id}', tags=['movies'])
def getmov(id: int = Path(ge=1,le=2000)):
    for movie in movies:
        if movie["id"] == id:
            return JSONResponse(content=movie)
    return JSONResponse(content=[])

@app.get('/movies/', tags=['movies'])
def getmovbycat (catergory: str = Query(min_length=5,max_length=15)):
    data = [item for item in movies if item['category'] == catergory]
    return JSONResponse(content=data)

@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie)
    return movies

@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item["id"] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return movies
    
@app.delete('/movies/{id}', tags=['movies'])
def delmov(id: int):
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
            return movies
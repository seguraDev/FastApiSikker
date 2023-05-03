from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

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

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales invalidas")

class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field( min_length=5, max_length = 15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field( min_length=5, max_length=15)
    
    class Config:
        schema_extra = {
            'example':{
                'id': 1,
                'title': 'Mi película',
                'overview': 'Descripción de la película',
                'year': 2022,
                'rating': 9.8,
                'category' : 'Acción'
            }
        }



@app.get('/', tags = ['home'])
def message():
    return HTMLResponse("<h1>Hello Word </h1>")

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def getmov(id: int = Path(ge=1,le=2000)) -> Movie:
    for movie in movies:
        if movie["id"] == id:
            return JSONResponse(content=movie)
    return JSONResponse(status_code=404, content=[])

@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def getmovbycat (catergory: str = Query(min_length=5,max_length=15)) -> List[Movie]:
    data = [item for item in movies if item['category'] == catergory]
    return JSONResponse(content=data)

@app.post('/movies', tags=['movies'], response_model=dict)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={"message": "se ha registrado la pelicula"})

@app.put('/movies/{id}', tags=['movies'], response_model=dict)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(status_code=200,content={"message": "se ha registrado la pelicula"})
    
@app.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delmov(id: int) -> dict:
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
            return JSONResponse(status_code=200, content={"message": "se ha eliminado la pelicula"})
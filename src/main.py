from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, status
from fastapi.concurrency import asynccontextmanager

from src.constants import STATE_FILE
from src.database_manager.local_file_storage import load_state, save_state
from src.routes.api_routes import router, movies, shops, _next_movie_id, _next_shop_id

@asynccontextmanager
async def lifespan(app: FastAPI):
    global movies, shops, _next_movie_id, _next_shop_id 
    movies, shops, _next_movie_id, _next_shop_id = load_state(STATE_FILE)
    yield
    save_state(STATE_FILE, movies, shops, _next_movie_id, _next_shop_id)
    
app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    if request.method == "POST" or request.method == "PUT" or request.method == "DELETE":
        save_state(STATE_FILE, movies, shops, _next_movie_id, _next_shop_id)
    return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    msgs = [ f"Validation Error: {dict_err['type']} {dict_err['loc'][1]} attribute." for dict_err in exc.errors() ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content= {"detail": msgs}
    )

app.include_router(router)

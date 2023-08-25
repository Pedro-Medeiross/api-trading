import os
from fastapi import FastAPI, Request
from connection import engine
from fastapi.middleware.cors import CORSMiddleware
from routes.user_routes import user_router
from routes.bot_routes import bot_router
from routes.trades_routes import trades_router
from routes.role_routes import role_router
from routes.management_routes import management_router
from routes.email_routes import email_router
from routes.news_routes import news_router
from models import trades
from connection import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


def table_exists(model):
    session = SessionLocal()
    try:
        # tenta obter os primeiros resultados da consulta a tabela
        session.query(model).first()
        return True
    except:
        return False
    finally:
        session.close()


models_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')

all_files = os.listdir(models_folder_path)

exclude_files = ['__pycache__', 'base_model.py', '__init__.py', 'trades.py']

models_files = [file for file in all_files if file not in exclude_files]


if table_exists(trades):
    print('Tabela já existe')
else:
    trades.Base.metadata.create_all(engine)

app = FastAPI()

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://v1.investingbrazil.online",
    "https://investingbrazil.online",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def sqlalchemy_error_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except SQLAlchemyError as e:
        error_message = str(e)
        # Trate a exceção do SQLAlchemy aqui
        return JSONResponse(status_code=500, content={"detail": "Erro no banco de dados", "error_message": error_message})

app.include_router(router=user_router, prefix="/user", tags=["User"])
app.include_router(router=trades_router, prefix="/trades", tags=["Trades"])
app.include_router(router=role_router, prefix="/role", tags=["Role"])
app.include_router(router=news_router, prefix="/news", tags=["News"])
app.include_router(router=management_router, prefix="/management", tags=["Management"])
app.include_router(router=email_router, prefix="/email", tags=["Email"])
app.include_router(router=bot_router, prefix="/bot", tags=["Bot"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": "Erro de validação", "errors": exc.errors()})

# Middleware para tratar exceções gerais (opcional)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Erro interno do servidor"})


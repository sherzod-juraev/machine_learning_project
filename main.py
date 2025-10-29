from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core import register_exception_handler, config
# Import modules
from modules import api_router


app = FastAPI()

# Add modules
app.include_router(api_router)

# exception handlers
register_exception_handler(app)

# Add cors for React.js
app.add_middleware(
    CORSMiddleware,
    allow_origins = [config.VITE_API_URL,],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
    allow_headers=['*']
)
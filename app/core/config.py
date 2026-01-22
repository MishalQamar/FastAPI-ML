import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = "FastAPI-ML"
    API_KEY=os.getenv("API_KEY",'demo-key')
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY",'secret')
    JWT_ALGORITHM='HS256'
    REDIS_URL=os.getenv("REDIS_URL",'redis://localhost:6379')
    MODEL_PATH='app/models/model.joblib'
    # Exchange rate: INR to GBP (1 GBP = X INR)
    # Default rate is approximately 1 GBP = 105 INR (can be overridden via env var)
    INR_TO_GBP_RATE = float(os.getenv("INR_TO_GBP_RATE", "105.0"))

settings = Settings()
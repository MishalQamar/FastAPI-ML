import joblib
import pandas as pd
from app.core.config import settings
from app.cache.redis_cache import get_cached_prediction, set_cached_predicition


model = joblib.load(settings.MODEL_PATH)
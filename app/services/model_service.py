import joblib
import pandas as pd
from app.core.config import settings
from app.cache.redis_cache import get_cached_prediction, set_cached_predicition

# Lazy load model to avoid import-time errors
_model = None

def _get_model():
    global _model
    if _model is None:
        _model = joblib.load(settings.MODEL_PATH)
    return _model


# API uses "torque"; model was trained on "torque_nm"
_API_TO_MODEL_COLUMNS = {"torque": "torque_nm"}


def predict_car_price(data: dict):
    cache_key = "".join([str(val) for val in data.values()])
    cached = get_cached_prediction(cache_key)
    if cached:
        return cached

    model = _get_model()
    mapped = {_API_TO_MODEL_COLUMNS.get(k, k): v for k, v in data.items()}
    input_data = pd.DataFrame([mapped])
    predicition = model.predict(input_data)[0]
    set_cached_predicition(cache_key, predicition)
    return predicition
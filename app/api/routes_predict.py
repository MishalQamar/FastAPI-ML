from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter()


class CarFeatures(BaseModel):
    company: str
    year: int
    owner: str
    fuel: str
    seller_type: str
    transmission: str
    km_driven: float
    mileage_mpg: float
    engine_cc: float
    max_power_bhp: float
    torque: float
    seats: float


@router.post("/predict")
def predict_price(
    car: CarFeatures,
    user=Depends(lambda token=Depends(__import__("app.core.dependencies").core.dependencies.get_current_user): token),
    api_key=Depends(lambda key=Depends(__import__("app.core.dependencies").core.dependencies.get_api_key): key),
):
    from app.services.model_service import predict_car_price
    from app.core.config import settings

    # Get prediction in INR (original currency)
    prediction_inr = predict_car_price(car.model_dump())
    
    # Convert to GBP
    prediction_gbp = prediction_inr / settings.INR_TO_GBP_RATE
    
    return {
        "predicted_price": round(prediction_gbp, 2),
        "currency": "GBP"
    }
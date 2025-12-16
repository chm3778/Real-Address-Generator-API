from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.utils.country_manager import country_manager
from app.utils.address_fetcher import address_fetcher
from app.utils.persona_generator import persona_generator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Real Address Generator API",
    description="Generates real addresses, names, and phone numbers based on country input.",
    version="1.0.0"
)

class AddressRequest(BaseModel):
    country: str
    state: Optional[str] = None
    city: Optional[str] = None
    zipcode: Optional[str] = None

class AddressResponse(BaseModel):
    name: str
    phone: str
    address: str
    city_state: str
    zipcode: Optional[str]
    country: str
    full_address: str

@app.get("/api/generate", response_model=AddressResponse)
def generate_address(
    country: str = Query(..., description="Country name (e.g., 'US', 'America', '美国')"),
    state: Optional[str] = Query(None, description="State/Province"),
    city: Optional[str] = Query(None, description="City"),
    zipcode: Optional[str] = Query(None, description="Zip/Postal Code")
):
    return _process_generation(country, state, city, zipcode)

@app.post("/api/generate", response_model=AddressResponse)
def generate_address_post(request: AddressRequest):
    return _process_generation(request.country, request.state, request.city, request.zipcode)

def _process_generation(country_input, state, city, zipcode):
    # 1. Normalize Country
    country_code = country_manager.normalize(country_input)
    if not country_code:
        # Fallback to US for adaptive behavior if normalization fails
        logger.warning(f"Country normalization failed for input '{country_input}'. Defaulting to US.")
        country_code = "US"

    # 2. Fetch Real Address
    real_address_data = address_fetcher.fetch_real_address(country_code, city, zipcode, state)
    
    if not real_address_data:
        # Fallback if external API is down completely (should be rare with our robust fallbacks)
        raise HTTPException(status_code=503, detail="Unable to fetch real address from network at this time.")

    # 3. Generate Persona (Name + Phone)
    persona = persona_generator.generate(country_code)

    # 4. Format Output
    # Requirements: name, phone, address, city_state, zipcode, country, full_address
    
    # Construct city_state string
    c = real_address_data.get('city') or ""
    s = real_address_data.get('state') or ""
    city_state = f"{c}, {s}".strip(", ")
    
    return {
        "name": persona['name'],
        "phone": persona['phone'],
        "address": real_address_data['address'], # Street address
        "city_state": city_state, # Province/City
        "zipcode": real_address_data['zipcode'],
        "country": real_address_data['country'] or country_code,
        "full_address": real_address_data['full_address']
    }

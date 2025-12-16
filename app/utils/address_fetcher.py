import requests
import random
import logging
import time
from faker import Faker
from app.utils.country_manager import country_manager

logger = logging.getLogger(__name__)

class AddressFetcher:
    def __init__(self):
        # Nominatim requires a valid User-Agent with contact info
        self.user_agent = "RealAddressGenerator/1.0 (contact@example.com)"
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.search_keywords = [
            "hotel", "restaurant", "school", "cafe", "bakery", "pharmacy", 
            "library", "post office", "park", "supermarket", "museum", "hospital"
        ]
        self.major_cities = {
            "US": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
            "CN": ["Beijing", "Shanghai", "Guangzhou", "Shenzhen"],
            "GB": ["London", "Manchester", "Birmingham"],
            "JP": ["Tokyo", "Osaka", "Kyoto"],
            "DE": ["Berlin", "Munich", "Hamburg"],
            "FR": ["Paris", "Lyon", "Marseille"],
        }

    def _get_headers(self):
        return {
            "User-Agent": self.user_agent
        }

    def fetch_real_address(self, country_code: str, city: str = None, zipcode: str = None, state: str = None):
        """
        Fetches a real address from OpenStreetMap (Nominatim).
        Uses intelligent fallbacks if specific inputs fail.
        """
        locale = country_manager.get_faker_locale(country_code)
        fake = Faker(locale)
        
        # Level 1: Specific User Input (City OR Zipcode)
        # If Zipcode is provided, it's very specific, so we try to use it.
        if city or zipcode:
            logger.info(f"Attempting Level 1 search with user input: City={city}, Zip={zipcode}, State={state}, Country={country_code}")
            address = self._query_nominatim(country_code, city=city, zipcode=zipcode, state=state)
            if address: return address

        # Level 2: Ignore User City/State/Zip (if they failed), generate a Random City for that country
        logger.info(f"Attempting Level 2 search with random city for {country_code}")
        for _ in range(2): 
            try:
                random_city = fake.city()
                address = self._query_nominatim(country_code, city=random_city)
                if address: return address
            except Exception as e:
                logger.warning(f"Error in Level 2 random city generation: {e}")
        
        # Try Hardcoded Major Cities
        if country_code in self.major_cities:
            fallback_city = random.choice(self.major_cities[country_code])
            logger.info(f"Attempting Level 2 fallback with major city: {fallback_city}")
            address = self._query_nominatim(country_code, city=fallback_city)
            if address: return address

        # Level 3: Absolute fallback
        logger.info(f"Attempting Level 3 broad search for {country_code}")
        address = self._query_nominatim(country_code, city=None, broad_search=True)
        if address: return address

        return None

    def _query_nominatim(self, country_code, city=None, zipcode=None, state=None, broad_search=False):
        """
        Helper to execute the search query.
        """
        keyword = random.choice(self.search_keywords)
        
        query_parts = []
        
        if not broad_search:
            query_parts.append(keyword)
            # If zipcode is provided, it's a strong filter.
            if zipcode:
                # Nominatim handles zipcodes well in free-form query or structured.
                # Let's try appending it to query parts.
                query_parts.append(f"in {zipcode}")
            
            if city:
                # If we have both zip and city, using both is good.
                # "Hotel in 10001 New York"
                query_parts.append(f"in {city}")
            
            if state:
                query_parts.append(state)
        else:
            query_parts.append(f"{keyword} in") 

        q_str = " ".join(query_parts)
        
        params = {
            "q": q_str,
            "countrycodes": country_code,
            "format": "jsonv2",
            "addressdetails": 1,
            "limit": 10, 
            "accept-language": "native" 
        }

        try:
            resp = requests.get(self.nominatim_url, params=params, headers=self._get_headers(), timeout=25)
            if resp.status_code == 200:
                results = resp.json()
                if results:
                    valid_results = [r for r in results if 'address' in r]
                    if valid_results:
                        picked = random.choice(valid_results)
                        return self._parse_osm_result(picked)
            else:
                logger.warning(f"Nominatim returned status {resp.status_code}")
        except Exception as e:
            logger.error(f"Nominatim Request Error: {e}")
        
        return None

    def _parse_osm_result(self, result):
        """
        Extracts relevant fields from OSM result.
        """
        addr = result.get('address', {})
        
        street = addr.get('road') or addr.get('pedestrian') or addr.get('footway') or addr.get('street')
        house_num = addr.get('house_number')
        
        address_line = ""
        if street:
            if house_num:
                address_line = f"{house_num} {street}"
            else:
                address_line = street
        else:
            address_line = addr.get('amenity') or addr.get('shop') or result.get('name') or "Unknown Street"

        city = addr.get('city') or addr.get('town') or addr.get('village') or addr.get('county') or addr.get('municipality')
        state = addr.get('state') or addr.get('province') or addr.get('region')
        zipcode = addr.get('postcode')
        country = addr.get('country')
        full_address = result.get('display_name')

        return {
            "address": address_line,
            "city": city,
            "state": state,
            "zipcode": zipcode,
            "country": country,
            "full_address": full_address
        }

address_fetcher = AddressFetcher()

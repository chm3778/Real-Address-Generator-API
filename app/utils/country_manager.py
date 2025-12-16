from babel import Locale
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CountryManager:
    def __init__(self):
        self.country_map = {}
        self.load_country_data()

    def load_country_data(self):
        """
        Dynamically builds a dictionary mapping country names (English & Chinese) 
        and codes to ISO 2-letter codes.
        """
        # 1. Load English names
        try:
            locale_en = Locale('en')
            for code, name in locale_en.territories.items():
                self.country_map[name.lower()] = code
        except Exception as e:
            logger.error(f"Error loading English locale data: {e}")

        # 2. Load Chinese names
        try:
            locale_zh = Locale('zh')
            for code, name in locale_zh.territories.items():
                self.country_map[name.lower()] = code
        except Exception as e:
            logger.error(f"Error loading Chinese locale data: {e}")

        # 3. Add ISO codes themselves (2-letter and 3-letter support if possible, mainly 2 for now)
        # We can iterate through the loaded map values to get valid codes
        valid_codes = set(self.country_map.values())
        for code in valid_codes:
            self.country_map[code.lower()] = code

        # 4. Add Manual Aliases (Colloquialisms)
        # These are commonly used terms that might not appear in official territory lists
        manual_aliases = {
            "america": "US",
            "usa": "US",
            "uk": "GB",
            "england": "GB",
            "great britain": "GB",
            "russia": "RU",
            "south korea": "KR",
            "north korea": "KP",
        }
        for alias, code in manual_aliases.items():
            self.country_map[alias] = code
        
        logger.info(f"Loaded {len(self.country_map)} country name mappings.")

    def normalize(self, input_str: str) -> str:
        """
        Normalizes a country string to its ISO 2-letter code.
        Returns None if not found.
        """
        if not input_str:
            return None
        
        normalized_input = input_str.strip().lower()
        return self.country_map.get(normalized_input)

    def get_faker_locale(self, iso_code: str) -> str:
        """
        Returns a suitable Faker locale code for a given ISO country code.
        Defaults to 'en_US' if no specific mapping is found.
        """
        # Mapping ISO codes to Faker locales
        # This is not exhaustive but covers major ones. 
        # We can expand this or use a library, but a simple map is efficient here.
        iso_to_faker = {
            "US": "en_US",
            "CN": "zh_CN",
            "GB": "en_GB",
            "FR": "fr_FR",
            "DE": "de_DE",
            "JP": "ja_JP",
            "KR": "ko_KR",
            "IT": "it_IT",
            "ES": "es_ES",
            "RU": "ru_RU",
            "IN": "en_IN", # or hi_IN
            "BR": "pt_BR",
            "CA": "en_CA",
            "AU": "en_AU",
            "TW": "zh_TW",
            "HK": "zh_HK",
            # Add more as needed
        }
        return iso_to_faker.get(iso_code, "en_US")

# Global instance
country_manager = CountryManager()

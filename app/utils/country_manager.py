from babel import Locale
import logging
from faker.config import AVAILABLE_LOCALES

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CountryManager:
    def __init__(self):
        self.country_map = {}
        self.iso_to_faker = {}
        self.load_country_data()
        self._build_faker_map()

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

    def _build_faker_map(self):
        """
        Dynamically builds a map from ISO country codes to Faker locales
        based on available locales in Faker.
        """
        territory_locales = {}

        for loc_str in AVAILABLE_LOCALES:
            try:
                l = Locale.parse(loc_str)
                terr = l.territory
                if terr:
                    if terr not in territory_locales:
                        territory_locales[terr] = []
                    territory_locales[terr].append(loc_str)
            except Exception:
                # Ignore locales that cannot be parsed by Babel
                continue

        for territory, locales in territory_locales.items():
            # Strategy: prefer English (en_XX), then fallback to first alphabetically
            selected = None

            # 1. Try to find a locale starting with 'en_'
            for loc in locales:
                if loc.startswith('en_'):
                    selected = loc
                    break

            # 2. If not found, just pick the first one after sorting
            if not selected:
                locales.sort()
                selected = locales[0]

            self.iso_to_faker[territory] = selected

        logger.info(f"Built Faker locale map with {len(self.iso_to_faker)} entries.")

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
        if not iso_code:
            return "en_US"

        # Use the dynamically built map, falling back to "en_US"
        return self.iso_to_faker.get(iso_code, "en_US")

# Global instance
country_manager = CountryManager()

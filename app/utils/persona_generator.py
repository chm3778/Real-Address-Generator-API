from app.utils.country_manager import country_manager
import phonenumbers
from phonenumbers import PhoneNumberFormat, PhoneNumberType
import random
import logging

logger = logging.getLogger(__name__)

class PersonaGenerator:
    def generate(self, country_code: str):
        """
        Generates a random name and phone number for the given country.
        """
        fake = country_manager.get_faker(country_code)

        return {
            "name": fake.name(),
            "phone": self._generate_phone_number(country_code, fake)
        }

    def _generate_phone_number(self, country_code: str, fake) -> str:
        """
        Generates a valid-looking phone number for the country.
        Uses phonenumbers library to get a correct format and country code,
        then randomizes the last few digits.
        Falls back to Faker if phonenumbers fails (e.g., Antarctica).
        """
        try:
            # Try to get an example mobile number first
            example = phonenumbers.example_number_for_type(country_code, PhoneNumberType.MOBILE)

            # If no mobile example, try generic example
            if not example:
                example = phonenumbers.example_number(country_code)

            if example:
                # Get E164 format (e.g. +12015550123)
                e164_str = phonenumbers.format_number(example, PhoneNumberFormat.E164)

                # Determine how many digits to randomize
                # We want to keep the country code and maybe the first few digits of the area code/prefix

                # e164_str starts with '+', so len(str(example.country_code)) + 1 is the end of CC
                cc_len = len(str(example.country_code))
                prefix_len = cc_len + 1 # include '+'

                total_digits = len(e164_str) - 1 # excluding '+'

                # We want to randomize the subscriber part.
                # Heuristic: Randomize the last 4 to 6 digits, but ensure we don't eat into the country code.
                # Also ensure we leave some "area code" digits if possible.

                # If we keep the first 2 digits of the national number (after CC), that usually preserves area code or mobile prefix.
                digits_to_keep_len = prefix_len + 2

                # Calculate how many digits we can randomize
                num_digits_to_randomize = len(e164_str) - digits_to_keep_len

                # Cap the randomization at 6 digits to keep it realistic and stable
                # and ensure we randomize at least 4 digits if possible
                num_digits_to_randomize = min(num_digits_to_randomize, 6)

                if num_digits_to_randomize < 4:
                    # If the number is short, just randomize what we can after CC + 1 digit
                     num_digits_to_randomize = max(0, len(e164_str) - (prefix_len + 1))

                if num_digits_to_randomize > 0:
                    prefix = e164_str[:-num_digits_to_randomize]
                    random_part = "".join([str(random.randint(0, 9)) for _ in range(num_digits_to_randomize)])
                    new_number_str = prefix + random_part

                    # Parse and re-format to ensure it looks good (spaces etc)
                    try:
                        new_obj = phonenumbers.parse(new_number_str, country_code)
                        return phonenumbers.format_number(new_obj, PhoneNumberFormat.INTERNATIONAL)
                    except Exception:
                        # If parsing fails (unlikely), return the string as is
                        return new_number_str
                else:
                     # Too short to randomize safely, return example formatted
                     return phonenumbers.format_number(example, PhoneNumberFormat.INTERNATIONAL)

        except Exception as e:
            logger.warning(f"Failed to generate phone number using phonenumbers for {country_code}: {e}")

        # Fallback to Faker
        return fake.phone_number()

persona_generator = PersonaGenerator()

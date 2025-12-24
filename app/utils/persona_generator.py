from app.utils.country_manager import country_manager

class PersonaGenerator:
    def generate(self, country_code: str):
        """
        Generates a random name and phone number for the given country.
        """
        fake = country_manager.get_faker(country_code)

        return {
            "name": fake.name(),
            "phone": fake.phone_number()
        }

persona_generator = PersonaGenerator()

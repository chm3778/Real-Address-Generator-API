import unittest
from app.utils.country_manager import country_manager

class TestCountryManager(unittest.TestCase):
    def test_normalization(self):
        test_cases = [
            ("美国", "US"),
            ("United States", "US"),
            ("USA", "US"),
            ("America", "US"),
            ("China", "CN"),
            ("中国", "CN"),
            ("CN", "CN"),
            ("Germany", "DE"),
            # ("Deutschland", "DE"), # Babel might know this if we load 'de' locale too, but let's check en/zh coverage
            ("France", "FR"),
            ("法国", "FR"),
            ("JAPAN", "JP"),
            ("日本", "JP"),
            ("UnknownLand", None),
        ]

        print("Running Country Normalization Tests...")
        for input_str, expected in test_cases:
            result = country_manager.normalize(input_str)
            self.assertEqual(result, expected, f"Input: '{input_str}' -> Expected: {expected}, Got: {result}")

    def test_get_faker_locale(self):
        """Test that get_faker_locale returns appropriate locales."""
        # Test basic mappings that should always exist if Faker is installed
        self.assertEqual(country_manager.get_faker_locale("US"), "en_US")
        self.assertEqual(country_manager.get_faker_locale("CN"), "zh_CN")
        self.assertEqual(country_manager.get_faker_locale("JP"), "ja_JP")

        # Test dynamically added mappings
        # Switzerland should have a mapping (likely de_CH)
        ch_locale = country_manager.get_faker_locale("CH")
        self.assertTrue(ch_locale.endswith("CH"), f"Expected *CH, got {ch_locale}")

        # Test priority (English preference)
        # Canada has en_CA and fr_CA. We prefer en_CA.
        self.assertEqual(country_manager.get_faker_locale("CA"), "en_CA")

        # India has multiple languages. We prefer en_IN.
        self.assertEqual(country_manager.get_faker_locale("IN"), "en_IN")

        # Test fallback for known country but no specific locale (depends on installed Faker)
        # If HK is not supported by Faker, it should fallback to en_US
        # If it IS supported, it should be something ending in HK.
        # Given current faker version (38.2.0), HK is not supported.
        hk_locale = country_manager.get_faker_locale("HK")
        self.assertEqual(hk_locale, "en_US")

        # Test unknown country
        self.assertEqual(country_manager.get_faker_locale("ZZ"), "en_US")
        self.assertEqual(country_manager.get_faker_locale(None), "en_US")

if __name__ == "__main__":
    unittest.main()

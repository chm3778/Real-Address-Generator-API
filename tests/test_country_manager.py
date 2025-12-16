from app.utils.country_manager import country_manager

def test_normalization():
    test_cases = [
        ("美国", "US"),
        ("United States", "US"),
        ("USA", "US"),
        ("America", "US"),
        ("China", "CN"),
        ("中国", "CN"),
        ("CN", "CN"),
        ("Germany", "DE"),
        ("Deutschland", "DE"), # Babel might know this if we load 'de' locale too, but let's check en/zh coverage
        ("France", "FR"),
        ("法国", "FR"),
        ("JAPAN", "JP"),
        ("日本", "JP"),
        ("UnknownLand", None),
    ]

    print("Running Country Normalization Tests...")
    for input_str, expected in test_cases:
        result = country_manager.normalize(input_str)
        status = "✅" if result == expected else f"❌ (Got {result})"
        print(f"{status} Input: '{input_str}' -> Expected: {expected}")

if __name__ == "__main__":
    test_normalization()

from app.utils.address_fetcher import address_fetcher

def test_fetcher():
    # Test 1: Generic US Search
    print("Test 1: Generic US Search")
    addr = address_fetcher.fetch_real_address("US")
    print(f"Result: {addr}\n")

    # Test 2: Specific City (New York)
    print("Test 2: Specific City (New York, US)")
    addr = address_fetcher.fetch_real_address("US", city="New York")
    print(f"Result: {addr}\n")

    # Test 3: Conflict / Anti-Stupid (Beijing, US) -> Should fallback to random US city
    print("Test 3: Conflict (Beijing, US)")
    addr = address_fetcher.fetch_real_address("US", city="Beijing")
    print(f"Result: {addr}\n")

    # Test 4: China Search
    print("Test 4: China Search")
    addr = address_fetcher.fetch_real_address("CN")
    print(f"Result: {addr}\n")

if __name__ == "__main__":
    test_fetcher()

# Real Address Generator API

A robust FastAPI service that generates **real-world addresses** (verified via OpenStreetMap), paired with localized names and phone numbers. It is designed to be adaptive, handling various country input formats (e.g., "US", "America", "美国") and intelligently falling back if specific city/zip inputs are invalid.

## Features

*   **Real Addresses:** Fetches actual physical addresses using OpenStreetMap (Nominatim).
*   **Adaptive Input:** Smartly handles conflicts (e.g., wrong city for a country) by prioritizing the country and finding a real location within it.
*   **Multi-language Support:** Accepts country names in English, Chinese ("美国"), and ISO codes.
*   **Localized Persona:** Generates native-sounding names and phone numbers corresponding to the address.
*   **Deployment Ready:** Includes `Dockerfile` and configuration for easy deployment on Render.

## Local Setup

### Using Python

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the server:
    ```bash
    uvicorn app.main:app --reload
    ```
3.  Access the API documentation at `http://localhost:8000/docs`.

### Using Docker

1.  Build the image:
    ```bash
    docker build -t real-address-api .
    ```
2.  Run the container:
    ```bash
    docker run -p 8000:8000 real-address-api
    ```

## API Usage

### Endpoint: `GET /api/generate`

**Parameters:**
*   `country` (required): Country name (e.g., "US", "China", "Germany", "美国").
*   `city` (optional): Preferred city.
*   `zipcode` (optional): Preferred zipcode.
*   `state` (optional): Preferred state/province.

**Example Request:**
```
GET /api/generate?country=US&city=New%20York
```

**Example Response:**
```json
{
  "name": "John Doe",
  "phone": "+1-555-0199",
  "address": "44 West 63rd Street",
  "city_state": "New York, New York",
  "zipcode": "10023",
  "country": "United States",
  "full_address": "Hotel Empire, 44, West 63rd Street, Lincoln Square, New York, 10023, United States"
}
```

## Deployment (Render)

1.  Create a new **Web Service** on Render.
2.  Connect this repository.
3.  Select **Docker** as the Runtime.
4.  Render will automatically build and deploy using the `Dockerfile`.

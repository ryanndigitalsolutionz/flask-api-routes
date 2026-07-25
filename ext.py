import requests

def fetch_external_product(barcode):
    """Fetch product info from Open Food Facts API using a valid barcode."""
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            # Open Food Facts returns status: 1 if the product exists in their database
            if data.get("status") == 1:
                product = data.get("product", {})
                return {
                    "name": product.get("product_name", "Unknown Product"),
                    "barcode": barcode,
                    "price": 4.99,
                    "stock": 10
                }
    except requests.RequestException:
        return None

    return None

from api.database import SessionLocal
from api.models import Product

products = [
    {"name": "Laptop", "description": "Powerful gaming laptop", "price": 4500.00},
    {"name": "Mouse", "description": "Wireless ergonomic mouse", "price": 150.00},
    {"name": "Keyboard", "description": "Mechanical keyboard with RGB", "price": 300.00},
    {"name": "Monitor", "description": "4K UHD Monitor", "price": 1200.00},
    {"name": "Headphones", "description": "Noise-cancelling headphones", "price": 800.00},
    {"name": "Smartphone", "description": "Latest model with high-end specs", "price": 3500.00},
    {"name": "Smartwatch", "description": "Tracks health and notifications", "price": 900.00},
    {"name": "Gaming Chair", "description": "Comfortable chair for long gaming sessions", "price": 1000.00},
    {"name": "External HDD", "description": "1TB external hard drive", "price": 400.00},
    {"name": "USB Flash Drive", "description": "128GB high-speed USB", "price": 80.00},
    {"name": "Webcam", "description": "1080p Full HD webcam", "price": 250.00},
    {"name": "Microphone", "description": "Studio-quality condenser microphone", "price": 600.00},
    {"name": "Desk Lamp", "description": "LED desk lamp with adjustable brightness", "price": 120.00},
    {"name": "Power Bank", "description": "Fast charging 20000mAh power bank", "price": 220.00},
    {"name": "Bluetooth Speaker", "description": "Portable speaker with deep bass", "price": 300.00},
    {"name": "Tablet", "description": "10-inch tablet for work and entertainment", "price": 2800.00},
    {"name": "Router", "description": "High-speed Wi-Fi 6 router", "price": 700.00},
    {"name": "VR Headset", "description": "Virtual Reality headset for immersive experience", "price": 3500.00},
    {"name": "Electric Scooter", "description": "Foldable electric scooter with long battery life", "price": 4500.00},
    {"name": "Coffee Machine", "description": "Automatic espresso coffee machine", "price": 1500.00},
    {"name": "Air Purifier", "description": "HEPA air purifier with smart features", "price": 1300.00},
    {"name": "Smart TV", "description": "50-inch 4K UHD Smart TV with HDR", "price": 3800.00},
    {"name": "Graphics Tablet", "description": "Professional graphics tablet for designers", "price": 2700.00},
    {"name": "Wireless Earbuds", "description": "Noise-canceling wireless earbuds", "price": 600.00},
]


def seed_products():
    db = SessionLocal()
    try:
        for product in products:
            existing_product = db.query(Product).filter(Product.name == product["name"]).first()
            if not existing_product:
                new_product = Product(**product)
                db.add(new_product)
        
        db.commit()
        print("Products added successfully!")
    except Exception as e:
        print(f"Error adding products: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_products()

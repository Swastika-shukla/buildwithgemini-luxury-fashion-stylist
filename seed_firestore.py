import sys
from google.cloud import firestore

FIRESTORE_PROJECT_ID = "qwiklabs-gcp-01-43f6fab872ca"
BUCKET_BASE_URL = "https://storage.googleapis.com/luxury-fashion-media-qwiklabs-gcp-01-43f6fab872ca"

ITEMS = [
    {
        "item_id": "gucci-dionysus-001",
        "brand": "Gucci",
        "name": "Dionysus Small Shoulder Bag",
        "category": "Handbags",
        "price_usd": 2980.0,
        "aesthetic": "Classic Elegance",
        "materials": "GG Supreme canvas, taupe suede, tiger head closure",
        "image_url": f"{BUCKET_BASE_URL}/gucci_bag.png",
        "in_stock": True,
    },
    {
        "item_id": "ysl-5a7-002",
        "brand": "Saint Laurent",
        "name": "Le 5 à 7 Shoulder Bag",
        "category": "Handbags",
        "price_usd": 2400.0,
        "aesthetic": "Minimalist Luxury",
        "materials": "Smooth calfskin leather, bronze-tone metal YSL hook",
        "image_url": "",
        "in_stock": True,
    },
    {
        "item_id": "prada-monolith-003",
        "brand": "Prada",
        "name": "Monolith Brushed Leather Loafers",
        "category": "Footwear",
        "price_usd": 1250.0,
        "aesthetic": "Modern Edge",
        "materials": "Brushed Spazzolato leather, chunky lug sole, enamel triangle logo",
        "image_url": f"{BUCKET_BASE_URL}/prada_loafers.png",
        "in_stock": True,
    },
    {
        "item_id": "chanel-classic-004",
        "brand": "Chanel",
        "name": "Classic Double Flap Medium",
        "category": "Handbags",
        "price_usd": 10800.0,
        "aesthetic": "Timeless Glamour",
        "materials": "Quilted lambskin leather, gold-tone metal hardware",
        "image_url": "",
        "in_stock": False,
    },
    {
        "item_id": "hermes-oran-005",
        "brand": "Hermès",
        "name": "Oran Sandal",
        "category": "Footwear",
        "price_usd": 760.0,
        "aesthetic": "Understated Elegance",
        "materials": "Box calfskin leather with iconic 'H' cut-out",
        "image_url": "",
        "in_stock": True,
    },
    {
        "item_id": "balenciaga-city-006",
        "brand": "Balenciaga",
        "name": "Le Cagole XS Shoulder Bag",
        "category": "Handbags",
        "price_usd": 2700.0,
        "aesthetic": "Avant-Garde Streetwear",
        "materials": "Arena lambskin leather, aged-silver hardware with studs & mirror",
        "image_url": "",
        "in_stock": True,
    },
    {
        "item_id": "prada-cleo-007",
        "brand": "Prada",
        "name": "Prada Cleo Brushed Leather Shoulder Bag",
        "category": "Handbags",
        "price_usd": 2900.0,
        "aesthetic": "Sleek Modernism",
        "materials": "Brushed Spazzolato leather",
        "image_url": "",
        "in_stock": True,
    }
]

def seed():
    print(f"Connecting to Firestore project '{FIRESTORE_PROJECT_ID}'...")
    db = firestore.Client(project=FIRESTORE_PROJECT_ID)
    collection_ref = db.collection("luxury_catalog")

    for item in ITEMS:
        doc_ref = collection_ref.document(item["item_id"])
        doc_ref.set(item)
        print(f"  [+] Seeded item '{item['item_id']}': {item['brand']} - {item['name']} (${item['price_usd']})")

    print("Firestore seeding with image URLs complete! ✅")

if __name__ == "__main__":
    seed()

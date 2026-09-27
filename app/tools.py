import json
import os
from typing import Optional
import urllib.parse
import urllib.request
from google import genai
from google.genai import types
from google.cloud import firestore, storage
from google.adk.tools import ToolContext

# IMPORTANT: Hardcode project ID and bucket name as explicit strings.
FIRESTORE_PROJECT_ID = "qwiklabs-gcp-01-43f6fab872ca"
BUCKET_NAME = "luxury-fashion-media-qwiklabs-gcp-01-43f6fab872ca"

_db_client = None
_genai_client = None
_storage_client = None

def get_genai_client():
    global _genai_client
    if _genai_client is None:
        _genai_client = genai.Client(
            vertexai=True,
            project=FIRESTORE_PROJECT_ID,
            location="global"
        )
    return _genai_client

def get_storage_client():
    global _storage_client
    if _storage_client is None:
        _storage_client = storage.Client(project=FIRESTORE_PROJECT_ID)
    return _storage_client


_db_client = None

def get_db():
    global _db_client
    if _db_client is None:
        _db_client = firestore.Client(project=FIRESTORE_PROJECT_ID)
    return _db_client


def search_luxury_catalog(
    brand: Optional[str] = None,
    category: Optional[str] = None,
    max_price: Optional[float] = None
) -> str:
    """Searches the luxury fashion catalog stored in Firestore for items matching criteria.

    Args:
        brand: Optional brand name to filter by (e.g. Gucci, Saint Laurent, Prada, Chanel, Hermès, Balenciaga).
        category: Optional category to filter by (e.g. Handbags, Footwear, Apparel, Accessories).
        max_price: Optional maximum price in USD.

    Returns:
        A formatted string listing the matching luxury items and their details.
    """
    db = get_db()
    collection_ref = db.collection("luxury_catalog")
    docs = collection_ref.stream()

    results = []
    for doc in docs:
        item = doc.to_dict()
        if brand and brand.lower() not in item.get("brand", "").lower():
            continue
        if category and category.lower() not in item.get("category", "").lower():
            continue
        if max_price is not None and max_price > 0 and item.get("price_usd", 0) > max_price:
            continue
        results.append(item)

    if not results:
        return "No luxury items found matching your search criteria."

    formatted = [f"Found {len(results)} item(s) in luxury catalog:"]
    for idx, item in enumerate(results, 1):
        stock_status = "In Stock" if item.get("in_stock", True) else "Out of Stock"
        img_str = f"\n   Image URL: {item.get('image_url')}" if item.get('image_url') else ""
        formatted.append(
            f"{idx}. [{item.get('brand')}] {item.get('name')} - ${item.get('price_usd'):,.2f} USD\n"
            f"   Category: {item.get('category')} | Aesthetic: {item.get('aesthetic')}\n"
            f"   Materials: {item.get('materials')}{img_str}\n"
            f"   Status: {stock_status} (ID: {item.get('item_id')})"
        )

    return "\n\n".join(formatted)


def add_luxury_item(
    item_id: str,
    brand: str,
    name: str,
    category: str,
    price_usd: float,
    aesthetic: str,
    materials: str,
    in_stock: bool = True
) -> str:
    """Adds a new luxury fashion item to the Firestore catalog.

    Args:
        item_id: Unique identifier for the item (e.g. gucci-marmont-007).
        brand: Luxury fashion house name (e.g. Gucci, Prada, Chanel).
        name: Full product title.
        category: Item category (e.g. Handbags, Footwear, Apparel, Accessories).
        price_usd: Price in US Dollars.
        aesthetic: Aesthetic style description (e.g. Minimalist Luxury, Classic Elegance).
        materials: Fabric or material composition and hardware details.
        in_stock: Availability status (defaults to True).

    Returns:
        Confirmation string indicating successful addition to Firestore.
    """
    db = get_db()
    item_data = {
        "item_id": item_id,
        "brand": brand,
        "name": name,
        "category": category,
        "price_usd": float(price_usd),
        "aesthetic": aesthetic,
        "materials": materials,
        "in_stock": in_stock,
    }

    doc_ref = db.collection("luxury_catalog").document(item_id)
    doc_ref.set(item_data)

    return f"Successfully added '{name}' by {brand} (${price_usd:,.2f}) to Firestore catalog with ID '{item_id}'."


def get_brand_history(brand: str) -> str:
    """Retrieves heritage, creative history, and iconic collections for major luxury houses.

    Args:
        brand: Name of the luxury fashion house (e.g. Gucci, Saint Laurent, Prada, Chanel, Hermès, Balenciaga).

    Returns:
        A narrative overview of the brand's history and aesthetic identity.
    """
    brand_lower = brand.lower()
    if "gucci" in brand_lower:
        return (
            "Gucci was founded in Florence, Italy in 1921 by Guccio Gucci as a leather goods and luggage company. "
            "Famous for its GG monogram, green-red-green web stripe, and horsebit hardware, Gucci represents Italian craft "
            "and maximalist luxury. Iconic pieces include the Bamboo Bag, Jackie 1961, and Dionysus shoulder bag."
        )
    elif "saint laurent" in brand_lower or "ysl" in brand_lower:
        return (
            "Yves Saint Laurent founded the house in Paris in 1961, revolutionizing women's fashion with 'Le Smoking' tuxedo "
            "and introducing ready-to-wear luxury (Rive Gauche). Renowned for Parisian rock-chic elegance and sharp tailoring. "
            "Iconic pieces include Le 5 à 7 bag, Sac de Jour, and Loulou quilted shoulder bag."
        )
    elif "prada" in brand_lower:
        return (
            "Prada was founded in Milan in 1913 by Mario Prada as a leather luxury shop. Miuccia Prada transformed it into "
            "an avant-garde fashion powerhouse in the late 1970s, famously pioneering industrial nylon bags. Known for 'ugly chic', "
            "intellectual minimalism, and Saffiano leather. Iconic items include Monolith loafers, Re-Nylon tote, and Cleo bag."
        )
    elif "chanel" in brand_lower:
        return (
            "House of Chanel was founded by Gabrielle 'Coco' Chanel in Paris in 1910. Chanel liberated women from restrictive corsets, "
            "introducing tweed suits, the Little Black Dress, Chanel No. 5, and the 2.55 quilted flap bag. Under Karl Lagerfeld and successor "
            "directors, Chanel remains the pinnacle of haute couture and French luxury elegance."
        )
    elif "hermès" in brand_lower or "hermes" in brand_lower:
        return (
            "Hermès was established in Paris in 1837 by Thierry Hermès as a harness-making workshop for European nobility. "
            "Famous for master leather craftsmanship, saddle-stitching, orange boxes, and silk scarves. Iconic holy-grail pieces "
            "include the Birkin and Kelly handbags, as well as Oran sandals."
        )
    elif "balenciaga" in brand_lower:
        return (
            "Cristóbal Balenciaga founded the house in San Sebastián, Spain in 1919 before opening in Paris in 1937. Christian Dior called him "
            "'the master of us all' for his architectural silhouettes and sculptural couture. Today under Demna, Balenciaga leads subverted "
            "streetwear and structural avant-garde fashion. Iconic items include the City bag, Triple S sneakers, and Le Cagole bag."
        )
    else:
        return f"Information on '{brand}' is available upon request. Query the luxury catalog for available items."


DUTY_RATES = {
    "uk": {"vat": 0.20, "duty": 0.12, "country_name": "United Kingdom (UK)"},
    "united kingdom": {"vat": 0.20, "duty": 0.12, "country_name": "United Kingdom (UK)"},
    "france": {"vat": 0.20, "duty": 0.12, "country_name": "France"},
    "italy": {"vat": 0.22, "duty": 0.12, "country_name": "Italy"},
    "japan": {"vat": 0.10, "duty": 0.10, "country_name": "Japan"},
    "uae": {"vat": 0.05, "duty": 0.05, "country_name": "United Arab Emirates (UAE)"},
    "dubai": {"vat": 0.05, "duty": 0.05, "country_name": "United Arab Emirates (UAE)"},
    "canada": {"vat": 0.05, "duty": 0.18, "country_name": "Canada"},
    "australia": {"vat": 0.10, "duty": 0.05, "country_name": "Australia"},
}


def calculate_luxury_import_duties(price_usd: float, destination_country: str) -> str:
    """Calculates estimated import duties, local VAT/GST, and total landed cost for luxury goods.

    Args:
        price_usd: The retail price of the luxury item in USD.
        destination_country: Target destination country (e.g. UK, France, Italy, Japan, UAE, Canada, Australia).

    Returns:
        A breakdown of calculated duties, local tax, and total landed cost.
    """
    key = destination_country.strip().lower()
    rate = DUTY_RATES.get(key, {"vat": 0.15, "duty": 0.10, "country_name": destination_country.title()})

    duty_amount = price_usd * rate["duty"]
    vat_amount = (price_usd + duty_amount) * rate["vat"]
    total_landed_cost = price_usd + duty_amount + vat_amount

    return (
        f"Landed Cost Breakdown for {rate['country_name']}:\n"
        f"  - Item Retail Price: ${price_usd:,.2f} USD\n"
        f"  - Estimated Luxury Import Duty ({rate['duty']*100:.0f}%): ${duty_amount:,.2f} USD\n"
        f"  - Local VAT/GST ({rate['vat']*100:.0f}%): ${vat_amount:,.2f} USD\n"
        f"  - Total Estimated Landed Cost: ${total_landed_cost:,.2f} USD"
    )


def get_live_exchange_rates(base_currency: str = "USD") -> str:
    """Fetches real-time live currency exchange rates from a free public API for luxury cross-border shopping.

    Args:
        base_currency: Base 3-letter currency code (e.g. USD, EUR, GBP, JPY). Defaults to 'USD'.

    Returns:
        A formatted summary of live exchange rates for major luxury fashion capitals.
    """
    base = base_currency.strip().upper()
    api_key = os.environ.get("EXCHANGE_RATE_API_KEY")

    if api_key:
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}"
    else:
        url = f"https://open.er-api.com/v6/latest/{base}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "LuxuryFashionStylist/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))

        if data.get("result") != "success":
            return f"Unable to fetch exchange rates for {base}: {data.get('error-type', 'Unknown error')}"

        rates = data.get("rates", {})
        target_currencies = ["EUR", "GBP", "JPY", "AED", "CAD", "AUD", "CHF", "CNY", "HKD"]

        lines = [f"Live Foreign Exchange Rates (Base: 1 {base}):"]
        for symbol in target_currencies:
            if symbol in rates:
                lines.append(f"  - 1 {base} = {rates[symbol]:,.4f} {symbol}")

        return "\n".join(lines)
    except Exception as e:
        return f"Error fetching live exchange rates: {str(e)}"


def geocode_address(address: str) -> str:
    """Uses Google Maps Geocoding API to convert an address or location name into geographic coordinates.

    Args:
        address: The address or place name to geocode (e.g. 'Via Montenapoleone, Milan, Italy' or 'Fifth Avenue, NYC').

    Returns:
        A formatted string containing formatted address, latitude, and longitude coordinates.
    """
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return "Error: GOOGLE_MAPS_API_KEY environment variable is not configured."

    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={urllib.parse.quote(address)}&key={api_key}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "LuxuryFashionStylist/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))

        if data.get("status") != "OK" or not data.get("results"):
            return f"Geocoding failed for '{address}': {data.get('status', 'NO_RESULTS')}"

        result = data["results"][0]
        fmt_address = result.get("formatted_address", address)
        loc = result.get("geometry", {}).get("location", {})
        lat, lng = loc.get("lat"), loc.get("lng")

        return (
            f"Geocoding Results for '{address}':\n"
            f"  - Formatted Address: {fmt_address}\n"
            f"  - Latitude: {lat}\n"
            f"  - Longitude: {lng}"
        )
    except Exception as e:
        return f"Error calling Geocoding API: {str(e)}"


def find_nearby_places(
    latitude: float,
    longitude: float,
    place_type: str = "clothing_store",
    radius_meters: float = 1000.0
) -> str:
    """Uses Google Places API (New) to search for nearby places of a given type around coordinates.

    Args:
        latitude: Target latitude coordinate.
        longitude: Target longitude coordinate.
        place_type: Type of place to search for (e.g. 'clothing_store', 'shopping_mall', 'shoe_store', 'store').
        radius_meters: Search radius in meters (defaults to 1000 meters).

    Returns:
        A formatted list of nearby places returning key fields (displayName, formattedAddress, location coordinates).
    """
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return "Error: GOOGLE_MAPS_API_KEY environment variable is not configured."

    url = "https://places.googleapis.com/v1/places:searchNearby"
    payload = {
        "includedTypes": [place_type],
        "maxResultCount": 5,
        "locationRestriction": {
            "circle": {
                "center": {"latitude": float(latitude), "longitude": float(longitude)},
                "radius": float(radius_meters),
            }
        },
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location",
        "User-Agent": "LuxuryFashionStylist/1.0",
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))

        places = data.get("places", [])
        if not places:
            return f"No nearby '{place_type}' places found within {radius_meters}m of ({latitude}, {longitude})."

        lines = [f"Found {len(places)} nearby '{place_type}' place(s):"]
        for idx, p in enumerate(places, 1):
            name = p.get("displayName", {}).get("text", "Unknown Name")
            address = p.get("formattedAddress", "N/A")
            loc = p.get("location", {})
            plat, plng = loc.get("latitude"), loc.get("longitude")
            lines.append(
                f"{idx}. {name}\n"
                f"   Address: {address}\n"
                f"   Location: ({plat}, {plng})"
            )

        return "\n\n".join(lines)
    except Exception as e:
        return f"Error calling Places API (New): {str(e)}"


async def generate_luxury_item_image(
    prompt: str,
    filename: str = "luxury_item.jpg",
    tool_context: ToolContext = None
) -> str:
    """Generates an image for a luxury fashion item using gemini-3.1-flash-lite-image model in global region, saves it with tool_context.save_artifact, and uploads it to Cloud Storage.

    Args:
        prompt: Detailed description of the luxury fashion item to generate (e.g. 'A classic Chanel 2.55 flap bag in black quilted lambskin').
        filename: Target filename for the saved artifact and GCS object (defaults to 'luxury_item.jpg').
        tool_context: Context automatically provided by ADK to save session artifacts.

    Returns:
        The public HTTPS URL (https://storage.googleapis.com/<bucket>/<object>) of the generated image hosted on Cloud Storage.
    """
    client = get_genai_client()

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-image",
            contents=f"Generate a high quality product photograph: {prompt}",
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"]
            )
        )
    except Exception as e:
        return f"Error generating image with gemini-3.1-flash-lite-image: {str(e)}"

    image_bytes = None
    mime_type = "image/jpeg"

    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                image_bytes = part.inline_data.data
                if part.inline_data.mime_type:
                    mime_type = part.inline_data.mime_type
                break

    if not image_bytes:
        return f"Error: Image generation model returned no image bytes for prompt '{prompt}'."

    # 1. Save with tool_context.save_artifact if context is present
    if tool_context is not None:
        try:
            artifact_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
            await tool_context.save_artifact(filename=filename, artifact=artifact_part)
        except Exception:
            pass



    # 2. Upload image bytes to public Cloud Storage bucket
    try:
        storage_cli = get_storage_client()
        bucket = storage_cli.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(image_bytes, content_type=mime_type)

        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"
        return public_url
    except Exception as e:
        return f"Error uploading image to Cloud Storage: {str(e)}"


async def generate_luxury_item_video(
    prompt: str,
    filename: str = "luxury_item_showcase.mp4",
    tool_context: ToolContext = None
) -> str:
    """Generates a short video for a luxury fashion item using Google's Omni model (gemini-omni-flash-preview) in the global region, saves it with tool_context.save_artifact, and uploads it to Cloud Storage.

    Args:
        prompt: Detailed description of the luxury fashion item video to generate (e.g. 'A 5-second cinematic runway showcase of a Chanel tweed jacket').
        filename: Target filename for the saved video artifact and GCS object (defaults to 'luxury_item_showcase.mp4').
        tool_context: Context automatically provided by ADK to save session artifacts.

    Returns:
        The public HTTPS URL (https://storage.googleapis.com/<bucket>/<object>) of the generated video hosted on Cloud Storage.
    """
    client = get_genai_client()
    video_bytes = None
    mime_type = "video/mp4"

    try:
        response = client.models.generate_content(
            model="gemini-omni-flash-preview",
            contents=f"Generate a short video showcasing this luxury item: {prompt}",
            config=types.GenerateContentConfig(
                response_modalities=["VIDEO"]
            )
        )
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    video_bytes = part.inline_data.data
                    if part.inline_data.mime_type:
                        mime_type = part.inline_data.mime_type
                    break
    except Exception as e:
        try:
            interaction = client.interactions.create(
                model="gemini-omni-flash-preview",
                input=f"Generate a short video showcasing this luxury item: {prompt}",
                generation_config={"response_modalities": ["VIDEO"]}
            )
            if hasattr(interaction, "outputs") and interaction.outputs:
                for out in interaction.outputs:
                    if hasattr(out, "data") and out.data:
                        video_bytes = out.data
                        break
        except Exception as inner_e:
            return f"Error generating video with gemini-omni-flash-preview: {str(e)} | {str(inner_e)}"

    if not video_bytes:
        return f"Error: Video generation model returned no video bytes for prompt '{prompt}'."

    # 1. Save with tool_context.save_artifact if context is present
    if tool_context is not None:
        try:
            artifact_part = types.Part.from_bytes(data=video_bytes, mime_type=mime_type)
            await tool_context.save_artifact(filename=filename, artifact=artifact_part)
        except Exception:
            pass

    # 2. Upload video bytes to public Cloud Storage bucket
    try:
        storage_cli = get_storage_client()
        bucket = storage_cli.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(video_bytes, content_type=mime_type)

        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"
        return public_url
    except Exception as e:
        return f"Error uploading video to Cloud Storage: {str(e)}"






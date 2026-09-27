# ⚜️ Haute Stylist — Luxury Fashion Concierge & Personal Stylist

**Haute Stylist** is an elite, AI-powered Luxury Fashion Concierge and Personal Stylist built with Google's **Agent Development Kit (ADK)**, **Gemini 2.5/3.1** models, **Firestore**, and **Vertex AI Memory Bank**.

It provides discerning clients with personalized luxury styling recommendations, brand heritage insights, Firestore catalog queries, international import duty & currency calculations, boutique locator mapping, studio product image generation, and runway video creation.

---

## 📹 Demo Video

Watch Haute Stylist in action (recorded with Playwright and scored with Google **Lyria (`lyria-002`)** AI upbeat lo-fi background music):

> 🎬 **Direct Public Video Stream (MP4)**: [https://storage.googleapis.com/luxury-fashion-media-qwiklabs-gcp-01-43f6fab872ca/luxury_stylist_demo.mp4](https://storage.googleapis.com/luxury-fashion-media-qwiklabs-gcp-01-43f6fab872ca/luxury_stylist_demo.mp4)
> 📁 **Demo Video Folder in Repository**: [`demo video/`](./demo%20video/)
>   - MP4 Format: [`demo video/luxury_stylist_demo.mp4`](./demo%20video/luxury_stylist_demo.mp4)
>   - WebM Format: [`demo video/luxury_stylist_demo.webm`](./demo%20video/luxury_stylist_demo.webm)

---

## 🌟 Key Features

1. **🏛️ Exclusive Luxury Fashion Catalog (Firestore)**
   - Search across top luxury brands (*Chanel, Hermès, Gucci, Prada, Saint Laurent, Balenciaga, Cartier, Louis Vuitton*).
   - Filter items by category, price, material, and brand. Add new luxury pieces directly to the Firestore collection.

2. **📜 Brand Heritage & History**
   - In-depth brand stories, founding dates, creative directors, and house signatures for iconic fashion houses.

3. **🛃 International Import Duty & Currency Conversion**
   - Real-time calculation of customs duties, VAT/sales taxes, and import fees across US, UK, EU, Japan, UAE, and global markets.
   - Live foreign currency exchange rate conversions.

4. **📍 Boutique Locator & Geocoding**
   - Address geocoding and Google Places API integration to locate flagship boutiques and ateliers near any street address or city.

5. **🎨 Studio Product Image Generation**
   - Studio-quality product photography generation using Gemini image models (`gemini-3.1-flash-lite-image` in `global` region).
   - Artifact saving & direct public Cloud Storage uploads.

6. **🎥 Runway Video Showcase Generation**
   - Runway and product video creation using Google's Omni model (`gemini-omni-flash-preview` in `global` region).
   - Dual artifact saving + GCS public hosting.

7. **🧠 Long-Term Memory & Sensitivity Tracking (Memory Bank)**
   - Persistent cross-session recollection of client preferences, sizing, and material sensitivities/allergies (e.g. wool, nickel, latex, exotic leathers).

8. **✨ Adaptive A2UI Interface**
   - Rendered using Google A2UI (Agent-to-UI) declarative JSON component cards (`Card`, `Column`, `Row`, `Text`, `Image`).

---

## 📁 Project Structure

```
luxury-fashion-stylist/
├── app/                        # Core ADK Agent Implementation
│   ├── agent.py               # Main agent configuration & system prompt
│   ├── tools.py               # 9 Custom Tools (Firestore, Places, Exchange, Duty, Image, Video, Memory)
│   ├── a2ui_utils.py          # A2UI response formatting callback
│   └── __init__.py
├── frontend/                   # Custom FastAPI Chat Frontend
│   ├── main.py                # FastAPI proxy server for ADK Agent Engine
│   └── static/
│       └── index.html         # Regal metallic gold luxury concierge UI
├── demo video/                 # Dedicated Demo Video Folder
│   ├── luxury_stylist_demo.mp4 # Universal MP4 video (H.264 + AAC + Lyria AI Music)
│   └── luxury_stylist_demo.webm# WebM VP9 demo recording
├── tests/                      # Pytest unit and integration test suite
│   ├── unit/
│   └── integration/
├── project_brief.md            # App concept, target audience, and specification
├── pyproject.toml              # Python dependencies (ADK, google-genai, google-cloud-storage, etc.)
└── agents-cli-manifest.yaml    # ADK manifest configuration
```

---

## 🚀 Quick Start & Local Execution

### Prerequisites
- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) Python package manager

### 1. Install Dependencies
```bash
uv sync
```

### 2. Set Up Environment
```bash
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
export GOOGLE_CLOUD_LOCATION="us-east1"
```

### 3. Run Agent Locally
To launch the agent interactive playground:
```bash
uv run adk web app/
```

To run the custom FastAPI luxury chat UI:
```bash
cd frontend/
uv run uvicorn main:app --port 8080 --host 127.0.0.1
```
Then open `http://localhost:8080` in your browser.

---

## 🛠️ Testing
Run the unit and integration test suite:
```bash
uv run pytest tests/unit tests/integration
```

---

## 📄 License
Licensed under the Apache License 2.0.

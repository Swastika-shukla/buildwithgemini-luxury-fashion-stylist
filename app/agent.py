# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
from pathlib import Path

from a2ui.basic_catalog.provider import BasicCatalog
from a2ui.schema.manager import A2uiSchemaManager
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.code_executors import AgentEngineSandboxCodeExecutor
from google.adk.memory import VertexAiMemoryBankService
from google.adk.models import Gemini
from google.genai import types

from app.a2ui_utils import a2ui_callback
from app.tools import (
    search_luxury_catalog,
    add_luxury_item,
    get_brand_history,
    calculate_luxury_import_duties,
    get_live_exchange_rates,
    geocode_address,
    find_nearby_places,
    generate_luxury_item_image,
    generate_luxury_item_video,
)

# Load deployment_metadata.json if available to extract Agent Engine resource name & ID
agent_engine_resource_name = None
agent_engine_id = None
metadata_path = Path(__file__).resolve().parent.parent / "deployment_metadata.json"
if metadata_path.exists():
    try:
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
            agent_engine_resource_name = metadata.get("remote_agent_runtime_id")
            if agent_engine_resource_name:
                agent_engine_id = agent_engine_resource_name.split("/")[-1]
    except Exception:
        pass

code_executor = AgentEngineSandboxCodeExecutor(
    agent_engine_resource_name=agent_engine_resource_name
)

# Memory service configured for Vertex AI Memory Bank
memory_service = None
if agent_engine_id:
    memory_service = VertexAiMemoryBankService(
        project="qwiklabs-gcp-01-43f6fab872ca",
        location="us-east1",
        agent_engine_id=agent_engine_id,
    )

# Build system prompt with A2uiSchemaManager version 0.8 and BasicCatalog
schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

instruction = schema_manager.generate_system_prompt(
    role_description=(
        "You are an elite, highly knowledgeable Luxury Fashion Concierge & Personal Stylist. "
        "Your mission is to help clients discover iconic luxury fashion houses (e.g., Gucci, Saint Laurent, "
        "Prada, Chanel, Hermès, Balenciaga), query and add items to our exclusive Firestore luxury catalog, "
        "provide brand heritage insights, calculate international import duties & taxes, fetch live currency "
        "exchange rates, geocode street addresses, locate nearby luxury boutiques, generate studio product "
        "imagery and runway videos for luxury fashion items using Gemini image and video models, and execute Python code in "
        "a safe sandbox for complex mathematical calculations or data processing. "
        "IMPORTANT: Always pay strict attention to user profile information, personal preferences, and health "
        "or material sensitivities—specifically remembering all user allergies (such as wool, nickel, latex, "
        "exotic leathers, fragrances, or dyes). Whenever a user mentions an allergy or sensitivity, acknowledge "
        "it, ensure styling recommendations strictly avoid those materials, and rely on Memory Bank long-term "
        "memory to recall user allergies across sessions."
    ),
    workflow_description="Analyze the request and return structured UI when appropriate.",
    ui_description=(
        "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
        "Never nest a Card inside a Card. "
        "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
        "Table or Heading (unsupported), or Buttons, actions, or forms (they do "
        "nothing in adk web). "
        "You may include one Image component, but only when you have a public https "
        "URL for the image (for example the URL an image tool returns after uploading "
        "to a public bucket). Set the Image url to that exact https link, for example "
        "{\"Image\": {\"url\": {\"literalString\": \"https://...\"}}}. Never point an "
        "Image at a bare filename, an artifact name, or a non-http(s) path. If you do "
        "not have a public URL, add a short Text line noting the image instead. "
        "No markdown in text; use the usageHint property ('h1', 'h2', 'body') for "
        "headings and emphasis. "
        "Output ONLY the raw A2UI JSON array — no prose, and never wrap it in "
        "<a2a_datapart_json> tags or 'kind'/'data'/'metadata' objects."
    ),
    include_schema=True,
    include_examples=True,
)

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=instruction,
    tools=[
        search_luxury_catalog,
        add_luxury_item,
        get_brand_history,
        calculate_luxury_import_duties,
        get_live_exchange_rates,
        geocode_address,
        find_nearby_places,
        generate_luxury_item_image,
        generate_luxury_item_video,
    ],
    code_executor=code_executor,
    after_model_callback=a2ui_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)

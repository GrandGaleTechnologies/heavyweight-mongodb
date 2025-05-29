# 🚀 Heavyweight Mongodb FastAPI Template

A robust, production-ready FastAPI template using MongoDB for high-performance, schema-flexible applications. Built on GrandGale Technologies' coding standards, it provides a modular structure, async Motor integration, automatic collection/index setup, and Logfire logging.

Inspired by [FastAPI guidelines](https://github.com/GrandGaleTechnologies/fastapi_guidelines) and enterprise best practices, it’s designed for rapid development and scalable deployments.

## 📑 Table of Contents

* [✨ Features](#-features)
* [📁 Project Structure](#-project-structure)
* [💡 Getting Started](#-getting-started)
* [⚙️ Database Setup](#️-database-setup)
* [🛠️ Example Module Snippets](#️-example-module-snippets)
* [🎗 License](#-license)
* [🤝 Contribute](#-contribute)
* [📬 Contact](#-contact)

## ✨ Features

* **MongoDB** integration via async Motor client
* **Automatic collections & index creation** on startup (`setup_mongodb`)
* **Optional Logfire** instrumentation: set `LOGFIRE_TOKEN` to enable logging; ignored if unset ([Logfire docs](https://logfire.io/docs))
* **Modular codebase** following GrandGale standards
* **Optional `uvloop`** support for enhanced async performance (Linux/macOS)

## 📁 Project Structure

```plaintext
.vscode/
app/
  core/
    database.py       # get_client(), setup_mongodb(), COLLECTIONS
    settings.py       # pydantic settings loader (MONGODB_URL, JWT secrets, LOGFIRE_TOKEN)
    handlers.py       # Exception handlers

  sample_module/
    __init__.py
    apis.py           # Where our api endpoints go
    db.py             # Where we keep our collection getters i.e. get_user_collection()
    exceptions.py     # Where we keep our module specific exceptions i.e. UserNotFound
    schemas.py        # base, doc, create, edit, response, paginated schemas
    selectors.py      # data retrieval functions (e.g., get_user_by_id)
    services.py       # business logic, CRUD operations

common/
  __init__.py
  annotations.py      # General annotations i.e. PaginationParams
  depdencies.py       # General dependencies i.e. get_pagination_params
  exceptions.py       # General exceptions i.e. NotFound
  security.py         # password hashing, token utilities
  pagination.py       # pagination params & metadata helper
  types.py            # General types i.e. PaginationParamsType

tests/
  __init__.py

.flake8
.gitignore
.pylintrc
docker-compose.yml
Dockerfile
.env_sample
pytest.init
railway.toml
README.md
requirements.txt
start.sh
```

## 💡 Getting Started

### Prerequisites

* Docker & Docker Compose (optional)
* using pip

### 1. Clone the repo

```bash
git clone https://github.com/GrandGaleTechnologies/heavyweight-mongodb
cd heavyweight-mongodb
```

### 2. Install dependencies with `pip`

```bash
NOTE: py or python3 depending on your OS
$ py -m venv .venv
$ .venv\Scripts\activate # for Windows
$ pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env_sample` to `.env` and set:

```dotenv
DEBUG=true
LOGFIRE_TOKEN=    # optional: enable Logfire if set
MONGODB_URL=mongodb://<user>:<pass>@host:27017
```

### 4. Startup: automatic DB & index setup

The `setup_mongodb()` function runs at application startup to create any missing collections and indexes defined in `app.core.database.COLLECTIONS`.

### 5. Run the application

#### Development mode

```bash
$ fastapi dev
```

#### Production mode

```bash
$ fastapi run
```

## ⚙️ Database Setup (app/core/database.py)

```python
from functools import lru_cache
from pymongo import AsyncIOMotorClient
from app.core.settings import get_settings

settings = get_settings()
DBNAME = "main"
COLLECTIONS = {"test": ["id"]}

@lru_cache()
def get_client():
    return AsyncIOMotorClient(
        settings.MONGODB_URL,
        tz_aware=True,
        uuidRepresentation="standard",
    )

async def setup_mongodb():
    client = get_client()
    db = client[DBNAME]
    existing = await db.list_collection_names()
    for name, indexes in COLLECTIONS.items():
        if name not in existing:
            col = await db.create_collection(name)
            for idx in indexes:
                await col.create_index(idx)
    return db
```

*Add new collections or indexes by updating `COLLECTIONS` and restarting the app.*

## 🛠️ Example Module Snippets

### `app/sample_module/db.py`

```python
from functools import lru_cache
from app.core.database import get_client

@lru_cache()
def get_user_collection():
    return get_client()["main"].get_collection("test")
```

This is used to get collections, by wrapping it in a lru_cache it returns the same collections obj on subsequent calls *curtesy of fastapi docs on pydantic-settings but we still arent super sure if this has any side effects.

### `app/sample_module/selectors.py`

```python
async def get_user_by_id(id: str, raise_exc=True):
    col = get_user_collection()
    user = await col.find_one({"id": id})
    if not user and raise_exc:
        raise UserNotFound()
    return user
```

### `app/sample_module/apis.py`

```python
@router.get("/{user_id}/", response_model=UserResponse)
async def route_user_details(user_id: str):
    user = await selectors.get_user_by_id(user_id)
    return {"data": user}

@router.get("", response_model=PaginatedUserListResponse)
async def route_user_list(pag: PaginationParams):
    col = get_user_collection()
    filters = {}  # build filters...
    cursor = col.find(filters).sort("first_name", ASCENDING)
    items = [doc async for doc in cursor.skip(...).limit(...)]
    total = await col.count_documents(filters)
    return {"data": items, "meta": get_pagination_metadata_mongo(total, len(items), pag)}
```

## 🎗 License

MIT License — see [LICENSE](LICENSE).

## 🤝 Contribute

Fork, branch, and PR. Follow [FastAPI guidelines](https://github.com/GrandGaleTechnologies/fastapi_guidelines).

## 📬 Contact

* **Name:** GrandGale Technologies
* **Email:** [admin@grandgale.tech](mailto:angobello0@gmail.com)
* **GitHub:** [https://github.com/GrandGaleTechnologies](https://github.com/GrandGaleTechnologies)
* **LinkedIn:** [https://linkedin.com/in/angobello0](https://linkedin.com/in/angobello0)

# Project Structure

## Overview
The API endpoints have been organized into separate modules for better maintainability and scalability.

## Directory Structure

```
bomach_backend_services/
├── config/                          # Django project configuration
│   ├── __init__.py
│   ├── settings.py                  # Django settings with CORS, decouple
│   ├── urls.py                      # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── api/                             # Main API application
│   ├── __init__.py
│   ├── api.py                       # Main API router (registers all endpoints)
│   ├── models.py                    # All database models
│   ├── schemas.py                   # Pydantic schemas for validation
│   ├── admin.py                     # Django admin configuration
│   ├── apps.py
│   ├── tests.py
│   │
│   ├── endpoints/                   # API endpoint modules
│   │   ├── __init__.py
│   │   ├── categories.py            # ServiceCategory CRUD endpoints
│   │   ├── services.py              # Service CRUD endpoints
│   │   ├── clients.py               # Client CRUD endpoints
│   │   ├── leads.py                 # ServiceLead CRUD endpoints
│   │   ├── quotes.py                # Quote CRUD endpoints
│   │   ├── orders.py                # ServiceOrder CRUD endpoints
│   │   ├── invoices.py              # Invoice CRUD endpoints
│   │   ├── payments.py              # Payment CRUD endpoints
│   │   └── stats.py                 # Statistics endpoint
│   │
│   └── migrations/                  # Database migrations
│       ├── __init__.py
│       └── 0001_initial.py
│
├── venv/                            # Virtual environment
├── manage.py                        # Django management script
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── README.md                        # Project documentation
├── API_EXAMPLES.md                  # API usage examples
└── STRUCTURE.md                     # This file
```

## File Responsibilities

### Main API File
- **api/api.py**: Main API entry point that registers all endpoint routers

### Endpoint Files (api/endpoints/)
Each endpoint file contains CRUD operations for a specific resource:

1. **categories.py**
   - List all categories
   - Create category
   - Get category by ID
   - Update category
   - Delete category

2. **services.py**
   - List services (with filters: status, category, search)
   - Create service
   - Get service by ID
   - Update service
   - Delete service

3. **clients.py**
   - List clients (with filters: verification_status, search)
   - Create client
   - Get client by ID
   - Update client
   - Delete client

4. **leads.py**
   - List service leads (with filters: status, client_id, search)
   - Create lead
   - Get lead by ID
   - Update lead
   - Delete lead

5. **quotes.py**
   - List quotes (with filters: status, client_id)
   - Create quote
   - Get quote by ID
   - Update quote
   - Delete quote

6. **orders.py**
   - List service orders (with filters: order_status, payment_status, client_id)
   - Create order
   - Get order by ID
   - Update order
   - Delete order

7. **invoices.py**
   - List invoices (with filters: status, client_id, search)
   - Create invoice with items
   - Get invoice by ID
   - Update invoice
   - Delete invoice

8. **payments.py**
   - List payments (with filter: invoice_id)
   - Create payment (auto-updates invoice)
   - Get payment by ID
   - Delete payment

9. **stats.py**
   - Get overall statistics (counts of services, orders, quotes, invoices)

## Benefits of This Structure

1. **Separation of Concerns**: Each endpoint file handles one resource
2. **Maintainability**: Easy to locate and modify specific endpoints
3. **Scalability**: Simple to add new endpoint modules
4. **Testability**: Each module can be tested independently
5. **Readability**: Clear organization makes onboarding easier
6. **Modularity**: Endpoints can be enabled/disabled by commenting out router registration

## How It Works

1. Each endpoint file creates a `Router()` instance
2. Endpoints are decorated with `@router.get()`, `@router.post()`, etc.
3. The main `api.py` imports all routers
4. Routers are registered with the main API using `api.add_router()`
5. URL prefixes are applied during registration (e.g., `/categories`, `/services`)

## Adding New Endpoints

To add new endpoints:

1. Create a new file in `api/endpoints/` (e.g., `reports.py`)
2. Import necessary dependencies and create a router:
   ```python
   from ninja import Router
   router = Router()
   ```
3. Define your endpoints using the router
4. Import the new module in `api/api.py`
5. Register the router: `api.add_router("/reports", reports.router)`

## Example Endpoint File Structure

```python
from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404

from ..models import MyModel
from ..schemas import MyModelIn, MyModelOut

router = Router()

@router.get("", response=List[MyModelOut], tags=["MyModel"])
def list_items(request):
    return MyModel.objects.all()

@router.post("", response=MyModelOut, tags=["MyModel"])
def create_item(request, payload: MyModelIn):
    return MyModel.objects.create(**payload.dict())
```

## URL Structure

All API endpoints are prefixed with `/api/`:

- `/api/health` - Health check
- `/api/stats` - Statistics
- `/api/categories/` - Category endpoints
- `/api/services/` - Service endpoints
- `/api/clients/` - Client endpoints
- `/api/leads/` - Lead endpoints
- `/api/quotes/` - Quote endpoints
- `/api/orders/` - Order endpoints
- `/api/invoices/` - Invoice endpoints
- `/api/payments/` - Payment endpoints

Interactive documentation: `/api/docs`

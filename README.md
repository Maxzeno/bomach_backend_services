# BOMACH Backend Services

Service Management API built with Django and Django Ninja.

## Features

This backend service manages:
- **Service Catalog**: Services and categories
- **Client Management**: Client information and verification
- **Service Leads**: Lead tracking and qualification
- **Quotes**: Quote generation and management
- **Service Orders**: Order tracking with status management
- **Invoicing**: Invoice generation with line items and tax calculation
- **Payments**: Payment tracking and invoice updates

## Models

### ServiceCategory
- Service categorization (e.g., Engineering, Construction)

### Service
- Service catalog with pricing and delivery time
- Status: active, inactive, draft
- Links to external User service via `created_by` field

### Client
- Client/customer information
- Verification status: verified, pending, rejected
- Links to external User service via `created_by` field

### ServiceLead
- Sales leads tracking
- Status: new, qualified, contacted, proposal_sent, converted, lost
- Links to Client and Service

### Quote
- Quote generation for services
- Auto-generated quote numbers (QTE-XXXXXXXXXXXX)
- Status: draft, sent, accepted, rejected, expired

### ServiceOrder
- Service orders from accepted quotes
- Auto-generated order numbers (ORD-XXXXXXXXXXXX)
- Order status: pending, accepted, in_progress, completed, cancelled
- Payment status: unpaid, partial, paid
- Links to external Employee service via `assigned_to` field

### Invoice
- Invoice generation with automatic tax calculation
- Auto-generated invoice numbers (SRV-YYYY-MM-XXXXXXXX)
- Status: draft, sent, viewed, partially_paid, paid, overdue, cancelled
- Tracks payment progress and balance
- Can link to ServiceOrder or ServiceLead

### InvoiceItem
- Line items for invoices
- Automatic total calculation

### Payment
- Payment tracking for invoices
- Auto-generated payment references (PAY-XXXXXXXXXXXX)
- Methods: cash, bank_transfer, cheque, card, mobile_money, other
- Automatically updates invoice payment status

## API Endpoints

### Health
- `GET /api/health` - Health check

### Statistics
- `GET /api/stats` - Get overall statistics

### Categories
- `GET /api/categories` - List all categories
- `POST /api/categories` - Create category
- `GET /api/categories/{id}` - Get category details
- `PUT /api/categories/{id}` - Update category
- `DELETE /api/categories/{id}` - Delete category

### Services
- `GET /api/services` - List services (filter: status, category_id, search)
- `POST /api/services` - Create service
- `GET /api/services/{id}` - Get service details
- `PUT /api/services/{id}` - Update service
- `DELETE /api/services/{id}` - Delete service

### Clients
- `GET /api/clients` - List clients (filter: verification_status, search)
- `POST /api/clients` - Create client
- `GET /api/clients/{id}` - Get client details
- `PUT /api/clients/{id}` - Update client
- `DELETE /api/clients/{id}` - Delete client

### Service Leads
- `GET /api/leads` - List leads (filter: status, client_id, search)
- `POST /api/leads` - Create lead
- `GET /api/leads/{id}` - Get lead details
- `PUT /api/leads/{id}` - Update lead
- `DELETE /api/leads/{id}` - Delete lead

### Quotes
- `GET /api/quotes` - List quotes (filter: status, client_id)
- `POST /api/quotes` - Create quote
- `GET /api/quotes/{id}` - Get quote details
- `PUT /api/quotes/{id}` - Update quote
- `DELETE /api/quotes/{id}` - Delete quote

### Service Orders
- `GET /api/orders` - List orders (filter: order_status, payment_status, client_id)
- `POST /api/orders` - Create order
- `GET /api/orders/{id}` - Get order details
- `PUT /api/orders/{id}` - Update order
- `DELETE /api/orders/{id}` - Delete order

### Invoices
- `GET /api/invoices` - List invoices (filter: status, client_id, search)
- `POST /api/invoices` - Create invoice with items
- `GET /api/invoices/{id}` - Get invoice details
- `PUT /api/invoices/{id}` - Update invoice
- `DELETE /api/invoices/{id}` - Delete invoice

### Payments
- `GET /api/payments` - List payments (filter: invoice_id)
- `POST /api/payments` - Create payment (auto-updates invoice)
- `GET /api/payments/{id}` - Get payment details
- `DELETE /api/payments/{id}` - Delete payment

## Interactive API Documentation

Once the server is running:
- Swagger UI: `http://localhost:8000/api/docs`
- OpenAPI Schema: `http://localhost:8000/api/openapi.json`

## Setup & Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configure environment** (copy .env.example to .env):
```bash
cp .env.example .env
```

3. **Run migrations**:
```bash
python manage.py migrate
```

4. **Create superuser** (optional):
```bash
python manage.py createsuperuser
```

5. **Run development server**:
```bash
python manage.py runserver
```

## Microservices Architecture

This service handles **Service Management**. It references external services:
- **User Service**: Stores user and employee data
  - Referenced via `created_by` fields (stores user IDs)
  - Referenced via `assigned_to` field in ServiceOrder (stores employee IDs)

## Key Features

### Auto-generated Numbers
- Quote numbers: `QTE-XXXXXXXXXXXX`
- Order numbers: `ORD-XXXXXXXXXXXX`
- Invoice numbers: `SRV-YYYY-MM-XXXXXXXX`
- Payment references: `PAY-XXXXXXXXXXXX`

### Automatic Calculations
- **Invoice**: Tax and total amounts calculated on save
- **InvoiceItem**: Total calculated from quantity × unit_price
- **Invoice**: Balance and payment progress properties
- **Payment**: Automatically updates invoice payment status

### Filtering & Search
- Services: Filter by status, category; search by name/description
- Clients: Filter by verification status; search by name/email/phone
- Leads: Filter by status, client; search by client name/notes
- Quotes: Filter by status, client
- Orders: Filter by order status, payment status, client
- Invoices: Filter by status, client; search by invoice number/client name

## Admin Panel

Access Django admin at `http://localhost:8000/admin/` to manage all entities with a user-friendly interface.

## Technology Stack

- **Django 5.2.9**: Web framework
- **Django Ninja 1.5.1**: REST API framework
- **django-cors-headers**: CORS support
- **python-decouple**: Environment configuration
- **grpcio & grpcio-tools**: gRPC support (ready for inter-service communication)

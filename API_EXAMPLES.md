# API Examples

## Base URL
```
http://localhost:8000/api
```

## Interactive Documentation
Visit `http://localhost:8000/api/docs` for interactive Swagger UI documentation.

---

## 1. Health Check

### Check API Status
```bash
GET /api/health

Response:
{
  "status": "ok",
  "message": "Service is running"
}
```

---

## 2. Statistics

### Get Overall Statistics
```bash
GET /api/stats

Response:
{
  "total_services": 452,
  "total_orders": 452,
  "total_quotes": 452,
  "total_invoices": 452
}
```

---

## 3. Service Categories

### List All Categories
```bash
GET /api/categories

Response:
[
  {
    "id": 1,
    "name": "Engineering",
    "description": "Engineering services",
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-01-15T10:00:00Z"
  }
]
```

### Create Category
```bash
POST /api/categories
Content-Type: application/json

{
  "name": "Engineering",
  "description": "Engineering and technical services"
}
```

### Update Category
```bash
PUT /api/categories/1
Content-Type: application/json

{
  "name": "Engineering Services",
  "description": "Professional engineering services"
}
```

### Delete Category
```bash
DELETE /api/categories/1
```

---

## 4. Services

### List Services
```bash
GET /api/services
GET /api/services?status=active
GET /api/services?category_id=1
GET /api/services?search=geotechnical

Response:
[
  {
    "id": 1,
    "name": "Geotechnical Investigation",
    "category": {
      "id": 1,
      "name": "Engineering",
      ...
    },
    "description": "Soil analysis and foundation engineering services",
    "base_price": "300000.00",
    "delivery_time": "3-5 weeks",
    "status": "active",
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-01-15T10:00:00Z",
    "created_by": "user_123"
  }
]
```

### Create Service
```bash
POST /api/services
Content-Type: application/json

{
  "name": "Geotechnical Investigation",
  "category_id": 1,
  "description": "Soil analysis and foundation engineering services for construction and infrastructure projects.",
  "base_price": "300000.00",
  "delivery_time": "3-5 weeks",
  "status": "active",
  "created_by": "user_123"
}
```

### Get Service Details
```bash
GET /api/services/1
```

### Update Service
```bash
PUT /api/services/1
Content-Type: application/json

{
  "base_price": "350000.00",
  "status": "active"
}
```

### Delete Service
```bash
DELETE /api/services/1
```

---

## 5. Clients

### List Clients
```bash
GET /api/clients
GET /api/clients?verification_status=verified
GET /api/clients?search=john

Response:
[
  {
    "id": 1,
    "name": "John Okafor",
    "email": "john.okafor@example.com",
    "phone": "+234 803 456 7890",
    "company": "",
    "address": "Land at Enugu - Independence Layout",
    "project_description": "Land at Enugu - Independence Layout, 1500 sqm",
    "verification_status": "verified",
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-01-15T10:00:00Z",
    "created_by": "user_123"
  }
]
```

### Create Client
```bash
POST /api/clients
Content-Type: application/json

{
  "name": "John Okafor",
  "email": "john.okafor@example.com",
  "phone": "+234 803 456 7890",
  "company": "",
  "address": "",
  "project_description": "Land at Enugu - Independence Layout, 1500 sqm",
  "verification_status": "pending",
  "created_by": "user_123"
}
```

### Update Client
```bash
PUT /api/clients/1
Content-Type: application/json

{
  "verification_status": "verified",
  "phone": "+234 803 456 7890"
}
```

### Delete Client
```bash
DELETE /api/clients/1
```

---

## 6. Service Leads

### List Leads
```bash
GET /api/leads
GET /api/leads?status=qualified
GET /api/leads?client_id=1

Response:
[
  {
    "id": 1,
    "client": {
      "id": 1,
      "name": "John Okafor",
      ...
    },
    "service": {
      "id": 1,
      "name": "Real Estate",
      ...
    },
    "estimated_value": "25000000.00",
    "status": "qualified",
    "notes": "Interested in bulk purchase",
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-01-15T10:00:00Z",
    "created_by": "user_123"
  }
]
```

### Create Lead
```bash
POST /api/leads
Content-Type: application/json

{
  "client_id": 1,
  "service_id": 1,
  "estimated_value": "25000000.00",
  "status": "new",
  "notes": "Interested in bulk purchase",
  "created_by": "user_123"
}
```

### Update Lead
```bash
PUT /api/leads/1
Content-Type: application/json

{
  "status": "qualified",
  "notes": "Follow up scheduled for next week"
}
```

### Delete Lead
```bash
DELETE /api/leads/1
```

---

## 7. Quotes

### List Quotes
```bash
GET /api/quotes
GET /api/quotes?status=accepted
GET /api/quotes?client_id=1

Response:
[
  {
    "id": 1,
    "quote_number": "QTE-A1B2C3D4E5F6",
    "client": {
      "id": 1,
      "name": "Abuja Infrastructure Company",
      ...
    },
    "service": {
      "id": 1,
      "name": "Environmental Impact Assessment",
      ...
    },
    "description": "EIA for shopping mall development in Central Business District",
    "amount": "650000.00",
    "valid_until": "2024-08-31",
    "status": "accepted",
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-01-15T10:00:00Z",
    "created_by": "user_123"
  }
]
```

### Create Quote
```bash
POST /api/quotes
Content-Type: application/json

{
  "client_id": 1,
  "service_id": 1,
  "description": "EIA for shopping mall development in Central Business District",
  "amount": "650000.00",
  "valid_until": "2024-08-31",
  "status": "draft",
  "created_by": "user_123"
}
```

### Update Quote
```bash
PUT /api/quotes/1
Content-Type: application/json

{
  "status": "accepted",
  "amount": "650000.00"
}
```

### Delete Quote
```bash
DELETE /api/quotes/1
```

---

## 8. Service Orders

### List Orders
```bash
GET /api/orders
GET /api/orders?order_status=in_progress
GET /api/orders?payment_status=partial
GET /api/orders?client_id=1

Response:
[
  {
    "id": 1,
    "order_number": "ORD-A1B2C3D4E5F6",
    "client": {
      "id": 1,
      "name": "Abuja Infrastructure Company",
      ...
    },
    "service": {
      "id": 1,
      "name": "Environmental Impact Assessment",
      ...
    },
    "quote": {
      "id": 1,
      "quote_number": "QTE-A1B2C3D4E5F6",
      ...
    },
    "description": "EIA for shopping mall development",
    "amount": "650000.00",
    "order_status": "in_progress",
    "payment_status": "partial",
    "valid_until": "2024-08-31",
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-01-15T10:00:00Z",
    "created_by": "user_123",
    "assigned_to": "employee_456"
  }
]
```

### Create Order
```bash
POST /api/orders
Content-Type: application/json

{
  "client_id": 1,
  "service_id": 1,
  "quote_id": 1,
  "description": "EIA for shopping mall development",
  "amount": "650000.00",
  "order_status": "pending",
  "payment_status": "unpaid",
  "valid_until": "2024-08-31",
  "created_by": "user_123",
  "assigned_to": "employee_456"
}
```

### Update Order
```bash
PUT /api/orders/1
Content-Type: application/json

{
  "order_status": "in_progress",
  "payment_status": "partial",
  "assigned_to": "employee_789"
}
```

### Delete Order
```bash
DELETE /api/orders/1
```

---

## 9. Invoices

### List Invoices
```bash
GET /api/invoices
GET /api/invoices?status=paid
GET /api/invoices?client_id=1
GET /api/invoices?search=SRV-2025

Response:
[
  {
    "id": 1,
    "invoice_number": "SRV-2025-01-87654321",
    "client": {
      "id": 1,
      "name": "John Okafor",
      ...
    },
    "service": {
      "id": 1,
      "name": "Real Estate",
      ...
    },
    "order": null,
    "lead": {
      "id": 1,
      ...
    },
    "issue_date": "2025-01-15",
    "due_date": "2025-02-14",
    "subtotal": "650000.00",
    "tax_rate": "7.50",
    "tax_amount": "48750.00",
    "total_amount": "698750.00",
    "amount_paid": "300000.00",
    "balance": "398750.00",
    "payment_progress": 42.94,
    "status": "partially_paid",
    "notes": "",
    "items": [
      {
        "id": 1,
        "description": "Service fee",
        "quantity": "1.00",
        "unit_price": "650000.00",
        "total": "650000.00",
        "created_at": "2025-01-15T10:00:00Z",
        "updated_at": "2025-01-15T10:00:00Z"
      }
    ],
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-01-15T10:00:00Z",
    "created_by": "user_123"
  }
]
```

### Create Invoice with Items
```bash
POST /api/invoices
Content-Type: application/json

{
  "client_id": 1,
  "service_id": 1,
  "order_id": null,
  "lead_id": 1,
  "issue_date": "2025-01-15",
  "due_date": "2025-02-14",
  "subtotal": "650000.00",
  "tax_rate": "7.50",
  "status": "draft",
  "notes": "",
  "created_by": "user_123",
  "items": [
    {
      "description": "Service fee",
      "quantity": "1.00",
      "unit_price": "650000.00"
    }
  ]
}
```

### Update Invoice
```bash
PUT /api/invoices/1
Content-Type: application/json

{
  "status": "sent",
  "due_date": "2025-02-28"
}
```

### Delete Invoice
```bash
DELETE /api/invoices/1
```

---

## 10. Payments

### List Payments
```bash
GET /api/payments
GET /api/payments?invoice_id=1

Response:
[
  {
    "id": 1,
    "payment_reference": "PAY-A1B2C3D4E5F6",
    "invoice_id": 1,
    "amount": "300000.00",
    "payment_method": "bank_transfer",
    "payment_date": "2025-01-20",
    "transaction_reference": "TXN123456789",
    "notes": "Partial payment",
    "created_at": "2025-01-20T10:00:00Z",
    "updated_at": "2025-01-20T10:00:00Z",
    "created_by": "user_123"
  }
]
```

### Create Payment (Auto-updates Invoice)
```bash
POST /api/payments
Content-Type: application/json

{
  "invoice_id": 1,
  "amount": "300000.00",
  "payment_method": "bank_transfer",
  "payment_date": "2025-01-20",
  "transaction_reference": "TXN123456789",
  "notes": "Partial payment",
  "created_by": "user_123"
}
```

### Get Payment Details
```bash
GET /api/payments/1
```

### Delete Payment
```bash
DELETE /api/payments/1
```

---

## Payment Methods
- `cash`
- `bank_transfer`
- `cheque`
- `card`
- `mobile_money`
- `other`

## Status Values

### Service Status
- `active`
- `inactive`
- `draft`

### Client Verification Status
- `verified`
- `pending`
- `rejected`

### Lead Status
- `new`
- `qualified`
- `contacted`
- `proposal_sent`
- `converted`
- `lost`

### Quote Status
- `draft`
- `sent`
- `accepted`
- `rejected`
- `expired`

### Order Status
- `pending`
- `accepted`
- `in_progress`
- `completed`
- `cancelled`

### Payment Status (Orders)
- `unpaid`
- `partial`
- `paid`

### Invoice Status
- `draft`
- `sent`
- `viewed`
- `partially_paid`
- `paid`
- `overdue`
- `cancelled`

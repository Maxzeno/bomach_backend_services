from ninja import Schema
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal


# ServiceCategory Schemas
class ServiceCategoryIn(Schema):
    name: str
    description: Optional[str] = ""


class ServiceCategoryOut(Schema):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


# Service Schemas
class ServiceIn(Schema):
    name: str
    category_id: int
    description: str
    base_price: Decimal
    delivery_time: str
    status: str = "active"
    created_by: str


class ServiceUpdate(Schema):
    name: Optional[str] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    base_price: Optional[Decimal] = None
    delivery_time: Optional[str] = None
    status: Optional[str] = None


class ServiceOut(Schema):
    id: int
    name: str
    category: ServiceCategoryOut
    description: str
    base_price: Decimal
    delivery_time: str
    status: str
    created_at: datetime
    updated_at: datetime
    created_by: str


# Client Reference Schema (for embedded client info)
class ClientRefOut(Schema):
    """Client reference info - data comes from main backend"""
    client_id: str
    client_name: str
    client_email: str


# ServiceLead Schemas
class ServiceLeadIn(Schema):
    client_id: str  # Reference to main backend client
    client_name: str  # Cached for display
    client_email: Optional[str] = ""
    service_id: Optional[int] = None
    estimated_value: Decimal
    status: str = "new"
    notes: Optional[str] = ""
    created_by: str


class ServiceLeadUpdate(Schema):
    client_id: Optional[str] = None
    client_name: Optional[str] = None
    client_email: Optional[str] = None
    service_id: Optional[int] = None
    estimated_value: Optional[Decimal] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class ServiceLeadOut(Schema):
    id: int
    client_id: str
    client_name: str
    client_email: str
    service: Optional[ServiceOut] = None
    estimated_value: Decimal
    status: str
    notes: str
    created_at: datetime
    updated_at: datetime
    created_by: str


# Quote Schemas
class QuoteIn(Schema):
    client_id: str  # Reference to main backend client
    client_name: str
    client_email: Optional[str] = ""
    service_id: int
    description: str
    amount: Decimal
    valid_until: date
    status: str = "draft"
    created_by: str


class QuoteUpdate(Schema):
    client_id: Optional[str] = None
    client_name: Optional[str] = None
    client_email: Optional[str] = None
    service_id: Optional[int] = None
    description: Optional[str] = None
    amount: Optional[Decimal] = None
    valid_until: Optional[date] = None
    status: Optional[str] = None


class QuoteOut(Schema):
    id: int
    quote_number: str
    client_id: str
    client_name: str
    client_email: str
    service: ServiceOut
    description: str
    amount: Decimal
    valid_until: date
    status: str
    created_at: datetime
    updated_at: datetime
    created_by: str


# ServiceOrder Schemas
class ServiceOrderIn(Schema):
    client_id: str  # Reference to main backend client
    client_name: str
    client_email: Optional[str] = ""
    service_id: int
    quote_id: Optional[int] = None
    description: str
    amount: Decimal
    order_status: str = "pending"
    payment_status: str = "unpaid"
    valid_until: date
    created_by: str
    assigned_to: Optional[str] = ""


class ServiceOrderUpdate(Schema):
    client_id: Optional[str] = None
    client_name: Optional[str] = None
    client_email: Optional[str] = None
    service_id: Optional[int] = None
    quote_id: Optional[int] = None
    description: Optional[str] = None
    amount: Optional[Decimal] = None
    order_status: Optional[str] = None
    payment_status: Optional[str] = None
    valid_until: Optional[date] = None
    assigned_to: Optional[str] = None


class ServiceOrderOut(Schema):
    id: int
    order_number: str
    client_id: str
    client_name: str
    client_email: str
    service: ServiceOut
    quote: Optional[QuoteOut] = None
    description: str
    amount: Decimal
    order_status: str
    payment_status: str
    valid_until: date
    created_at: datetime
    updated_at: datetime
    created_by: str
    assigned_to: str


# InvoiceItem Schemas
class InvoiceItemIn(Schema):
    description: str
    quantity: Decimal
    unit_price: Decimal


class InvoiceItemOut(Schema):
    id: int
    description: str
    quantity: Decimal
    unit_price: Decimal
    total: Decimal
    created_at: datetime
    updated_at: datetime


# Invoice Schemas
class InvoiceIn(Schema):
    client_id: str  # Reference to main backend client
    client_name: str
    client_email: Optional[str] = ""
    service_id: int
    order_id: Optional[int] = None
    lead_id: Optional[int] = None
    issue_date: date
    due_date: date
    subtotal: Decimal
    tax_rate: Decimal = Decimal("7.50")
    status: str = "draft"
    notes: Optional[str] = ""
    created_by: str
    items: List[InvoiceItemIn] = []


class InvoiceUpdate(Schema):
    client_id: Optional[str] = None
    client_name: Optional[str] = None
    client_email: Optional[str] = None
    service_id: Optional[int] = None
    order_id: Optional[int] = None
    lead_id: Optional[int] = None
    issue_date: Optional[date] = None
    due_date: Optional[date] = None
    subtotal: Optional[Decimal] = None
    tax_rate: Optional[Decimal] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class InvoiceOut(Schema):
    id: int
    invoice_number: str
    client_id: str
    client_name: str
    client_email: str
    service: ServiceOut
    order: Optional[ServiceOrderOut] = None
    lead: Optional[ServiceLeadOut] = None
    issue_date: date
    due_date: date
    subtotal: Decimal
    tax_rate: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    amount_paid: Decimal
    balance: Decimal
    payment_progress: float
    status: str
    notes: str
    items: List[InvoiceItemOut]
    created_at: datetime
    updated_at: datetime
    created_by: str


# Payment Schemas
class PaymentIn(Schema):
    invoice_id: int
    amount: Decimal
    payment_method: str
    payment_date: date
    transaction_reference: Optional[str] = ""
    notes: Optional[str] = ""
    created_by: str


class PaymentOut(Schema):
    id: int
    payment_reference: str
    invoice_id: int
    amount: Decimal
    payment_method: str
    payment_date: date
    transaction_reference: str
    notes: str
    created_at: datetime
    updated_at: datetime
    created_by: str


# List/Pagination Schemas
class PaginatedResponse(Schema):
    count: int
    results: List


class ServiceListOut(Schema):
    count: int
    results: List[ServiceOut]


class ServiceLeadListOut(Schema):
    count: int
    results: List[ServiceLeadOut]


class QuoteListOut(Schema):
    count: int
    results: List[QuoteOut]


class ServiceOrderListOut(Schema):
    count: int
    results: List[ServiceOrderOut]


class InvoiceListOut(Schema):
    count: int
    results: List[InvoiceOut]


class PaymentListOut(Schema):
    count: int
    results: List[PaymentOut]


# Stats Schemas
class ServiceStatsOut(Schema):
    total_services: int
    total_orders: int
    total_quotes: int
    total_invoices: int


# Error Schemas
class ErrorOut(Schema):
    detail: str

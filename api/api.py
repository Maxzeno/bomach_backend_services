from ninja import NinjaAPI
from ninja import Schema
from typing import List
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import (
    ServiceCategory, Service, Client, ServiceLead, Quote,
    ServiceOrder, Invoice, InvoiceItem, Payment
)
from .schemas import (
    ServiceCategoryIn, ServiceCategoryOut,
    ServiceIn, ServiceUpdate, ServiceOut,
    ClientIn, ClientUpdate, ClientOut,
    ServiceLeadIn, ServiceLeadUpdate, ServiceLeadOut,
    QuoteIn, QuoteUpdate, QuoteOut,
    ServiceOrderIn, ServiceOrderUpdate, ServiceOrderOut,
    InvoiceIn, InvoiceUpdate, InvoiceOut, InvoiceItemIn,
    PaymentIn, PaymentOut,
    ServiceStatsOut
)

api = NinjaAPI(title="BOMACH Service Management API", version="1.0.0")


# Health Check
class HealthCheckResponse(Schema):
    status: str
    message: str


@api.get("/health", response=HealthCheckResponse, tags=["Health"])
def health_check(request):
    return {
        "status": "ok",
        "message": "Service is running"
    }


# ============= SERVICE CATEGORY ENDPOINTS =============
@api.get("/categories", response=List[ServiceCategoryOut], tags=["Categories"])
def list_categories(request):
    return ServiceCategory.objects.all()


@api.post("/categories", response=ServiceCategoryOut, tags=["Categories"])
def create_category(request, payload: ServiceCategoryIn):
    category = ServiceCategory.objects.create(**payload.dict())
    return category


@api.get("/categories/{category_id}", response=ServiceCategoryOut, tags=["Categories"])
def get_category(request, category_id: int):
    return get_object_or_404(ServiceCategory, id=category_id)


@api.put("/categories/{category_id}", response=ServiceCategoryOut, tags=["Categories"])
def update_category(request, category_id: int, payload: ServiceCategoryIn):
    category = get_object_or_404(ServiceCategory, id=category_id)
    for attr, value in payload.dict().items():
        setattr(category, attr, value)
    category.save()
    return category


@api.delete("/categories/{category_id}", tags=["Categories"])
def delete_category(request, category_id: int):
    category = get_object_or_404(ServiceCategory, id=category_id)
    category.delete()
    return {"success": True, "message": "Category deleted successfully"}


# ============= SERVICE ENDPOINTS =============
@api.get("/services", response=List[ServiceOut], tags=["Services"])
def list_services(request, status: str = None, category_id: int = None, search: str = None):
    services = Service.objects.select_related('category').all()

    if status:
        services = services.filter(status=status)
    if category_id:
        services = services.filter(category_id=category_id)
    if search:
        services = services.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )

    return services


@api.post("/services", response=ServiceOut, tags=["Services"])
def create_service(request, payload: ServiceIn):
    service = Service.objects.create(**payload.dict())
    return service


@api.get("/services/{service_id}", response=ServiceOut, tags=["Services"])
def get_service(request, service_id: int):
    return get_object_or_404(Service.objects.select_related('category'), id=service_id)


@api.put("/services/{service_id}", response=ServiceOut, tags=["Services"])
def update_service(request, service_id: int, payload: ServiceUpdate):
    service = get_object_or_404(Service, id=service_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(service, attr, value)
    service.save()
    return service


@api.delete("/services/{service_id}", tags=["Services"])
def delete_service(request, service_id: int):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    return {"success": True, "message": "Service deleted successfully"}


# ============= CLIENT ENDPOINTS =============
@api.get("/clients", response=List[ClientOut], tags=["Clients"])
def list_clients(request, verification_status: str = None, search: str = None):
    clients = Client.objects.all()

    if verification_status:
        clients = clients.filter(verification_status=verification_status)
    if search:
        clients = clients.filter(
            Q(name__icontains=search) | Q(email__icontains=search) | Q(phone__icontains=search)
        )

    return clients


@api.post("/clients", response=ClientOut, tags=["Clients"])
def create_client(request, payload: ClientIn):
    client = Client.objects.create(**payload.dict())
    return client


@api.get("/clients/{client_id}", response=ClientOut, tags=["Clients"])
def get_client(request, client_id: int):
    return get_object_or_404(Client, id=client_id)


@api.put("/clients/{client_id}", response=ClientOut, tags=["Clients"])
def update_client(request, client_id: int, payload: ClientUpdate):
    client = get_object_or_404(Client, id=client_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(client, attr, value)
    client.save()
    return client


@api.delete("/clients/{client_id}", tags=["Clients"])
def delete_client(request, client_id: int):
    client = get_object_or_404(Client, id=client_id)
    client.delete()
    return {"success": True, "message": "Client deleted successfully"}


# ============= SERVICE LEAD ENDPOINTS =============
@api.get("/leads", response=List[ServiceLeadOut], tags=["Service Leads"])
def list_leads(request, status: str = None, client_id: int = None, search: str = None):
    leads = ServiceLead.objects.select_related('client', 'service', 'service__category').all()

    if status:
        leads = leads.filter(status=status)
    if client_id:
        leads = leads.filter(client_id=client_id)
    if search:
        leads = leads.filter(
            Q(client__name__icontains=search) | Q(notes__icontains=search)
        )

    return leads


@api.post("/leads", response=ServiceLeadOut, tags=["Service Leads"])
def create_lead(request, payload: ServiceLeadIn):
    lead = ServiceLead.objects.create(**payload.dict())
    return lead


@api.get("/leads/{lead_id}", response=ServiceLeadOut, tags=["Service Leads"])
def get_lead(request, lead_id: int):
    return get_object_or_404(
        ServiceLead.objects.select_related('client', 'service', 'service__category'),
        id=lead_id
    )


@api.put("/leads/{lead_id}", response=ServiceLeadOut, tags=["Service Leads"])
def update_lead(request, lead_id: int, payload: ServiceLeadUpdate):
    lead = get_object_or_404(ServiceLead, id=lead_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(lead, attr, value)
    lead.save()
    return lead


@api.delete("/leads/{lead_id}", tags=["Service Leads"])
def delete_lead(request, lead_id: int):
    lead = get_object_or_404(ServiceLead, id=lead_id)
    lead.delete()
    return {"success": True, "message": "Lead deleted successfully"}


# ============= QUOTE ENDPOINTS =============
@api.get("/quotes", response=List[QuoteOut], tags=["Quotes"])
def list_quotes(request, status: str = None, client_id: int = None):
    quotes = Quote.objects.select_related('client', 'service', 'service__category').all()

    if status:
        quotes = quotes.filter(status=status)
    if client_id:
        quotes = quotes.filter(client_id=client_id)

    return quotes


@api.post("/quotes", response=QuoteOut, tags=["Quotes"])
def create_quote(request, payload: QuoteIn):
    quote = Quote.objects.create(**payload.dict())
    return quote


@api.get("/quotes/{quote_id}", response=QuoteOut, tags=["Quotes"])
def get_quote(request, quote_id: int):
    return get_object_or_404(
        Quote.objects.select_related('client', 'service', 'service__category'),
        id=quote_id
    )


@api.put("/quotes/{quote_id}", response=QuoteOut, tags=["Quotes"])
def update_quote(request, quote_id: int, payload: QuoteUpdate):
    quote = get_object_or_404(Quote, id=quote_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(quote, attr, value)
    quote.save()
    return quote


@api.delete("/quotes/{quote_id}", tags=["Quotes"])
def delete_quote(request, quote_id: int):
    quote = get_object_or_404(Quote, id=quote_id)
    quote.delete()
    return {"success": True, "message": "Quote deleted successfully"}


# ============= SERVICE ORDER ENDPOINTS =============
@api.get("/orders", response=List[ServiceOrderOut], tags=["Service Orders"])
def list_orders(request, order_status: str = None, payment_status: str = None, client_id: int = None):
    orders = ServiceOrder.objects.select_related(
        'client', 'service', 'service__category', 'quote'
    ).all()

    if order_status:
        orders = orders.filter(order_status=order_status)
    if payment_status:
        orders = orders.filter(payment_status=payment_status)
    if client_id:
        orders = orders.filter(client_id=client_id)

    return orders


@api.post("/orders", response=ServiceOrderOut, tags=["Service Orders"])
def create_order(request, payload: ServiceOrderIn):
    order = ServiceOrder.objects.create(**payload.dict())
    return order


@api.get("/orders/{order_id}", response=ServiceOrderOut, tags=["Service Orders"])
def get_order(request, order_id: int):
    return get_object_or_404(
        ServiceOrder.objects.select_related('client', 'service', 'service__category', 'quote'),
        id=order_id
    )


@api.put("/orders/{order_id}", response=ServiceOrderOut, tags=["Service Orders"])
def update_order(request, order_id: int, payload: ServiceOrderUpdate):
    order = get_object_or_404(ServiceOrder, id=order_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(order, attr, value)
    order.save()
    return order


@api.delete("/orders/{order_id}", tags=["Service Orders"])
def delete_order(request, order_id: int):
    order = get_object_or_404(ServiceOrder, id=order_id)
    order.delete()
    return {"success": True, "message": "Order deleted successfully"}


# ============= INVOICE ENDPOINTS =============
@api.get("/invoices", response=List[InvoiceOut], tags=["Invoices"])
def list_invoices(request, status: str = None, client_id: int = None, search: str = None):
    invoices = Invoice.objects.select_related(
        'client', 'service', 'service__category', 'order', 'lead'
    ).prefetch_related('items').all()

    if status:
        invoices = invoices.filter(status=status)
    if client_id:
        invoices = invoices.filter(client_id=client_id)
    if search:
        invoices = invoices.filter(
            Q(invoice_number__icontains=search) | Q(client__name__icontains=search)
        )

    return invoices


@api.post("/invoices", response=InvoiceOut, tags=["Invoices"])
def create_invoice(request, payload: InvoiceIn):
    items_data = payload.dict().pop('items', [])
    invoice = Invoice.objects.create(**payload.dict())

    for item_data in items_data:
        InvoiceItem.objects.create(invoice=invoice, **item_data)

    return invoice


@api.get("/invoices/{invoice_id}", response=InvoiceOut, tags=["Invoices"])
def get_invoice(request, invoice_id: int):
    return get_object_or_404(
        Invoice.objects.select_related(
            'client', 'service', 'service__category', 'order', 'lead'
        ).prefetch_related('items'),
        id=invoice_id
    )


@api.put("/invoices/{invoice_id}", response=InvoiceOut, tags=["Invoices"])
def update_invoice(request, invoice_id: int, payload: InvoiceUpdate):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(invoice, attr, value)
    invoice.save()
    return invoice


@api.delete("/invoices/{invoice_id}", tags=["Invoices"])
def delete_invoice(request, invoice_id: int):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.delete()
    return {"success": True, "message": "Invoice deleted successfully"}


# ============= PAYMENT ENDPOINTS =============
@api.get("/payments", response=List[PaymentOut], tags=["Payments"])
def list_payments(request, invoice_id: int = None):
    payments = Payment.objects.all()

    if invoice_id:
        payments = payments.filter(invoice_id=invoice_id)

    return payments


@api.post("/payments", response=PaymentOut, tags=["Payments"])
def create_payment(request, payload: PaymentIn):
    payment = Payment.objects.create(**payload.dict())
    return payment


@api.get("/payments/{payment_id}", response=PaymentOut, tags=["Payments"])
def get_payment(request, payment_id: int):
    return get_object_or_404(Payment, id=payment_id)


@api.delete("/payments/{payment_id}", tags=["Payments"])
def delete_payment(request, payment_id: int):
    payment = get_object_or_404(Payment, id=payment_id)
    payment.delete()
    return {"success": True, "message": "Payment deleted successfully"}


# ============= STATS ENDPOINT =============
@api.get("/stats", response=ServiceStatsOut, tags=["Statistics"])
def get_stats(request):
    return {
        "total_services": Service.objects.count(),
        "total_orders": ServiceOrder.objects.count(),
        "total_quotes": Quote.objects.count(),
        "total_invoices": Invoice.objects.count(),
    }

from ninja import NinjaAPI, Schema, Swagger

from api.api.v1 import budgets, categories, content, documents, events, expenses, invoices, leads, marketing_campaigns, orders, payments, property, quotes, services, stats
from api.utils.auth import AuthBearer


# Initialize NinjaAPI with authentication
api = NinjaAPI(
    title="BOMACH Service Management API",
    version="1.0.0",
    docs_url="/docs/",

    auth=AuthBearer(),  # Require authentication for all endpoints by default
    docs=Swagger(settings={"persistAuthorization": True})

)


# Health Check
class HealthCheckResponse(Schema):
    status: str
    message: str


@api.get("/health", response=HealthCheckResponse, tags=["Health"], auth=None)  # Public endpoint
def health_check(request):
    return {
        "status": "ok",
        "message": "Service is running"
    }


# Register routers (all protected by default auth)
api.add_router("/budgets", budgets.router)
api.add_router("/categories", categories.router)
api.add_router("/content", content.router)
api.add_router("/documents", documents.router)
api.add_router("/events", events.router)
api.add_router("/expenses", expenses.router)
api.add_router("/services", services.router)
api.add_router("/leads", leads.router)
api.add_router("/quotes", quotes.router)
api.add_router("/orders", orders.router)
api.add_router("/invoices", invoices.router)
api.add_router("/marketing-campaigns", marketing_campaigns.router)
api.add_router("/payments", payments.router)
api.add_router("/properties", property.router)
api.add_router("/stats", stats.router)

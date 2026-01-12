from ninja import NinjaAPI, Schema, Swagger

from api.api.v1 import categories, invoices, leads, orders, payments, quotes, services, stats
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
api.add_router("/categories", categories.router)
api.add_router("/services", services.router)
api.add_router("/leads", leads.router)
api.add_router("/quotes", quotes.router)
api.add_router("/orders", orders.router)
api.add_router("/invoices", invoices.router)
api.add_router("/payments", payments.router)
api.add_router("/stats", stats.router)

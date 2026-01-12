from ninja import Router

from api.api.schema.schemas import ServiceStatsOut
from api.models.payment import Invoice
from api.models.service import Quote, Service, ServiceOrder


router = Router()


@router.get("", response=ServiceStatsOut, tags=["Statistics"])
def get_stats(request):
    return {
        "total_services": Service.objects.count(),
        "total_orders": ServiceOrder.objects.count(),
        "total_quotes": Quote.objects.count(),
        "total_invoices": Invoice.objects.count(),
    }

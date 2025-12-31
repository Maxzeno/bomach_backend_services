from ninja import Router

from ..models import Service, ServiceOrder, Quote, Invoice
from ..schemas import ServiceStatsOut

router = Router()


@router.get("", response=ServiceStatsOut, tags=["Statistics"])
def get_stats(request):
    return {
        "total_services": Service.objects.count(),
        "total_orders": ServiceOrder.objects.count(),
        "total_quotes": Quote.objects.count(),
        "total_invoices": Invoice.objects.count(),
    }

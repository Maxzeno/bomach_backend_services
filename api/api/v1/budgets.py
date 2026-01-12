from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models import Q

from api.api.schema.budget_schemas import BudgetIn, BudgetOut, BudgetUpdate
from api.models.budget import Budget
from ninja.pagination import paginate, LimitOffsetPagination


router = Router(tags=["Budgets"])


@router.get("", response=List[BudgetOut])
@paginate(LimitOffsetPagination, page_size=10)
def list_budgets(
    request,
    status: str = None,
    project_id: str = None,
    payment_method: str = None,
    search: str = None
):
    """List all budgets with optional filtering."""
    budgets = Budget.objects.all()

    if status:
        budgets = budgets.filter(status=status)
    if project_id:
        budgets = budgets.filter(project_id=project_id)
    if payment_method:
        budgets = budgets.filter(payment_method=payment_method)
    if search:
        budgets = budgets.filter(
            Q(invoice_id__icontains=search) | Q(project_id__icontains=search)
        )

    return budgets


@router.post("", response=BudgetOut)
def create_budget(request, payload: BudgetIn):
    """Create a new budget."""
    budget = Budget.objects.create(**payload.dict())
    return budget


@router.get("/{budget_id}", response=BudgetOut)
def get_budget(request, budget_id: int):
    """Get a specific budget by ID."""
    return get_object_or_404(Budget, id=budget_id)


@router.put("/{budget_id}", response=BudgetOut)
def update_budget(request, budget_id: int, payload: BudgetUpdate):
    """Update an existing budget."""
    budget = get_object_or_404(Budget, id=budget_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(budget, attr, value)
    budget.save()
    return budget


@router.delete("/{budget_id}")
def delete_budget(request, budget_id: int):
    """Delete a budget."""
    budget = get_object_or_404(Budget, id=budget_id)
    budget.delete()
    return {"success": True, "message": "Budget deleted successfully"}


@router.get("/invoice/{invoice_id}", response=List[BudgetOut])
def get_budgets_by_invoice(request, invoice_id: str):
    """Get all budgets for a specific invoice ID."""
    budgets = Budget.objects.filter(invoice_id=invoice_id)
    return budgets


@router.get("/project/{project_id}/summary")
def get_project_budget_summary(request, project_id: str):
    """Get budget summary for a specific project."""
    budgets = Budget.objects.filter(project_id=project_id)

    total_budget = sum(budget.amount for budget in budgets)
    paid_budget = sum(budget.amount for budget in budgets.filter(status="paid"))
    approved_budget = sum(budget.amount for budget in budgets.filter(status="approved"))
    draft_budget = sum(budget.amount for budget in budgets.filter(status="draft"))

    return {
        "project_id": project_id,
        "total_budget": total_budget,
        "paid_budget": paid_budget,
        "approved_budget": approved_budget,
        "draft_budget": draft_budget,
        "budget_count": budgets.count(),
        "status_breakdown": {
            "draft": budgets.filter(status="draft").count(),
            "approved": budgets.filter(status="approved").count(),
            "paid": budgets.filter(status="paid").count(),
            "cancelled": budgets.filter(status="cancelled").count()
        }
    }

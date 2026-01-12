from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum
from ninja.pagination import paginate, LimitOffsetPagination

from api.api.schema.expense_schemas import ExpenseIn, ExpenseOut, ExpenseUpdate
from api.models.expenses import Expense


router = Router(tags=["Expenses"])


@router.get("", response=List[ExpenseOut])
@paginate(LimitOffsetPagination, page_size=10)
def list_expenses(
    request,
    status: str = None,
    category: str = None,
    user_id: str = None,
    search: str = None
):
    """List all expenses with optional filtering."""
    expenses = Expense.objects.all()

    if status:
        expenses = expenses.filter(status=status)
    if category:
        expenses = expenses.filter(category=category)
    if user_id:
        expenses = expenses.filter(user_id=user_id)
    if search:
        expenses = expenses.filter(
            Q(description__icontains=search) | Q(user_id__icontains=search)
        )

    return expenses


@router.post("", response=ExpenseOut)
def create_expense(request, payload: ExpenseIn):
    """Create a new expense."""
    expense = Expense.objects.create(**payload.dict())
    return expense


@router.get("/{expense_id}", response=ExpenseOut)
def get_expense(request, expense_id: int):
    """Get a specific expense by ID."""
    return get_object_or_404(Expense, id=expense_id)


@router.put("/{expense_id}", response=ExpenseOut)
def update_expense(request, expense_id: int, payload: ExpenseUpdate):
    """Update an existing expense."""
    expense = get_object_or_404(Expense, id=expense_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(expense, attr, value)
    expense.save()
    return expense


@router.delete("/{expense_id}")
def delete_expense(request, expense_id: int):
    """Delete an expense."""
    expense = get_object_or_404(Expense, id=expense_id)
    expense.delete()
    return {"success": True, "message": "Expense deleted successfully"}


@router.get("/user/{user_id}/expenses", response=List[ExpenseOut])
@paginate(LimitOffsetPagination, page_size=10)
def get_user_expenses(request, user_id: str):
    """Get all expenses for a specific user."""
    expenses = Expense.objects.filter(user_id=user_id)
    return expenses


@router.get("/user/{user_id}/summary")
def get_user_expense_summary(request, user_id: str):
    """Get expense summary for a specific user."""
    expenses = Expense.objects.filter(user_id=user_id)

    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    pending_expenses = expenses.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0
    approved_expenses = expenses.filter(status='approved').aggregate(total=Sum('amount'))['total'] or 0
    rejected_expenses = expenses.filter(status='rejected').aggregate(total=Sum('amount'))['total'] or 0
    paid_expenses = expenses.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0

    category_breakdown = {}
    for category, _ in Expense.CATEGORY_CHOICES:
        category_expenses = expenses.filter(category=category)
        category_breakdown[category] = {
            "count": category_expenses.count(),
            "total": category_expenses.aggregate(total=Sum('amount'))['total'] or 0
        }

    return {
        "user_id": user_id,
        "total_expenses": total_expenses,
        "pending_expenses": pending_expenses,
        "approved_expenses": approved_expenses,
        "rejected_expenses": rejected_expenses,
        "paid_expenses": paid_expenses,
        "expense_count": expenses.count(),
        "status_breakdown": {
            "pending": expenses.filter(status='pending').count(),
            "approved": expenses.filter(status='approved').count(),
            "rejected": expenses.filter(status='rejected').count(),
            "paid": expenses.filter(status='paid').count()
        },
        "category_breakdown": category_breakdown
    }


@router.get("/summary/all")
def get_all_expenses_summary(request):
    """Get overall expense summary across all users."""
    expenses = Expense.objects.all()

    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    pending_expenses = expenses.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0
    approved_expenses = expenses.filter(status='approved').aggregate(total=Sum('amount'))['total'] or 0
    rejected_expenses = expenses.filter(status='rejected').aggregate(total=Sum('amount'))['total'] or 0
    paid_expenses = expenses.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0

    category_breakdown = {}
    for category, _ in Expense.CATEGORY_CHOICES:
        category_expenses = expenses.filter(category=category)
        category_breakdown[category] = {
            "count": category_expenses.count(),
            "total": category_expenses.aggregate(total=Sum('amount'))['total'] or 0
        }

    return {
        "total_expenses": total_expenses,
        "pending_expenses": pending_expenses,
        "approved_expenses": approved_expenses,
        "rejected_expenses": rejected_expenses,
        "paid_expenses": paid_expenses,
        "expense_count": expenses.count(),
        "status_breakdown": {
            "pending": expenses.filter(status='pending').count(),
            "approved": expenses.filter(status='approved').count(),
            "rejected": expenses.filter(status='rejected').count(),
            "paid": expenses.filter(status='paid').count()
        },
        "category_breakdown": category_breakdown
    }

from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum
from ninja.pagination import paginate, LimitOffsetPagination
from django.core.exceptions import ValidationError

from api.api.schema.expense_schemas import ExpenseIn, ExpenseOut, ExpenseUpdate
from api.api.schema.others import MessageSchema
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


@router.post("", response={201: ExpenseOut, 400: MessageSchema})
def create_expense(request, payload: ExpenseIn):
    """Create a new expense."""
    try:
        expense = Expense.objects.create(**payload.dict())
        return 201, expense
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}


@router.get("/{expense_id}", response=ExpenseOut)
def get_expense(request, expense_id: int):
    """Get a specific expense by ID."""
    return get_object_or_404(Expense, id=expense_id)


@router.put("/{expense_id}", response={200: ExpenseOut, 400: MessageSchema, 404: MessageSchema})
def update_expense(request, expense_id: int, payload: ExpenseUpdate):
    """Update an existing expense."""
    try:
        expense = get_object_or_404(Expense, id=expense_id)
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(expense, attr, value)
        expense.save()
        return 200, expense
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}


@router.delete("/{expense_id}", response={200: MessageSchema, 400: MessageSchema, 404: MessageSchema})
def delete_expense(request, expense_id: int):
    """Delete an expense."""
    try:
        expense = get_object_or_404(Expense, id=expense_id)
        expense.delete()
        return 200, {"detail": "Expense deleted successfully"}
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}


@router.get("/user/{user_id}/expenses", response=List[ExpenseOut])
@paginate(LimitOffsetPagination, page_size=10)
def get_user_expenses(request, user_id: str):
    """Get all expenses for a specific user."""
    expenses = Expense.objects.filter(user_id=user_id)
    return expenses


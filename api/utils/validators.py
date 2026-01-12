from typing import Optional
from django.core.exceptions import ValidationError
from django.conf import settings
from api.utils.auth_client import AuthClient


def validate_employee_id(employee_id: str, service_token: Optional[str] = None) -> dict:
    if not employee_id:
        raise ValidationError("Employee ID is required")

    token = service_token or getattr(
        settings,
        'SERVICE_AUTH_TOKEN',
        getattr(settings, 'MAIN_BACKEND_SERVICE_TOKEN', None)
    )

    if not token:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(
            f"No SERVICE_AUTH_TOKEN configured - skipping validation for employee_id: {employee_id}"
        )
        return {'employee_id': employee_id}

    client = AuthClient()
    try:
        employee_info = client.get_employee_info(employee_id, token)

        if not employee_info:
            raise ValidationError(
                f"Employee with ID '{employee_id}' does not exist in the main backend"
            )

        # Verify employee is active
        if not employee_info.get('is_active', True):
            raise ValidationError(
                f"Employee with ID '{employee_id}' is not active"
            )

        return employee_info

    finally:
        client.close()


def validate_client_id(client_id: str, service_token: Optional[str] = None) -> dict:
    if not client_id:
        raise ValidationError("Client ID is required")

    token = service_token or getattr(
        settings,
        'SERVICE_AUTH_TOKEN',
        getattr(settings, 'MAIN_BACKEND_SERVICE_TOKEN', None)
    )

    if not token:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(
            f"No SERVICE_AUTH_TOKEN configured - skipping validation for client_id: {client_id}"
        )
        return {'client_id': client_id}

    client = AuthClient()
    try:
        client_info = client.get_client_info(client_id, token)

        if not client_info:
            raise ValidationError(
                f"Client with ID '{client_id}' does not exist in the main backend"
            )

        return client_info

    finally:
        client.close()


def validate_user_id(user_id: str, service_token: Optional[str] = None) -> dict:
    if not user_id:
        raise ValidationError("User ID is required")

    # Convert to int if it's a string
    try:
        user_id_int = int(user_id) if isinstance(user_id, str) else user_id
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid user ID format: '{user_id}'")

    token = service_token or getattr(
        settings,
        'SERVICE_AUTH_TOKEN',
        getattr(settings, 'MAIN_BACKEND_SERVICE_TOKEN', None)
    )

    if not token:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(
            f"No SERVICE_AUTH_TOKEN configured - skipping validation for user_id: {user_id}"
        )
        return {'id': user_id_int}

    client = AuthClient()
    try:
        # Note: This may need adjustment based on auth_client implementation
        user_info = getattr(client, 'get_user_info', lambda uid, tok: None)(user_id_int, token)

        if not user_info:
            raise ValidationError(
                f"User with ID '{user_id}' does not exist in the main backend"
            )

        # Verify user is active
        if not user_info.get('is_active', True):
            raise ValidationError(
                f"User with ID '{user_id}' is not active"
            )

        return user_info

    finally:
        client.close()

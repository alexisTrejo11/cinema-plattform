from app.shared.docs.common_responses import common_error_responses as common_responses
from fastapi import status

create_promotion_examples = {
    "201": {
        "description": "Promotion created successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "Promotion created successfully.",
                    "data": {"id": "promo-123"},
                }
            }
        },
    },
    status.HTTP_400_BAD_REQUEST: common_responses[status.HTTP_400_BAD_REQUEST],
    status.HTTP_404_NOT_FOUND: common_responses[status.HTTP_404_NOT_FOUND],
    status.HTTP_500_INTERNAL_SERVER_ERROR: common_responses[
        status.HTTP_500_INTERNAL_SERVER_ERROR
    ],
}

activate_promotion_examples = {
    status.HTTP_200_OK: {
        "description": "Promotion activated successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "Promotion activated successfully.",
                }
            }
        },
    },
    status.HTTP_400_BAD_REQUEST: common_responses[status.HTTP_400_BAD_REQUEST],
    status.HTTP_404_NOT_FOUND: common_responses[status.HTTP_404_NOT_FOUND],
    status.HTTP_500_INTERNAL_SERVER_ERROR: common_responses[
        status.HTTP_500_INTERNAL_SERVER_ERROR
    ],
}


deactivate_promotion_examples = {
    status.HTTP_200_OK: {
        "description": "Promotion deactivated successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "Promotion deactivated successfully.",
                }
            }
        },
    },
    status.HTTP_400_BAD_REQUEST: common_responses[status.HTTP_400_BAD_REQUEST],
    status.HTTP_404_NOT_FOUND: common_responses[status.HTTP_404_NOT_FOUND],
    status.HTTP_500_INTERNAL_SERVER_ERROR: common_responses[
        status.HTTP_500_INTERNAL_SERVER_ERROR
    ],
}


extend_promotion_examples = {
    status.HTTP_200_OK: {
        "description": "Promotion extended successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "Promotion extended successfully.",
                }
            }
        },
    },
    status.HTTP_400_BAD_REQUEST: common_responses[status.HTTP_400_BAD_REQUEST],
    status.HTTP_404_NOT_FOUND: common_responses[status.HTTP_404_NOT_FOUND],
    status.HTTP_500_INTERNAL_SERVER_ERROR: common_responses[
        status.HTTP_500_INTERNAL_SERVER_ERROR
    ],
}

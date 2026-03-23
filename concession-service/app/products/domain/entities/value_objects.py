from app.shared.schema import PydanticUUID


class ProductId(PydanticUUID):
    """Value object for product ID."""

    pass


class CategoryId(PydanticUUID):
    """Value object for category ID."""

    pass


class ComboId(PydanticUUID):
    """Value object for combo meal ID."""

    pass

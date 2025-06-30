from datetime import datetime
from typing import List, Optional
from app.products.domain.entities import FoodProduct
from decimal import Decimal
from .exceptions import *

class Combo:
    """Represents a combo meal consisting of multiple food products.
    
    A combo is a collection of food items sold together at a special price,
    potentially with a discount percentage applied. The class enforces business
    rules regarding pricing, discounts, and item composition.
    
    Attributes:
        id: Unique identifier for the combo (optional for new combos)
        name: Name of the combo (1-200 characters)
        price: Total price of the combo (must be greater than 0)
        description: Optional description of the combo
        discount_percentage: Discount percentage (0-100)
        image_url: Optional URL for combo image
        is_available: Whether the combo is currently available
        items: List of ComboItem objects in this combo
    """
    
    def __init__(
        self,
        id: Optional[int],
        name: str,
        price: Decimal,
        description: Optional[str] = None,
        discount_percentage: Decimal = Decimal('0'),
        image_url: Optional[str] = None,
        is_available: bool = True,
        items: Optional[List['ComboItem']] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None  
    ):
        """Initializes a Combo with validation of basic attributes.
        
        Args:
            id: Unique identifier for the combo (None for new combos)
            name: Name of the combo (1-200 characters)
            price: Total price of the combo (must be positive)
            description: Optional description of the combo
            discount_percentage: Discount percentage (default 0, range 0-100)
            image_url: Optional URL for combo image
            is_available: Whether combo is available (default True)
            items: Optional list of ComboItems in this combo
            
        Raises:
            ValueError: If name, price or discount_percentage are invalid
            TypeError: If items contains non-ComboItem objects
        """
        if not isinstance(name, str) or not (1 <= len(name) <= 200):
            raise ValueError("name must be a string between 1 and 200 characters.")
        if not isinstance(price, Decimal) or price <= Decimal('0'):
            raise ValueError("price must be a Decimal greater than 0.")
        if not isinstance(discount_percentage, Decimal) or not (Decimal('0') <= discount_percentage <= Decimal('100')):
            raise ValueError("discount_percentage must be a Decimal between 0 and 100.")
        if items is not None and not all(isinstance(item, ComboItem) for item in items):
            raise TypeError("items must be a list of ComboItem instances.")
            
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.discount_percentage = discount_percentage
        self.image_url = image_url
        self.is_available = is_available
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()
        self.items = items if items is not None else [] 
        
        
    def validate_business_logic(self):
        """Validates all business rules for the combo.
        
        Performs comprehensive validation including:
        - Price range validation
        - Item count validation
        - Price vs. sum of product prices validation
        - Discount percentage consistency
        
        Raises:
            PriceRangeException: If price is outside allowed range
            ItemRangeException: If item count is outside allowed range
            PriceSumException: If combo price exceeds sum of product prices
            DiscountPercentageException: If discount doesn't match price ratio
        """
        self._validate_numbers()
    
    def _validate_numbers(self):
        """Internal method to validate all numeric business rules."""
        self._validate_price_range()
        self._validate_item_range()
        
        product_total_price = self._get_product_total_price_sum()
        self._assert_price(product_total_price)
        self._assert_discount_percentage(product_total_price)

    def _get_product_total_price_sum(self) -> Decimal:
        """Calculates the sum of all individual product prices in the combo.
        
        Returns:
            Decimal: Sum of all product prices in the combo
        """
        product_price_sum = Decimal('0')
        for item in self.items:
            item.validate_quantity_range()
            product_price_sum += Decimal(str(item.product.price))
        return product_price_sum

    def _validate_price_range(self):
        """Validates that combo price is within allowed range (10-2000)."""
        min_price = Decimal('10')
        max_price = Decimal('2000')
        if not (min_price <= self.price <= max_price):
            raise PriceRangeException(min_price, max_price)

    def _validate_item_range(self):
        """Validates that combo contains between 1-10 items."""
        min_items = 1
        max_items = 10
        if not (min_items <= len(self.items)) <= max_items:
            raise ItemRangeException(min_items, max_items)

    def _assert_price(self, product_total_price: Decimal):
        """Ensures combo price doesn't exceed sum of individual product prices.
        
        Args:
            product_total_price: Sum of all individual product prices
            
        Raises:
            PriceSumException: If combo price exceeds sum of product prices
        """
        if self.price > product_total_price:
            raise PriceSumException(product_total_price)

    def _assert_discount_percentage(self, product_price_sum: Decimal):
        """Validates that discount percentage matches price ratio.
        
        Args:
            product_price_sum: Sum of all individual product prices
            
        Raises:
            DiscountPercentageException: If calculated discount doesn't match 
                the declared discount percentage within tolerance
        """
        if product_price_sum == Decimal('0'):
            raise DiscountPercentageException(
                Decimal('0'),
                details={"message": "Cannot calculate discount for zero-value product sum"}
            )
        
        combo_price_ratio = (self.price * Decimal('100')) / product_price_sum
        actual_discount = Decimal('100') - combo_price_ratio
           
        tolerance = Decimal('0.01')
        if abs(actual_discount - self.discount_percentage) > tolerance:
            raise DiscountPercentageException(
                round(actual_discount, 2),
                details={
                    "expected": round(float(self.discount_percentage), 2),
                    "actual": round(float(actual_discount), 2),
                    "tolerance": float(tolerance)
                }
            )

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Combo to a dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "discount_percentage": str(self.discount_percentage),
            "image_url": self.image_url,
            "is_available": self.is_available,
            "created_at": self.created_at if self.created_at else None,
            "updated_at": self.updated_at if self.updated_at else None,
            "items": [item.__dict__ for item in self.items]
        }   

    def __repr__(self):
        """Returns a string representation of the Combo."""
        return f"Combo(id={self.id}, name='{self.name}', price={self.price}, discount_percentage={self.discount_percentage})"

class ComboItem:
    """Represents an individual food product within a combo.
    
    Attributes:
        product: The FoodProduct included in the combo
        quantity: Quantity of this product in the combo (1-10)
    """
    
    def __init__(self, product: FoodProduct, quantity: int = 1):
        """Initializes a ComboItem with validation.
        
        Args:
            product: FoodProduct to include in combo
            quantity: Quantity of this product (default 1)
            
        Raises:
            TypeError: If product is not a FoodProduct or quantity is not an integer
        """
        if not isinstance(product, FoodProduct):
            raise TypeError("product must be an instance of FoodProduct")
        if not isinstance(quantity, int):
            raise TypeError("quantity must be an integer")

        self.product = product
        self.quantity = quantity

    def validate_quantity_range(self):
        """Validates that quantity is within allowed range (1-10).
        
        Raises:
            QuantityRangeException: If quantity is outside 1-10 range
        """
        min_quantity = 1
        max_quantity = 10
        if not (min_quantity <= self.quantity <= max_quantity):
            raise QuantityRangeException(self.product.id, min_quantity, max_quantity)
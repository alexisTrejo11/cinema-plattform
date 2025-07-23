from abc import ABC, abstractmethod
from app.products.domain.entities.product import Product, ProductId
from app.products.domain.entities.product_category import ProductCategory
from typing import Dict, Optional, List
from app.products.application.queries import SearchProductsQuery, ProductId


class ProductCategoryRepository(ABC):
    """
    Abstract base class for a product category repository.

    Defines the contract for data access operations related to food categories.
    Implementations of this interface will handle persistence of ProductCategory entities.
    """

    @abstractmethod
    async def get_by_id(self, category_id: int) -> Optional[ProductCategory]:
        """
        Retrieves a single food category by its unique identifier.

        Args:
            category_id (int): The unique identifier of the food category.

        Returns:
            Optional[ProductCategory]: The ProductCategory entity if found, otherwise None.
        """
        pass

    @abstractmethod
    async def list(self) -> List[ProductCategory]:
        """
        Retrieves a list of all food categories.

        Returns:
            List[ProductCategory]: A list containing all ProductCategory entities.
        """
        pass

    @abstractmethod
    async def save(self, category: ProductCategory) -> ProductCategory:
        """
        Saves a new food category or updates an existing one.

        If the category has an ID, it attempts to update the existing record.
        If the category does not have an ID (or ID is 0), it creates a new record.

        Args:
            category (ProductCategory): The ProductCategory entity to save.

        Returns:
            ProductCategory: The saved ProductCategory entity, potentially with an updated ID
                          if it was a new category.
        """
        pass

    @abstractmethod
    async def delete(self, category_id: int) -> bool:
        """
        Deletes a food category by its unique identifier.

        Args:
            category_id (int): The unique identifier of the food category to delete.

        Returns:
            bool: True if the category was successfully deleted, False otherwise.
        """
        pass

    @abstractmethod
    async def exists_by_id(self, category_id: int) -> bool:
        """
        Checks if a food category with the given ID exists.

        Args:
            category_id (int): The unique identifier of the food category.

        Returns:
            bool: True if a category with the specified ID exists, False otherwise.
        """
        pass

    @abstractmethod
    async def exists_by_name(self, category_name: str) -> bool:
        """
        Checks if a food category with the given name exists.

        Args:
            category_name (str): The name of the food category.

        Returns:
            bool: True if a category with the specified name exists, False otherwise.
        """
        pass


class ProductRepository(ABC):
    """
    Abstract base class for a product repository.

    Defines the contract for data access operations related to food products.
    Implementations of this interface will handle persistence of Product entities.
    """

    @abstractmethod
    async def get_by_id(self, product_id: ProductId) -> Optional[Product]:
        """
        Retrieves a single food product by its ID.

        Args:
            product_id (int): The unique identifier of the food product.

        Returns:
            Optional[Product]: The Product entity if found, otherwise None.
        """
        pass

    @abstractmethod
    async def get_by_id_in(
        self, product_id_list: List[ProductId]
    ) -> Dict[ProductId, Product]:
        """
        Retrieves multiple food products based on a list of their IDs.

        Args:
            product_id_list (List[ProductId]): A list of unique identifiers for the food products.

        Returns:
            Dict[ProductId, Product]: A dictionary where keys are product IDs and values are
                                    the corresponding Product entities. Products not found
                                    will not be included in the dictionary.
        """
        pass

    @abstractmethod
    async def search(self, food_params: SearchProductsQuery) -> List[Product]:
        """
        Searches for food products based on various criteria provided in SearchFoodParams.

        Args:
            food_params (SearchFoodParams): An object containing search parameters
                                            like price range, name, category,
                                            availability, offset, and limit.

        Returns:
            List[Product]: A list of Product domain entities that match
                               the search criteria.
        """
        pass

    @abstractmethod
    async def save(self, product: Product) -> Product:
        """
        Saves a new food product or updates an existing one.

        If the product has an ID, it attempts to update the existing record.
        If the product does not have an ID, it creates a new record.

        Args:
            product (Product): The Product entity to save.

        Returns:
            Product: The saved Product entity, potentially with an updated ID
                         if it was a new product.
        """
        pass

    @abstractmethod
    async def delete(self, product_id: ProductId) -> None:
        """
        Deletes a food product by its unique identifier.

        Args:
            product_id (ProductId): The unique identifier of the food product to delete.

        Returns:
            None
        """
        pass

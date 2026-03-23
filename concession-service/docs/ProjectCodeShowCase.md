# Code Showcase

## Code Examples (`CodeExample[]`)

### Example 1: Product Entity with Validation

- **ID**: "product-entity"
- **Title**: "Domain Entity with Business Validation"
- **Description**: "Product entity demonstrating Pydantic validation, value objects, and business rule enforcement using hexagonal architecture patterns."
- **Category**: "Domain"
- **Duration** (optional): "N/A"
- **Views** (optional): 100
- **Tags** (optional):
  - "python"
  - "domain-driven-design"
  - "pydantic"
  - "validation"

#### Files (`CodeFile[]`)

- **Name**: "product.py"
- **Path**: "app/products/domain/entities/product.py"
- **Language**: "python"
- **Content**:
  ```python
  from datetime import datetime
  from decimal import Decimal
  from typing import Any, Dict, Optional
  from uuid import UUID

  from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

  from .value_objects import ProductId
  from ..validator import ProductValidator


  class Product(BaseModel):
      """Represents a food product in the domain with business validations."""

      model_config = ConfigDict(arbitrary_types_allowed=True)

      id: ProductId = Field(default_factory=ProductId.generate)
      name: str = ""
      price: Decimal = Decimal("0.00")
      category_id: int = 0
      description: Optional[str] = None
      image_url: str
      is_available: bool = True
      preparation_time_mins: Optional[int] = None
      calories: Optional[int] = None
      created_at: datetime = Field(default_factory=datetime.now)
      updated_at: datetime = Field(default_factory=datetime.now)
      deleted_at: Optional[datetime] = None

      @field_validator("id", mode="before")
      @classmethod
      def _validate_id_field(cls, value: Any) -> ProductId:
          if value in (None, ""):
              return ProductId.generate()
          if isinstance(value, ProductId):
              return value
          if isinstance(value, UUID):
              return ProductId(value)
          if isinstance(value, str):
              return ProductId.from_string(value)
          raise ValueError(f"Cannot convert {type(value)} to ProductId")

      @classmethod
      def create(cls, data: Dict[str, Any]) -> "Product":
          default_image_url: str = "https://via.placeholder.com/150"
          data["id"] = ProductId.generate()
          data["price"] = Decimal(str(data["price"]))
          data["image_url"] = data["image_url"] or default_image_url
          return cls(**data)

      @model_validator(mode="after")
      def _run_business_validation(self) -> "Product":
          ProductValidator.validate_product(self)
          return self

      def validate_business_rules(self):
          """Validate all business rules for this product."""
          ProductValidator.validate_product(self)

      def restore(self) -> "Product":
          self.deleted_at = None
          return self
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "The Product entity demonstrates several key patterns: value objects for ID validation, Pydantic validators for type conversion, model validators for business rule enforcement, and soft delete via the deleted_at field."

---

### Example 2: Promotion Domain Logic

- **ID**: "promotion-domain"
- **Title**: "Rich Domain Model with Business Operations"
- **Description**: "Promotion entity showing complex domain logic including activation, expiration, and usage tracking with comprehensive business validations."
- **Category**: "Domain"
- **Tags** (optional):
  - "python"
  - "domain-driven-design"
  - "business-logic"

#### Files (`CodeFile[]`)

- **Name**: "promotion.py"
- **Path**: "app/promotions/domain/entities/promotion.py"
- **Language**: "python"
- **Content**:
  ```python
  from datetime import datetime, timezone
  from typing import List, Optional

  from pydantic import BaseModel, ConfigDict, Field

  from .value_objects import PromotionId, PromotionType, ProductId
  from ..exceptions.promotion_exceptions import *

  def _utc_now() -> datetime:
      """Always use timezone-aware UTC for domain timestamps and comparisons."""
      return datetime.now(timezone.utc)

  class Promotion(BaseModel):
      """Domain entity representing a commercial promotion."""

      model_config = ConfigDict(arbitrary_types_allowed=True)

      name: str
      promotion_type: PromotionType
      rule: dict = Field(default_factory=dict)
      start_date: datetime
      end_date: datetime
      applicable_product_ids: List[ProductId] = Field(default_factory=list)
      applicable_categories_ids: List[int] = Field(default_factory=list)
      description: Optional[str] = None
      is_active: bool = True
      id: PromotionId = Field(default_factory=PromotionId.generate)
      max_uses: Optional[int] = None
      current_uses: int = 0
      created_at: datetime = Field(default_factory=_utc_now)
      updated_at: datetime = Field(default_factory=_utc_now)

      def validate_creation_fields(self):
          # Comprehensive validation logic...
          pass

      def activate(self):
          if self.is_active:
              raise PromotionAlreadyActiveError(promotion_id=str(self.id))
          self.is_active = True
          self.updated_at = _utc_now()

      def deactivate(self):
          if not self.is_active:
              raise PromotionAlreadyInactiveError(promotion_id=str(self.id))
          self.is_active = False
          self.updated_at = _utc_now()

      def extend_validity(self, new_end_date: datetime):
          # Extension logic with timezone validation...
          pass

      def apply(self, quantity: int):
          if not self.is_active:
              raise PromotionAlreadyInactiveError(...)
          if _utc_now() > self.end_date:
              raise PromotionExpiredError(...)
          if self.max_uses is not None and self.current_uses + quantity > self.max_uses:
              raise PromotionMaxUsesExceededError(...)
          self.current_uses += quantity
          self.updated_at = _utc_now()
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "The Promotion entity showcases a rich domain model with comprehensive business operations: activation/deactivation workflows, date-based validation, usage tracking with max uses limits, and timezone-aware timestamps."

---

### Example 3: Dependency Injection Container

- **ID**: "di-container"
- **Title**: "Use Case Container with Dependency Injection"
- **Description**: "Demonstrates the dependency injection pattern using FastAPI's Depends for managing use case instances and their repository dependencies."
- **Category**: "Architecture"
- **Tags** (optional):
  - "python"
  - "fastapi"
  - "dependency-injection"
  - "cqrs"

#### Files (`CodeFile[]`)

- **Name**: "container.py"
- **Path**: "app/products/application/use_cases/container.py"
- **Language**: "python"
- **Content**:
  ```python
  from typing import List
  from app.products.domain.repositories import (
      ProductRepository,
      ProductCategoryRepository,
  )
  from app.products.application.queries import SearchProductsQuery, GetProductByIdQuery
  from app.products.application.commands import ProductCreateCommand, ProductUpdateCommand

  from .product_use_cases import (
      GetProductByIdUseCase,
      UpdateProductUseCase,
      CreateProductUseCase,
      SearchProductUseCase,
      DeleteProductUseCase,
  )
  from .category_use_cases import (
      GetCategoryByIdUseCase,
      GetAllCategoriesUseCase,
      CreateCategoryUseCase,
      UpdateCategoryUseCase,
      DeleteCategoryUseCase,
  )

  class ProductUseCases:
      def __init__(
          self,
          product_repository: ProductRepository,
          category_repository: ProductCategoryRepository,
      ):
          self.product_repository = product_repository
          self.category_repository = category_repository
          self.get_product_by_uc = GetProductByIdUseCase(product_repository)
          self.search_product_uc = SearchProductUseCase(product_repository)
          self.update_product_uc = UpdateProductUseCase(
              product_repository, category_repository
          )
          self.create_product_uc = CreateProductUseCase(
              product_repository, category_repository
          )
          self.delete_product_uc = DeleteProductUseCase(product_repository)

      async def get_product_by_id(self, query: GetProductByIdQuery) -> Product:
          return await self.get_product_by_uc.execute(query)

      async def search_products(self, query: SearchProductsQuery) -> ProductPaginatedResponse:
          return await self.search_product_uc.execute(query)

      async def create_product(self, create_data: ProductCreateCommand) -> Product:
          return await self.create_product_uc.execute(create_data)
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "The ProductUseCases container demonstrates the dependency injection pattern by accepting repository interfaces in its constructor. FastAPI's dependency injection system wires up the concrete implementations at runtime."

---

### Example 4: API Controller with Rate Limiting

- **ID**: "api-controller"
- **Title**: "FastAPI Controller with Rate Limiting"
- **Description**: "Shows how to implement rate-limited endpoints with authentication using FastAPI routers and SlowAPI."
- **Category**: "API"
- **Tags** (optional):
  - "python"
  - "fastapi"
  - "rate-limiting"
  - "authentication"

#### Files (`CodeFile[]`)

- **Name**: "product_controller.py"
- **Path**: "app/products/infrastructure/api/controllers/product_controller.py"
- **Language**: "python"
- **Content**:
  ```python
  from fastapi import APIRouter, Depends, Path, Request, status
  from uuid import UUID

  from app.config.rate_limit import limiter
  from app.config.security import require_roles, AuthUserContext
  from app.products.domain.entities.value_objects import ProductId
  from app.products.application.commands import ProductUpdateCommand, ProductCreateCommand
  from app.products.application.queries import GetProductByIdQuery, SearchProductsQuery

  router = APIRouter(prefix="/api/v2/products", tags=["Food Products"])

  @router.get(
      "/{product_id}",
      response_model=ProductResponse,
      summary="Get product by ID",
  )
  @limiter.limit("60/minute")
  async def get_product_by_id(
      request: Request,
      product_id: UUID = Path(..., description="ID of the product to retrieve"),
      usecase: ProductUseCases = Depends(get_product_use_cases),
  ):
      query = GetProductByIdQuery(product_id=ProductId(value=product_id))
      product = await usecase.get_product_by_id(query)
      return ProductResponse.from_entity(product)

  @router.post(
      "/",
      response_model=ProductResponse,
      status_code=status.HTTP_201_CREATED,
      summary="Create a new food product",
  )
  @limiter.limit("10/minute")
  async def create_product(
      request: Request,
      product_data: CreateProductRequest,
      performed_by: AuthUserContext = Depends(require_roles("admin", "manager")),
      usecase: ProductUseCases = Depends(get_product_use_cases),
  ):
      command = ProductCreateCommand(**product_data.model_dump())
      product = await usecase.create_product(command)
      return ProductResponse.from_entity(product)
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "The controller demonstrates rate limiting with SlowAPI (@limiter.limit decorators), JWT authentication with role-based access control (require_roles dependency), and proper use of FastAPI's dependency injection system."

---

### Example 5: gRPC Service Implementation

- **ID**: "grpc-service"
- **Title**: "gRPC Service for Inter-Service Communication"
- **Description**: "Shows the gRPC server implementation using grpcio for high-performance service-to-service communication."
- **Category**: "Integration"
- **Tags** (optional):
  - "python"
  - "grpc"
  - "microservices"
  - "protobuf"

#### Files (`CodeFile[]`)

- **Name**: "server.py"
- **Path**: "app/grpc/server.py"
- **Language**: "python"
- **Content**:
  ```python
  import asyncio
  import logging
  import os

  import grpc

  from app.config.db.postgres_config import AsyncSessionLocal
  from app.grpc.generated import concession_pb2_grpc
  from app.grpc.services.concession_catalog_servicer import ConcessionCatalogGrpcServicer

  logger = logging.getLogger(__name__)

  async def serve_grpc(host: str = "0.0.0.0", port: int = 50051) -> None:
      server = grpc.aio.server()
      concession_pb2_grpc.add_ConcessionCatalogServiceServicer_to_server(
          ConcessionCatalogGrpcServicer(AsyncSessionLocal), server
      )
      bind_address = f"{host}:{port}"
      server.add_insecure_port(bind_address)

      await server.start()
      logger.info("Concession gRPC server started on %s", bind_address)
      await server.wait_for_termination()

  if __name__ == "__main__":
      grpc_host = os.getenv("GRPC_HOST", "0.0.0.0")
      grpc_port = int(os.getenv("GRPC_PORT", "50051"))
      asyncio.run(serve_grpc(host=grpc_host, port=grpc_port))
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "The gRPC server demonstrates async gRPC server setup with dependency injection of the database session factory, enabling high-performance inter-service communication within the cinema platform."

---

### Example 6: Database Migrations with Alembic

- **ID**: "alembic-migrations"
- **Title**: "Database Schema with Alembic"
- **Description**: "Shows the Alembic migration structure for managing PostgreSQL database schema evolution."
- **Category**: "Database"
- **Tags** (optional):
  - "python"
  - "alembic"
  - "postgresql"
  - "migrations"

#### Files (`CodeFile[]`)

- **Name**: "0003_create_products.py"
- **Path**: "alembic/versions/0003_create_products.py"
- **Language**: "python"
- **Content**:
  ```python
  """create products

  Revision ID: 0003
  Revises: 0002
  Create Date: 2024-01-15
  
  """
  from alembic import op
  import sqlalchemy as sa
  from sqlalchemy.dialects import postgresql

  revision = '0003'
  down_revision = '0002'
  branch_labels = None
  depends_on = None

  def upgrade() -> None:
      op.create_table(
          'products',
          sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
          sa.Column('name', sa.String(length=200), nullable=False),
          sa.Column('description', sa.Text(), nullable=True),
          sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
          sa.Column('image_url', sa.String(length=500), nullable=True),
          sa.Column('is_available', sa.Boolean(), nullable=False, default=True),
          sa.Column('preparation_time_mins', sa.Integer(), nullable=True),
          sa.Column('calories', sa.Integer(), nullable=True),
          sa.Column('category_id', sa.Integer(), nullable=False),
          sa.Column('created_at', sa.DateTime(), nullable=True),
          sa.Column('updated_at', sa.DateTime(), nullable=True),
          sa.Column('deleted_at', sa.DateTime(), nullable=True),
          sa.ForeignKeyConstraint(['category_id'], ['product_categories.id']),
          sa.PrimaryKeyConstraint('id')
      )
      op.create_index('ix_products_id', 'products', ['id'])
      op.create_index('ix_products_category_id', 'products', ['category_id'])

  def downgrade() -> None:
      op.drop_index('ix_products_category_id', table_name='products')
      op.drop_index('ix_products_id', table_name='products')
      op.drop_table('products')
  ```
- **Highlighted** (optional): `false`
- **Explanation** (optional): "The migration file demonstrates Alembic's migration structure with upgrade/downgrade functions, proper foreign key constraints, and index creation for query optimization."

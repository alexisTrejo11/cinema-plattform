# Project Features

## Feature List (`ProjectFeature[]`)

### Feature 1: Product Catalog Management

- **ID**: "product-catalog"
- **Title**: "Product Catalog Management"
- **Description**: Full CRUD operations for cinema concession products including snacks, beverages, and food items with support for pricing, availability status, preparation time, and nutritional information.
- **Icon**: "package"
- **Category** (`FeatureCategory`): `api` | `database`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Create, read, update, and delete food products
  - Soft delete support for data retention
  - Category-based product organization
  - Search and filter with pagination
  - Price range filtering
- **Tech Stack** (optional):
  - FastAPI
  - SQLAlchemy ORM
  - PostgreSQL
  - Redis Cache
- **Metrics** (optional, `FeatureMetric[]`):
  - **Label**: "Total Products"
  - **Value**: "150+"
  - **Trend** (optional): `up`
  - **Icon** (optional): "package"
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "product_controller.py"
  - **Code**:
    ```python
    @router.get("/{product_id}", response_model=ProductResponse)
    async def get_product_by_id(product_id: UUID):
        query = GetProductByIdQuery(product_id=ProductId(value=product_id))
        product = await usecase.get_product_by_id(query)
        return ProductResponse.from_entity(product)
    ```
- **GitHub Example URL** (optional): "https://github.com/anomalyco/cinema-plattform/blob/main/concession-service/app/products/infrastructure/api/controllers/product_controller.py"

---

### Feature 2: Combo Meal Management

- **ID**: "combo-management"
- **Title**: "Combo Meal Management"
- **Description**: Create and manage combo meals that bundle multiple products together with discounted pricing. Supports custom discount percentages and product quantity management.
- **Icon**: "layers"
- **Category** (`FeatureCategory`): `api` | `database`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Create combo meals with multiple products
  - Configurable discount percentages
  - Availability toggling
  - Query combos by product inclusion
  - Soft delete with restore capability
- **Tech Stack** (optional):
  - FastAPI
  - SQLAlchemy ORM
  - PostgreSQL
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "combo_controllers.py"
  - **Code**:
    ```python
    @router.post("/", response_model=UUID, status_code=status.HTTP_201_CREATED)
    async def create_combo(request_data: ComboCreateRequest):
        command = ComboCreateCommand(**request_data.model_dump())
        combo = await usecase.create_combo(command)
        return combo.id.value
    ```
- **GitHub Example URL** (optional): "https://github.com/anomalyco/cinema-plattform/blob/main/concession-service/app/combos/infrastructure/api/combo_controllers.py"

---

### Feature 3: Promotional Campaigns

- **ID**: "promotions"
- **Title**: "Promotional Campaigns"
- **Description**: Time-limited promotional campaigns with support for specific products or categories. Includes activation/deactivation, validity extension, and usage tracking.
- **Icon**: "tag"
- **Category** (`FeatureCategory`): `api` | `database` | `security`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Create promotions with start/end dates
  - Link promotions to specific products or categories
  - Activation and deactivation workflows
  - Usage tracking with max uses limit
  - Extend promotion validity
- **Tech Stack** (optional):
  - FastAPI
  - PostgreSQL with JSON rules column
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "promotion_controller.py"
  - **Code**:
    ```python
    class Promotion(BaseModel):
        name: str
        promotion_type: PromotionType
        rule: dict = Field(default_factory=dict)
        start_date: datetime
        end_date: datetime
        applicable_product_ids: List[ProductId] = Field(default_factory=list)
        applicable_categories_ids: List[int] = Field(default_factory=list)
        is_active: bool = True
    ```
- **GitHub Example URL** (optional): "https://github.com/anomalyco/cinema-plattform/blob/main/concession-service/app/promotions/domain/entities/promotion.py"

---

### Feature 4: Category Management

- **ID**: "category-management"
- **Title**: "Product Category Management"
- **Description**: Hierarchical organization of products into categories (e.g., Snacks, Beverages, Combos) with activation status control.
- **Icon**: "folder"
- **Category** (`FeatureCategory`): `api` | `database`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Create and manage product categories
  - Toggle category active status
  - Soft delete for data retention
  - Products linked to categories
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "category_controller.py"
  - **Code**:
    ```python
    router = APIRouter(prefix="/api/v2/categories", tags=["Product Categories"])
    
    @router.post("/", response_model=ProductCategoryResponse)
    async def create_category(category_data: CategoryRequest):
        command = CategoryCreateCommand(**category_data.model_dump())
        category = await useCases.create_category(command)
        return ProductCategoryResponse.model_validate(category)
    ```

---

### Feature 5: Authentication & Authorization

- **ID**: "auth"
- **Title**: "JWT Authentication & Role-Based Access Control"
- **Description**: Secure API endpoints with JWT token validation and role-based authorization for admin and manager operations.
- **Icon**: "shield"
- **Category** (`FeatureCategory`): `authentication` | `security`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - JWT token validation middleware
  - Role-based authorization (admin, manager)
  - Configurable JWT audience and issuer validation
  - Token expiration handling
- **Tech Stack** (optional):
  - PyJWT
  - FastAPI Security
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "security.py"
  - **Code**:
    ```python
    def require_roles(*allowed_roles: str):
        def dependency(request: Request) -> AuthUserContext:
            user = require_authenticated_user(request)
            user_roles = {role.strip().lower() for role in user.roles}
            if not (user_roles & normalized_allowed):
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return user
        return dependency
    ```

---

### Feature 6: Rate Limiting

- **ID**: "rate-limiting"
- **Title**: "API Rate Limiting"
- **Description**: Protection against abuse with configurable rate limits per endpoint using SlowAPI.
- **Icon**: "clock"
- **Category** (`FeatureCategory`): `security` | `performance`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - 60 requests/minute for read endpoints
  - 10 requests/minute for write endpoints
  - Per-client rate limiting using IP address
- **Tech Stack** (optional):
  - SlowAPI

---

### Feature 7: Redis Caching

- **ID**: "caching"
- **Title**: "Redis Caching Layer"
- **Description**: High-performance caching for frequently accessed data to reduce database load and improve response times.
- **Icon**: "database"
- **Category** (`FeatureCategory`): `caching` | `performance`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Redis-based cache service
  - Automatic cache initialization on startup
  - Graceful degradation if Redis unavailable
  - FastAPI-Cache integration

---

### Feature 8: gRPC Inter-Service Communication

- **ID**: "grpc"
- **Title**: "gRPC Service Interface"
- **Description**: High-performance gRPC interface for internal service-to-service communication with the cinema platform.
- **Icon**: "zap"
- **Category** (`FeatureCategory`): `api` | `integration`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - ConcessionCatalogService with 6 RPC methods
  - Product, Combo, and Promotion lookup operations
  - Single and batch retrieval support
  - Separate gRPC server container
- **Tech Stack** (optional):
  - grpcio
  - Protocol Buffers
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "protobuf"
  - **Filename** (optional): "concession.proto"
  - **Code**:
    ```protobuf
    service ConcessionCatalogService {
      rpc GetProductById (EntityByIdRequest) returns (ProductReply) {}
      rpc GetProductsByIds (EntityByIdsRequest) returns (ProductListReply) {}
      rpc GetComboById (EntityByIdRequest) returns (ComboReply) {}
      rpc GetCombosByIds (EntityByIdsRequest) returns (ComboListReply) {}
      rpc GetPromotionById (EntityByIdRequest) returns (PromotionReply) {}
      rpc GetPromotionsByIds (EntityByIdsRequest) returns (PromotionListReply) {}
    }
    ```

---

### Feature 9: Comprehensive Testing

- **ID**: "testing"
- **Title**: "Unit & Integration Testing"
- **Description**: pytest-based testing suite with async support for unit tests, repository tests, and end-to-end API tests.
- **Icon**: "check-circle"
- **Category** (`FeatureCategory`): `testing`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Async test fixtures with pytest-asyncio
  - Repository layer testing with in-memory database
  - E2E API endpoint testing
  - Test database isolation
- **Tech Stack** (optional):
  - pytest
  - pytest-asyncio
  - pytest-mock
  - SQLAlchemy AsyncSession

---

### Feature 10: Docker Containerization

- **ID**: "docker"
- **Title**: "Docker Containerization & Orchestration"
- **Description**: Production-ready Docker setup with multi-container orchestration including load balancing, database, and cache.
- **Icon**: "container"
- **Category** (`FeatureCategory`): `infrastructure` | `performance`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Multi-stage Docker build for optimized image size
  - 3 application instances with nginx load balancing
  - Separate gRPC server container
  - PostgreSQL 16 Alpine database
  - Redis 7 Alpine cache
  - Automatic migration on startup
  - Health checks configured

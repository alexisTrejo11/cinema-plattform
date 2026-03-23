# API Schema

- **Type**: `REST` | `GraphQL` | `SOAP` | `Mixed`

**Note**: The service exposes both REST (for client-facing operations) and gRPC (for inter-service communication) APIs.

---

## HTTP Endpoints (`ApiEndpoint[]`)

### Endpoint 1: Health Check

- **ID**: "health-check"
- **Method**: `GET`
- **URL Path**: "/health"
- **Summary**: "Service Health Check"
- **Description**: "Returns the current health status of the service"
- **Tags**:
  - "Health"
- **Authenticated**: `false`
- **Rate Limit**: "Unlimited"

#### Responses (`ApiResponse[]`)

- **Status**: 200
- **Description**: "Service is healthy"
- **Example**:
  ```json
  {
    "status": "ok",
    "message": "Product Service API is running"
  }
  ```

---

### Endpoint 2: Get Product by ID

- **ID**: "get-product-by-id"
- **Method**: `GET`
- **URL Path**: "/api/v2/products/{product_id}"
- **Summary**: "Get product by ID"
- **Description**: "Retrieve detailed information about a specific food product"
- **Tags**:
  - "Food Products"
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

#### Parameters (`ApiParameter[]`, optional)

- **Name**: "product_id"
- **In**: `path`
- **Type**: "UUID"
- **Required**: `true`
- **Description**: "ID of the product to retrieve"

#### Responses (`ApiResponse[]`)

- **Status**: 200
- **Description**: "Product details"
- **Schema**:
  ```json
  {
    "id": "string (UUID)",
    "name": "string",
    "price": "number",
    "description": "string",
    "image_url": "string",
    "is_available": "boolean",
    "preparation_time_mins": "integer",
    "calories": "integer",
    "category_id": "integer"
  }
  ```

---

### Endpoint 3: Search Products

- **ID**: "search-products"
- **Method**: `GET`
- **URL Path**: "/api/v2/products/"
- **Summary**: "Search food products"
- **Description**: "Search and filter food products with pagination"
- **Tags**:
  - "Food Products"
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

#### Parameters (`ApiParameter[]`, optional)

- **Name**: "name_like"
- **In**: `query`
- **Type**: "string"
- **Required**: `false`
- **Description**: "Filter by product name"

- **Name**: "category_id"
- **In**: `query`
- **Type**: "integer"
- **Required**: `false`
- **Description**: "Filter by category ID"

- **Name**: "min_price"
- **In**: `query`
- **Type**: "number"
- **Required**: `false`
- **Description**: "Minimum price filter"

- **Name**: "max_price"
- **In**: `query`
- **Type**: "number"
- **Required**: `false`
- **Description**: "Maximum price filter"

- **Name**: "available_only"
- **In**: `query`
- **Type**: "boolean"
- **Required**: `false`
- **Description**: "Only show available products"

- **Name**: "page"
- **In**: `query`
- **Type**: "integer"
- **Required**: `false`
- **Description**: "Page number (default: 1)"

- **Name**: "page_size"
- **In**: `query`
- **Type**: "integer"
- **Required**: `false`
- **Description**: "Items per page (default: 10)"

---

### Endpoint 4: Create Product

- **ID**: "create-product"
- **Method**: `POST`
- **URL Path**: "/api/v2/products/"
- **Summary**: "Create a new food product"
- **Description**: "Creates a new food product with the provided details"
- **Tags**:
  - "Food Products"
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

#### Request Body (`ApiRequestBody`, optional)

- **Content Type**: "application/json"
- **Schema**:
  ```json
  {
    "name": "string",
    "price": "number",
    "category_id": "integer",
    "description": "string",
    "image_url": "string",
    "preparation_time_mins": "integer",
    "calories": "integer",
    "is_available": "boolean"
  }
  ```

#### Responses (`ApiResponse[]`)

- **Status**: 201
- **Description**: "Product created successfully"

---

### Endpoint 5: Update Product

- **ID**: "update-product"
- **Method**: `PATCH`
- **URL Path**: "/api/v2/products/{product_id}"
- **Summary**: "Update a food product"
- **Description**: "Update details of an existing food product"
- **Tags**:
  - "Food Products"
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

#### Parameters (`ApiParameter[]`, optional)

- **Name**: "product_id"
- **In**: `path`
- **Type**: "UUID"
- **Required**: `true`
- **Description**: "ID of the product to update"

#### Request Body (`ApiRequestBody`, optional)

- **Content Type**: "application/json"
- **Schema**:
  ```json
  {
    "name": "string (optional)",
    "price": "number (optional)",
    "description": "string (optional)",
    "image_url": "string (optional)",
    "is_available": "boolean (optional)",
    "preparation_time_mins": "integer (optional)",
    "calories": "integer (optional)"
  }
  ```

---

### Endpoint 6: Delete Product

- **ID**: "delete-product"
- **Method**: `DELETE`
- **URL Path**: "/api/v2/products/{product_id}"
- **Summary**: "Delete a food product"
- **Description**: "Permanently remove a food product from the system"
- **Tags**:
  - "Food Products"
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

#### Responses (`ApiResponse[]`)

- **Status**: 204
- **Description**: "Product deleted successfully"

---

### Endpoint 7: List Categories

- **ID**: "list-categories"
- **Method**: `GET`
- **URL Path**: "/api/v2/categories/"
- **Summary**: "List all product categories"
- **Description**: "Retrieve a list of all product categories"
- **Tags**:
  - "Product Categories"
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

#### Responses (`ApiResponse[]`)

- **Status**: 200
- **Description**: "List of categories"
- **Schema**:
  ```json
  [
    {
      "id": "integer",
      "name": "string",
      "description": "string",
      "is_active": "boolean"
    }
  ]
  ```

---

### Endpoint 8: Create Category

- **ID**: "create-category"
- **Method**: `POST`
- **URL Path**: "/api/v2/categories/"
- **Summary**: "Create a new product category"
- **Description**: "Creates a new product category with the provided details"
- **Tags**:
  - "Product Categories"
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

#### Request Body (`ApiRequestBody`, optional)

- **Content Type**: "application/json"
- **Schema**:
  ```json
  {
    "name": "string",
    "description": "string",
    "is_active": "boolean"
  }
  ```

---

### Endpoint 9: Get Combo by ID

- **ID**: "get-combo-by-id"
- **Method**: `GET`
- **URL Path**: "/api/v2/combos/{combo_id}"
- **Summary**: "Get combo by ID"
- **Description**: "Retrieve detailed information about a specific combo"
- **Tags**:
  - "Combos"
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

#### Parameters (`ApiParameter[]`, optional)

- **Name**: "include_items"
- **In**: `query`
- **Type**: "boolean"
- **Required**: `false`
- **Description**: "Whether to include combo items in the response"

---

### Endpoint 10: Get Active Combos

- **ID**: "get-active-combos"
- **Method**: `GET`
- **URL Path**: "/api/v2/combos/"
- **Summary**: "Get active combos"
- **Description**: "Retrieve a list of currently available combos"
- **Tags**:
  - "Combos"
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

---

### Endpoint 11: Create Combo

- **ID**: "create-combo"
- **Method**: `POST`
- **URL Path**: "/api/v2/combos/"
- **Summary**: "Create a new combo"
- **Description**: "Creates a new combo meal with the provided details"
- **Tags**:
  - "Combos"
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

#### Request Body (`ApiRequestBody`, optional)

- **Content Type**: "application/json"
- **Schema**:
  ```json
  {
    "name": "string",
    "description": "string",
    "price": "number",
    "discount_percentage": "number",
    "image_url": "string",
    "is_available": "boolean",
    "items": [
      {
        "product_id": "UUID",
        "quantity": "integer"
      }
    ]
  }
  ```

---

### Endpoint 12: Restore Combo

- **ID**: "restore-combo"
- **Method**: `POST`
- **URL Path**: "/api/v2/combos/{combo_id}/restore"
- **Summary**: "Restore a deleted combo"
- **Description**: "Restore a deleted combo"
- **Tags**:
  - "Combos"
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

### Endpoint 13: Delete Combo

- **ID**: "delete-combo"
- **Method**: `DELETE`
- **URL Path**: "/api/v2/combos/{combo_id}"
- **Summary**: "Delete a combo"
- **Description**: "Remove a combo from the system"
- **Tags**:
  - "Combos"
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

### Endpoint 14: Get Active Promotions

- **ID**: "get-active-promotions"
- **Method**: `GET`
- **URL Path**: "/api/v2/promotions/active"
- **Summary**: "Get all active promotions"
- **Description**: "Retrieves a paginated list of all active promotions"
- **Tags**:
  - "Promotions"
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

---

### Endpoint 15: Get Promotions by Product

- **ID**: "get-promotions-by-product"
- **Method**: `GET`
- **URL Path**: "/api/v2/promotions/product/{product_id}"
- **Summary**: "Get promotions by product ID"
- **Description**: "Retrieves a paginated list of promotions applicable to a specific product"
- **Tags**:
  - "Promotions"
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

---

### Endpoint 16: Get Promotion by ID

- **ID**: "get-promotion-by-id"
- **Method**: `GET`
- **URL Path**: "/api/v2/promotions/{promotion_id}"
- **Summary**: "Get promotion by ID"
- **Description**: "Retrieves a single promotion by its unique ID"
- **Tags**:
  - "Promotions"
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

---

### Endpoint 17: Create Promotion

- **ID**: "create-promotion"
- **Method**: `POST`
- **URL Path**: "/api/v2/promotions/"
- **Summary**: "Create a new promotion"
- **Description**: "Creates a new promotion in the system"
- **Tags**:
  - "Promotions"
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

#### Request Body (`ApiRequestBody`, optional)

- **Content Type**: "application/json"
- **Schema**:
  ```json
  {
    "name": "string",
    "promotion_type": "string",
    "rule": "object",
    "start_date": "datetime",
    "end_date": "datetime",
    "description": "string",
    "applicable_product_ids": ["UUID"],
    "applicable_categories_ids": ["integer"],
    "max_uses": "integer"
  }
  ```

---

### Endpoint 18: Activate Promotion

- **ID**: "activate-promotion"
- **Method**: `PATCH`
- **URL Path**: "/api/v2/promotions/{promotion_id}/activate"
- **Summary**: "Activate a promotion"
- **Description**: "Activates an existing promotion by its ID"
- **Tags**:
  - "Promotions"
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

### Endpoint 19: Deactivate Promotion

- **ID**: "deactivate-promotion"
- **Method**: `PATCH`
- **URL Path**: "/api/v2/promotions/{promotion_id}/deactivate"
- **Summary**: "Deactivate a promotion"
- **Description**: "Deactivates an existing promotion by its ID"
- **Tags**:
  - "Promotions"
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

### Endpoint 20: Extend Promotion

- **ID**: "extend-promotion"
- **Method**: `PATCH`
- **URL Path**: "/api/v2/promotions/{promotion_id}/extend"
- **Summary**: "Extend a promotion's end date"
- **Description**: "Extends the end date of an existing promotion"
- **Tags**:
  - "Promotions"
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

### Endpoint 21: Apply Promotion

- **ID**: "apply-promotion"
- **Method**: `PATCH`
- **URL Path**: "/api/v2/promotions/{promotion_id}/apply"
- **Summary**: "Apply a promotion to products"
- **Description**: "Applies a promotion to specified products"
- **Tags**:
  - "Promotions"
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

### Endpoint 22: Delete Promotion

- **ID**: "delete-promotion"
- **Method**: `DELETE`
- **URL Path**: "/api/v2/promotions/{promotion_id}"
- **Summary**: "Delete a promotion"
- **Description**: "Deletes an existing promotion by its ID"
- **Tags**:
  - "Promotions"
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

### Endpoint 23: Add Products to Promotion

- **ID**: "add-products-to-promotion"
- **Method**: `POST`
- **URL Path**: "/api/v2/promotions/products/add"
- **Summary**: "Add products to a promotion"
- **Description**: "Add products to an existing promotion"
- **Tags**:
  - "Promotions Items"
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

### Endpoint 24: Add Category to Promotion

- **ID**: "add-category-to-promotion"
- **Method**: `POST`
- **URL Path**: "/api/v2/promotions/categories/add"
- **Summary**: "Add category to a promotion"
- **Description**: "Add a category to an existing promotion"
- **Tags**:
  - "Promotions Items"
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

### Endpoint 25: Remove Category from Promotion

- **ID**: "remove-category-from-promotion"
- **Method**: `DELETE`
- **URL Path**: "/api/v2/promotions/categories/remove"
- **Summary**: "Remove category from a promotion"
- **Description**: "Remove a category from an existing promotion"
- **Tags**:
  - "Promotions Items"
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

### Endpoint 26: Remove Products from Promotion

- **ID**: "remove-products-from-promotion"
- **Method**: `DELETE`
- **URL Path**: "/api/v2/promotions/products/remove"
- **Summary**: "Remove products from a promotion"
- **Description**: "Remove products from an existing promotion"
- **Tags**:
  - "Promotions Items"
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

## gRPC Services

### ConcessionCatalogService

**Package**: `concession`

**Service Definition**:
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

**Messages**:

- `EntityByIdRequest`: `{ id: string }`
- `EntityByIdsRequest`: `{ ids: string[] }`
- `ProductReply`: `{ exists: bool, data: ProductData }`
- `ProductListReply`: `{ items: ProductReply[] }`
- `ComboReply`: `{ exists: bool, data: ComboData }`
- `ComboListReply`: `{ items: ComboReply[] }`
- `PromotionReply`: `{ exists: bool, data: PromotionData }`
- `PromotionListReply`: `{ items: PromotionReply[] }`

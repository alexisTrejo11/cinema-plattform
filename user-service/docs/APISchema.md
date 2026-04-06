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
    "message": "User Service API is running"
  }
  ```

---

### Endpoint 2: User Signup

- **ID**: "signup"
- **Method**: `POST`
- **URL Path**: "/api/v2/auth/signup"
- **Summary**: "Register a new user"
- **Description**: "Allows a new user to sign up by providing their details. Returns the created user's information."
- **Tags**:
  - "auth"
- **Authenticated**: `false`
- **Rate Limit**: "30/minute"

#### Request Body (`ApiRequestBody`, optional)

- **Content Type**: "application/json"
- **Schema**:
  ```json
  {
    "email": "string (EmailStr)",
    "password": "string",
    "first_name": "string",
    "last_name": "string",
    "date_of_birth": "date",
    "gender": "MALE | FEMALE | OTHER",
    "phone_number": "string (optional)"
  }
  ```

#### Responses (`ApiResponse[]`)

- **Status**: 201
- **Description**: "User created successfully"
- **Schema**:
  ```json
  {
    "id": "integer",
    "email": "string",
    "role": "CUSTOMER | ADMIN | EMPLOYEE | MANAGER",
    "status": "PENDING | ACTIVE | INACTIVE | BANNED"
  }
  ```

---

### Endpoint 3: User Login

- **ID**: "login"
- **Method**: `POST`
- **URL Path**: "/api/v2/auth/login"
- **Summary**: "Authenticate user and get tokens"
- **Description**: "Authenticates a user with their credentials and returns access and refresh tokens."
- **Tags**:
  - "auth"
- **Authenticated**: `false`
- **Rate Limit**: "30/minute"

#### Request Body (`ApiRequestBody`, optional)

- **Content Type**: "application/json"
- **Schema**:
  ```json
  {
    "identifier_field": "string (email or username)",
    "password": "string",
    "twoFACode": "string (optional)"
  }
  ```

#### Responses (`ApiResponse[]`)

- **Status**: 200
- **Description**: "Authentication successful"
- **Schema**:
  ```json
  {
    "access_token": "string",
    "refresh_token": "string",
    "expires_in_minutes": "integer",
    "token_type": "bearer"
  }
  ```

---

### Endpoint 4: Logout

- **ID**: "logout"
- **Method**: `POST`
- **URL Path**: "/api/v2/auth/logout"
- **Summary**: "Log out a user from a specific session"
- **Description**: "Invalidates a specific refresh token, effectively logging out the user from that session."
- **Tags**:
  - "auth"
- **Authenticated**: `true`
- **Rate Limit**: "30/minute"

#### Request Body (`ApiRequestBody`, optional)

- **Content Type**: "application/json"
- **Schema**:
  ```json
  {
    "refresh_token": "string"
  }
  ```

#### Responses (`ApiResponse[]`)

- **Status**: 204
- **Description**: "Logout successful"

---

### Endpoint 5: Logout All Sessions

- **ID**: "logout-all"
- **Method**: `POST`
- **URL Path**: "/api/v2/auth/logout-all"
- **Summary**: "Log out user from all sessions"
- **Description**: "Invalidates all refresh tokens for the current user, logging them out from all active sessions."
- **Tags**:
  - "auth"
- **Authenticated**: `true`
- **Rate Limit**: "30/minute"

#### Responses (`ApiResponse[]`)

- **Status**: 204
- **Description**: "All sessions invalidated"

---

### Endpoint 6: Refresh Token

- **ID**: "refresh"
- **Method**: `POST`
- **URL Path**: "/api/v2/auth/refresh"
- **Summary**: "Refresh access token"
- **Description**: "Exchanges a valid refresh token for a new access token and refresh token pair."
- **Tags**:
  - "auth"
- **Authenticated**: `true`
- **Rate Limit**: "30/minute"

#### Request Body (`ApiRequestBody`, optional)

- **Content Type**: "application/json"
- **Schema**:
  ```json
  {
    "refresh_token": "string"
  }
  ```

---

### Endpoint 7: Enable 2FA

- **ID**: "enable-2fa"
- **Method**: `PATCH`
- **URL Path**: "/api/v2/auth/2FA/enable"
- **Summary**: "Enable two-factor authentication"
- **Description**: "Enables TOTP-based 2FA for the authenticated user, returning a QR code and secret."
- **Tags**:
  - "auth"
- **Authenticated**: `true`
- **Rate Limit**: "30/minute"

#### Responses (`ApiResponse[]`)

- **Status**: 200
- **Description**: "2FA enabled"
- **Schema**:
  ```json
  {
    "qr_code": "string",
    "secret": "string"
  }
  ```

---

### Endpoint 8: Disable 2FA

- **ID**: "disable-2fa"
- **Method**: `PATCH`
- **URL Path**: "/api/v2/auth/2FA/disable"
- **Summary**: "Disable two-factor authentication"
- **Description**: "Disables 2FA for the authenticated user."
- **Tags**:
  - "auth"
- **Authenticated**: `true`
- **Rate Limit**: "30/minute"

#### Parameters (`ApiParameter[]`, optional)

- **Name**: "token"
- **In**: `query`
- **Type**: "string"
- **Required**: `false`
- **Description**: "Current 2FA token to verify before disabling"

---

### Endpoint 9: List Users (Admin)

- **ID**: "list-users"
- **Method**: `GET`
- **URL Path**: "/api/v2/users/"
- **Summary**: "Retrieve a list of all users"
- **Description**: "Fetches a paginated list of all registered users. Requires 'admin' role."
- **Tags**:
  - "Users Management"
- **Authenticated**: `true`
- **Rate Limit**: "30/minute"

#### Parameters (`ApiParameter[]`, optional)

- **Name**: "offset"
- **In**: `query`
- **Type**: "integer"
- **Required**: `false`
- **Description**: "Number of users to skip (default: 0)"
- **Example** (optional): 0

- **Name**: "limit"
- **In**: `query`
- **Type**: "integer"
- **Required**: `false`
- **Description**: "Max users to return (default: 10, max: 100)"
- **Example** (optional): 10

---

### Endpoint 10: Get User by ID (Admin)

- **ID**: "get-user"
- **Method**: `GET`
- **URL Path**: "/api/v2/users/{user_id}"
- **Summary**: "Retrieve a single user by ID"
- **Description**: "Fetches detailed information for a specific user using their unique ID. Requires 'admin' role."
- **Tags**:
  - "Users Management"
- **Authenticated**: `true`
- **Rate Limit**: "30/minute"

#### Parameters (`ApiParameter[]`, optional)

- **Name**: "user_id"
- **In**: `path`
- **Type**: "integer"
- **Required**: `true`
- **Description**: "ID of the user to retrieve"

---

### Endpoint 11: Create User (Admin)

- **ID**: "create-user"
- **Method**: `POST`
- **URL Path**: "/api/v2/users/"
- **Summary**: "Create a new user"
- **Description**: "Registers a new user in the system. Requires 'admin' role."
- **Tags**:
  - "Users Management"
- **Authenticated**: `true`
- **Rate Limit**: "30/minute"

#### Request Body (`ApiRequestBody`, optional)

- **Content Type**: "application/json"
- **Schema**:
  ```json
  {
    "email": "string",
    "password": "string",
    "first_name": "string",
    "last_name": "string",
    "phone_number": "string",
    "date_of_birth": "date",
    "gender": "MALE | FEMALE | OTHER",
    "role": "CUSTOMER | EMPLOYEE | MANAGER"
  }
  ```

---

### Endpoint 12: Update User (Admin)

- **ID**: "update-user"
- **Method**: `PUT`
- **URL Path**: "/api/v2/users/{user_id}"
- **Summary**: "Update an existing user"
- **Description**: "Updates the details of an existing user identified by their ID. Requires 'admin' role."
- **Tags**:
  - "Users Management"
- **Authenticated**: `true`
- **Rate Limit**: "30/minute"

#### Parameters (`ApiParameter[]`, optional)

- **Name**: "user_id"
- **In**: `path`
- **Type**: "integer"
- **Required**: `true`
- **Description**: "ID of the user to update"

---

### Endpoint 13: Delete User (Admin)

- **ID**: "delete-user"
- **Method**: `DELETE`
- **URL Path**: "/api/v2/users/{user_id}"
- **Summary**: "Delete a user by ID"
- **Description**: "Deletes a user from the system using their unique ID. Requires 'admin' role."
- **Tags**:
  - "Users Management"
- **Authenticated**: `true`
- **Rate Limit**: "30/minute"

---

### Endpoint 14: Activate User (Admin)

- **ID**: "activate-user"
- **Method**: `PATCH`
- **URL Path**: "/api/v2/users/{user_id}/activate"
- **Summary**: "Activate a user by ID"
- **Description**: "Activates a user account. Requires 'admin' role."
- **Tags**:
  - "Users Management"
- **Authenticated**: `true`
- **Rate Limit**: "30/minute"

#### Parameters (`ApiParameter[]`, optional)

- **Name**: "activation_token"
- **In**: `query`
- **Type**: "string"
- **Required**: `false`
- **Description**: "Optional activation token"

---

### Endpoint 15: Ban User (Admin)

- **ID**: "ban-user"
- **Method**: `PATCH`
- **URL Path**: "/api/v2/users/{user_id}/ban"
- **Summary**: "Ban a user by ID"
- **Description**: "Bans a user account. Requires 'admin' role."
- **Tags**:
  - "Users Management"
- **Authenticated**: `true`
- **Rate Limit**: "30/minute"

---

### Endpoint 16: Get My Profile

- **ID**: "get-my-profile"
- **Method**: `GET`
- **URL Path**: "/api/v2/profiles/"
- **Summary**: "Retrieve the authenticated user's profile"
- **Description**: "Fetches the detailed profile information for the currently authenticated user."
- **Tags**:
  - "User Profiles"
- **Authenticated**: `true`
- **Rate Limit**: "30/minute"

---

### Endpoint 17: Update My Profile

- **ID**: "update-my-profile"
- **Method**: `PATCH`
- **URL Path**: "/api/v2/profiles/"
- **Summary**: "Update the authenticated user's profile"
- **Description**: "Updates specific fields of the currently authenticated user's profile. Partial updates are supported."
- **Tags**:
  - "User Profiles"
- **Authenticated**: `true`
- **Rate Limit**: "30/minute"

#### Request Body (`ApiRequestBody`, optional)

- **Content Type**: "application/json"
- **Schema**:
  ```json
  {
    "first_name": "string (optional)",
    "last_name": "string (optional)",
    "phone_number": "string (optional)",
    "date_of_birth": "date (optional)",
    "gender": "MALE | FEMALE | OTHER (optional)"
  }
  ```

---

## gRPC Services

### UsersService

**Package**: `users`

**Service Definition**:
```protobuf
service UsersService {
  rpc GetUserById (UserByIdRequest) returns (UserResponse) {}
  rpc GetUsersByIds (UsersByIdsRequest) returns (UsersListResponse) {}
  rpc GetUserByEmail (UserByEmailRequest) returns (UserResponse) {}
}
```

**Messages**:

- `UserByIdRequest`: `{ user_id: int64 }`
- `UsersByIdsRequest`: `{ user_ids: int64[] }`
- `UserByEmailRequest`: `{ email: string }`
- `UserResponse`: `{ id, email, role, status, profile_data... }`
- `UsersListResponse`: `{ users: UserResponse[] }`

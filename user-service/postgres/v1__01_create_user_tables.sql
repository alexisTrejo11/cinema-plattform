CREATE TYPE gender_enum AS ENUM ('MALE', 'FEMALE', 'OTHER');
CREATE TYPE role_enum AS ENUM ('CUSTOMER', 'EMPLOYEE', 'MANAGER', 'ADMIN');
CREATE TYPE user_status_enum AS ENUM ('PENDING', 'ACTIVE', 'INACTIVE', 'BANNED');


CREATE TABLE users (
    id SERIAL PRIMARY KEY,    
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    phone_number VARCHAR(20) UNIQUE,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255),
    role role_enum NOT NULL,
    gender gender_enum NOT NULL,
    status user_status_enum NOT NULL DEFAULT 'PENDING',
    date_of_birth TIMESTAMP NOT NULL,
    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
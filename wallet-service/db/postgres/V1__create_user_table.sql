DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role_enum') THEN
        CREATE TYPE user_role_enum AS ENUM ('ADMIN', 'MANAGER', 'EMPLOYEE', 'CUSTOMER');
    END IF;
END $$;

-- Create currency_enum type
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'currency_enum') THEN
        CREATE TYPE currency_enum AS ENUM ('MXN', 'USD', 'EUR');
    END IF;
END $$;

-- Create transaction_type_enum type
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'transaction_type_enum') THEN
        CREATE TYPE transaction_type_enum AS ENUM ('ADD_CREDIT', 'BUY_PRODUCT', 'REFUND', 'TRANSFER_IN', 'TRANSFER_OUT');
    END IF;
END $$;


CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    roles user_role_enum[] NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    deleted_at TIMESTAMP WITHOUT TIME ZONE
);

CREATE UNIQUE INDEX idx_users_email ON users (email);

CREATE INDEX idx_users_is_active ON users (is_active);

CREATE INDEX idx_users_roles ON users USING GIN (roles);

CREATE INDEX idx_users_active_created_at ON users (is_active, created_at DESC);

CREATE INDEX idx_users_deleted_at ON users (deleted_at);


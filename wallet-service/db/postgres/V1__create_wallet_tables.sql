-- Create cinema_wallets table
CREATE TABLE cinema_wallets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    balance_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    balance_currency currency_enum NOT NULL DEFAULT 'USD',
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    deleted_at TIMESTAMP WITHOUT TIME ZONE,
    
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
);

-- Create wallet_transactions table
CREATE TABLE wallet_transactions (
    transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    wallet_id UUID NOT NULL,
    amount_value DECIMAL(10, 2) NOT NULL,
    amount_currency currency_enum NOT NULL,
    transaction_type transaction_type_enum NOT NULL,
    payment_method VARCHAR(255) NOT NULL,
    payment_reference VARCHAR(255),
    timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),

    CONSTRAINT fk_wallet
        FOREIGN KEY (wallet_id)
        REFERENCES cinema_wallets (id)
        ON DELETE CASCADE
);


-- Indexes for cinema_wallets table
CREATE INDEX idx_cinema_wallets_user_id ON cinema_wallets (user_id);
-- CREATE INDEX idx_cinema_wallets_balance ON cinema_wallets (balance_amount, balance_currency);

-- Indexes for wallet_transactions table
CREATE INDEX idx_wallet_transactions_wallet_id ON wallet_transactions (wallet_id);
CREATE INDEX idx_wallet_transactions_type ON wallet_transactions (transaction_type);
CREATE INDEX idx_wallet_transactions_timestamp ON wallet_transactions (timestamp DESC);
CREATE INDEX idx_wallet_transactions_wallet_id_timestamp ON wallet_transactions (wallet_id, timestamp DESC);
CREATE INDEX idx_wallet_transactions_currency ON wallet_transactions (amount_currency);
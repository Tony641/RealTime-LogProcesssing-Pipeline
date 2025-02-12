CREATE TABLE search_events (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    search_query TEXT NOT NULL,
    timestamp BIGINT NOT NULL
);

CREATE TABLE user_activity (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    product_id UUID NOT NULL,
    event_type TEXT NOT NULL,
    timestamp BIGINT NOT NULL
);

CREATE TABLE product_catalog (
    product_id UUID PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price DECIMAL NOT NULL
);

CREATE TABLE user_features (
    user_id UUID PRIMARY KEY,
    product_id UUID NOT NULL,
    search_count INT DEFAULT 0,
    clicks INT DEFAULT 0,
    views INT DEFAULT 0,
    purchases INT DEFAULT 0
);

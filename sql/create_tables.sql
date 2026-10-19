CREATE TABLE IF NOT EXISTS siagrow.orders
(
    record_id     String,
    source        LowCardinality(String),
    source_id     String,
    sender        String,
    customer_name String,
    product       String,
    quantity      UInt32,
    unit_price    Float64,
    total_amount  Float64,
    city          LowCardinality(String),
    order_date    DateTime,
    received_at   DateTime,
    ingested_at   DateTime
)
ENGINE = ReplacingMergeTree(ingested_at)
PARTITION BY toYYYYMM(order_date)
ORDER BY (source, record_id);

CREATE VIEW IF NOT EXISTS siagrow.orders_clean AS
SELECT * FROM siagrow.orders FINAL;
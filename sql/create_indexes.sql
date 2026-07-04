-- -------------------------------------------------------------------
-- Index creation script
-- Project: PayLive AI Copilot
-- Database: paylive_ai_copilot
--
-- This script creates indexes used to optimize:
-- - joins between relational tables;
-- - filters by seller, customer, live session, product and platform;
-- - date-based queries;
-- - analytics queries;
-- - future REST API endpoints.
--
-- Execution context:
-- This script must be executed on the paylive_ai_copilot database,
-- after sql/03_create_tables.sql.
--
-- Docker execution example:
-- docker cp sql/04_create_indexes.sql paylive_postgres:/tmp/04_create_indexes.sql
-- docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -f /tmp/04_create_indexes.sql
-- -------------------------------------------------------------------


-- -------------------------------------------------------------------
-- CORE.SELLERS
-- -------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_sellers_main_platform
    ON core.sellers (main_platform);

CREATE INDEX IF NOT EXISTS idx_sellers_seller_status
    ON core.sellers (seller_status);

CREATE INDEX IF NOT EXISTS idx_sellers_country
    ON core.sellers (country);


-- -------------------------------------------------------------------
-- CORE.CUSTOMERS
-- -------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_customers_platform
    ON core.customers (platform);

CREATE INDEX IF NOT EXISTS idx_customers_country
    ON core.customers (country);

CREATE INDEX IF NOT EXISTS idx_customers_created_at
    ON core.customers (created_at);


-- -------------------------------------------------------------------
-- CORE.PRODUCTS
-- -------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_products_category
    ON core.products (category);

CREATE INDEX IF NOT EXISTS idx_products_product_status
    ON core.products (product_status);

CREATE INDEX IF NOT EXISTS idx_products_source
    ON core.products (source);

CREATE INDEX IF NOT EXISTS idx_products_unit_price
    ON core.products (unit_price);


-- -------------------------------------------------------------------
-- CORE.LIVE_SESSIONS
-- -------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_live_sessions_seller_id
    ON core.live_sessions (seller_id);

CREATE INDEX IF NOT EXISTS idx_live_sessions_platform
    ON core.live_sessions (platform);

CREATE INDEX IF NOT EXISTS idx_live_sessions_live_status
    ON core.live_sessions (live_status);

CREATE INDEX IF NOT EXISTS idx_live_sessions_actual_start_at
    ON core.live_sessions (actual_start_at);

CREATE INDEX IF NOT EXISTS idx_live_sessions_created_at
    ON core.live_sessions (created_at);

CREATE INDEX IF NOT EXISTS idx_live_sessions_seller_platform
    ON core.live_sessions (seller_id, platform);


-- -------------------------------------------------------------------
-- CORE.LIVE_PRODUCTS
-- -------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_live_products_live_id
    ON core.live_products (live_id);

CREATE INDEX IF NOT EXISTS idx_live_products_product_id
    ON core.live_products (product_id);

CREATE INDEX IF NOT EXISTS idx_live_products_live_product
    ON core.live_products (live_id, product_id);


-- -------------------------------------------------------------------
-- CORE.LIVE_COMMENTS
-- -------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_live_comments_live_id
    ON core.live_comments (live_id);

CREATE INDEX IF NOT EXISTS idx_live_comments_customer_id
    ON core.live_comments (customer_id);

CREATE INDEX IF NOT EXISTS idx_live_comments_platform
    ON core.live_comments (platform);

CREATE INDEX IF NOT EXISTS idx_live_comments_intent
    ON core.live_comments (manual_intent_label);

CREATE INDEX IF NOT EXISTS idx_live_comments_commented_at
    ON core.live_comments (commented_at);

CREATE INDEX IF NOT EXISTS idx_live_comments_live_intent
    ON core.live_comments (live_id, manual_intent_label);


-- -------------------------------------------------------------------
-- CORE.CARTS
-- -------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_carts_live_id
    ON core.carts (live_id);

CREATE INDEX IF NOT EXISTS idx_carts_customer_id
    ON core.carts (customer_id);

CREATE INDEX IF NOT EXISTS idx_carts_cart_status
    ON core.carts (cart_status);

CREATE INDEX IF NOT EXISTS idx_carts_created_at
    ON core.carts (created_at);

CREATE INDEX IF NOT EXISTS idx_carts_live_status
    ON core.carts (live_id, cart_status);


-- -------------------------------------------------------------------
-- CORE.CART_ITEMS
-- -------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_cart_items_cart_id
    ON core.cart_items (cart_id);

CREATE INDEX IF NOT EXISTS idx_cart_items_product_id
    ON core.cart_items (product_id);

CREATE INDEX IF NOT EXISTS idx_cart_items_cart_product
    ON core.cart_items (cart_id, product_id);


-- -------------------------------------------------------------------
-- CORE.ORDERS
-- -------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_orders_cart_id
    ON core.orders (cart_id);

CREATE INDEX IF NOT EXISTS idx_orders_customer_id
    ON core.orders (customer_id);

CREATE INDEX IF NOT EXISTS idx_orders_seller_id
    ON core.orders (seller_id);

CREATE INDEX IF NOT EXISTS idx_orders_order_status
    ON core.orders (order_status);

CREATE INDEX IF NOT EXISTS idx_orders_created_at
    ON core.orders (created_at);

CREATE INDEX IF NOT EXISTS idx_orders_seller_status
    ON core.orders (seller_id, order_status);


-- -------------------------------------------------------------------
-- CORE.PAYMENTS
-- -------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_payments_order_id
    ON core.payments (order_id);

CREATE INDEX IF NOT EXISTS idx_payments_payment_status
    ON core.payments (payment_status);

CREATE INDEX IF NOT EXISTS idx_payments_paid_at
    ON core.payments (paid_at);

CREATE INDEX IF NOT EXISTS idx_payments_provider
    ON core.payments (payment_provider);

CREATE INDEX IF NOT EXISTS idx_payments_order_status
    ON core.payments (order_id, payment_status);


-- -------------------------------------------------------------------
-- CORE.STOCK_MOVEMENTS
-- -------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_stock_movements_product_id
    ON core.stock_movements (product_id);

CREATE INDEX IF NOT EXISTS idx_stock_movements_live_id
    ON core.stock_movements (live_id);

CREATE INDEX IF NOT EXISTS idx_stock_movements_created_at
    ON core.stock_movements (created_at);

CREATE INDEX IF NOT EXISTS idx_stock_movements_movement_type
    ON core.stock_movements (movement_type);


-- -------------------------------------------------------------------
-- CORE.LIVE_EVENTS
-- -------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_live_events_live_id
    ON core.live_events (live_id);

CREATE INDEX IF NOT EXISTS idx_live_events_customer_id
    ON core.live_events (customer_id);

CREATE INDEX IF NOT EXISTS idx_live_events_event_type
    ON core.live_events (event_type);

CREATE INDEX IF NOT EXISTS idx_live_events_event_timestamp
    ON core.live_events (event_timestamp);

CREATE INDEX IF NOT EXISTS idx_live_events_source_system
    ON core.live_events (source_system);

CREATE INDEX IF NOT EXISTS idx_live_events_live_type
    ON core.live_events (live_id, event_type);


-- -------------------------------------------------------------------
-- ANALYTICS.DATASET_FINAL_LIVE_SALES
-- -------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_dataset_final_live_sales_seller_id
    ON analytics.dataset_final_live_sales (seller_id);

CREATE INDEX IF NOT EXISTS idx_dataset_final_live_sales_platform
    ON analytics.dataset_final_live_sales (platform);

CREATE INDEX IF NOT EXISTS idx_dataset_final_live_sales_live_date
    ON analytics.dataset_final_live_sales (live_date);

CREATE INDEX IF NOT EXISTS idx_dataset_final_live_sales_live_status
    ON analytics.dataset_final_live_sales (live_status);

CREATE INDEX IF NOT EXISTS idx_dataset_final_live_sales_total_revenue
    ON analytics.dataset_final_live_sales (total_revenue);

CREATE INDEX IF NOT EXISTS idx_dataset_final_live_sales_conversion_rate
    ON analytics.dataset_final_live_sales (conversion_rate);

CREATE INDEX IF NOT EXISTS idx_dataset_final_live_sales_top_category
    ON analytics.dataset_final_live_sales (top_product_category);

CREATE INDEX IF NOT EXISTS idx_dataset_final_live_sales_seller_date
    ON analytics.dataset_final_live_sales (seller_id, live_date);

CREATE INDEX IF NOT EXISTS idx_dataset_final_live_sales_platform_date
    ON analytics.dataset_final_live_sales (platform, live_date);


-- -------------------------------------------------------------------
-- AUDIT IMPORT TABLES
-- -------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_import_batches_status
    ON audit.import_batches (status);

CREATE INDEX IF NOT EXISTS idx_import_batches_started_at
    ON audit.import_batches (started_at);

CREATE INDEX IF NOT EXISTS idx_import_logs_batch_id
    ON audit.import_logs (import_batch_id);

CREATE INDEX IF NOT EXISTS idx_import_logs_table_name
    ON audit.import_logs (schema_name, table_name);

CREATE INDEX IF NOT EXISTS idx_import_logs_status
    ON audit.import_logs (status);

CREATE INDEX IF NOT EXISTS idx_import_logs_imported_at
    ON audit.import_logs (imported_at);


-- -------------------------------------------------------------------
-- INDEX COMMENTS
-- -------------------------------------------------------------------

COMMENT ON INDEX core.idx_live_sessions_seller_id IS
'Optimizes joins and filters between sellers and live sessions.';

COMMENT ON INDEX core.idx_live_comments_live_id IS
'Optimizes aggregation of comments by live session.';

COMMENT ON INDEX core.idx_carts_live_id IS
'Optimizes aggregation of carts by live session.';

COMMENT ON INDEX core.idx_orders_cart_id IS
'Optimizes joins between carts and orders.';

COMMENT ON INDEX core.idx_payments_order_id IS
'Optimizes joins between orders and payments.';

COMMENT ON INDEX core.idx_live_events_live_id IS
'Optimizes aggregation of behavioral and technical events by live session.';

COMMENT ON INDEX analytics.idx_dataset_final_live_sales_seller_id IS
'Optimizes analytics and API filters by seller.';

COMMENT ON INDEX analytics.idx_dataset_final_live_sales_live_date IS
'Optimizes analytics and API filters by live date.';

COMMENT ON INDEX analytics.idx_dataset_final_live_sales_conversion_rate IS
'Optimizes future AI and analytics queries using conversion rate.';

COMMENT ON INDEX audit.idx_import_logs_batch_id IS
'Optimizes access to import logs by import batch.';
-- -------------------------------------------------------------------
-- Table creation script
-- Project: PayLive AI Copilot
-- Database: paylive_ai_copilot
--
-- This script creates:
-- - core business tables;
-- - analytics final AI dataset table;
-- - audit import tracking tables.
--
-- Execution context:
-- This script must be executed on the paylive_ai_copilot database,
-- after sql/02_create_schemas.sql.
--
-- Docker execution example:
-- docker cp sql/03_create_tables.sql paylive_postgres:/tmp/03_create_tables.sql
-- docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -f /tmp/03_create_tables.sql
-- -------------------------------------------------------------------


-- -------------------------------------------------------------------
-- CORE SCHEMA
-- -------------------------------------------------------------------


CREATE TABLE IF NOT EXISTS core.sellers (
    seller_id TEXT PRIMARY KEY,
    shop_name TEXT,
    owner_first_name TEXT,
    owner_last_name TEXT,
    email TEXT,
    phone_number TEXT,
    country VARCHAR(100),
    main_platform VARCHAR(50),
    created_at TIMESTAMP,
    seller_status VARCHAR(50),
    cleaned_at TIMESTAMP,
    data_quality_status VARCHAR(50),

    CONSTRAINT chk_sellers_main_platform
        CHECK (main_platform IN ('tiktok', 'instagram', 'facebook_live', 'youtube_live', 'other') OR main_platform IS NULL),

    CONSTRAINT chk_sellers_status
        CHECK (seller_status IN ('active', 'inactive', 'suspended') OR seller_status IS NULL)
);

COMMENT ON TABLE core.sellers IS
'Cleaned sellers table. Contains fictitious seller and shop information.';


CREATE TABLE IF NOT EXISTS core.customers (
    customer_id TEXT PRIMARY KEY,
    username TEXT,
    platform VARCHAR(50),
    email TEXT,
    country VARCHAR(100),
    created_at TIMESTAMP,
    cleaned_at TIMESTAMP,
    data_quality_status VARCHAR(50),

    CONSTRAINT chk_customers_platform
        CHECK (platform IN ('tiktok', 'instagram', 'facebook_live', 'youtube_live', 'other') OR platform IS NULL)
);

COMMENT ON TABLE core.customers IS
'Cleaned customers table. Contains fictitious or pseudonymized customer information.';


CREATE TABLE IF NOT EXISTS core.products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    brand TEXT,
    description TEXT,
    unit_price NUMERIC(12, 2),
    stock_quantity INTEGER,
    product_status VARCHAR(50),
    source VARCHAR(100),
    created_at TIMESTAMP,
    cleaned_at TIMESTAMP,
    data_quality_status VARCHAR(50),

    CONSTRAINT chk_products_unit_price
        CHECK (unit_price >= 0 OR unit_price IS NULL),

    CONSTRAINT chk_products_stock_quantity
        CHECK (stock_quantity >= 0 OR stock_quantity IS NULL),

    CONSTRAINT chk_products_status
        CHECK (product_status IN ('active', 'inactive', 'out_of_stock') OR product_status IS NULL)
);

COMMENT ON TABLE core.products IS
'Cleaned products table. Contains simulated, API and scraped products in a common schema.';


CREATE TABLE IF NOT EXISTS core.live_sessions (
    live_id TEXT PRIMARY KEY,
    seller_id TEXT NOT NULL,
    platform VARCHAR(50),
    live_title TEXT,
    scheduled_start_at TIMESTAMP,
    actual_start_at TIMESTAMP,
    ended_at TIMESTAMP,
    live_status VARCHAR(50),
    peak_viewers INTEGER,
    currency VARCHAR(10),
    created_at TIMESTAMP,
    cleaned_at TIMESTAMP,
    data_quality_status VARCHAR(50),

    CONSTRAINT fk_live_sessions_seller
        FOREIGN KEY (seller_id)
        REFERENCES core.sellers (seller_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_live_sessions_platform
        CHECK (platform IN ('tiktok', 'instagram', 'facebook_live', 'youtube_live', 'other') OR platform IS NULL),

    CONSTRAINT chk_live_sessions_status
        CHECK (live_status IN ('scheduled', 'live', 'ended', 'cancelled') OR live_status IS NULL),

    CONSTRAINT chk_live_sessions_peak_viewers
        CHECK (peak_viewers >= 0 OR peak_viewers IS NULL),

    CONSTRAINT chk_live_sessions_currency
        CHECK (currency IN ('EUR', 'USD', 'GBP', 'CAD', 'CHF') OR currency IS NULL)
);

COMMENT ON TABLE core.live_sessions IS
'Cleaned live sessions table. One row represents one sales live session.';


CREATE TABLE IF NOT EXISTS core.live_products (
    live_product_id TEXT PRIMARY KEY,
    live_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    display_order INTEGER,
    special_live_price NUMERIC(12, 2),
    initial_stock INTEGER,
    remaining_stock INTEGER,
    cleaned_at TIMESTAMP,
    data_quality_status VARCHAR(50),

    CONSTRAINT fk_live_products_live
        FOREIGN KEY (live_id)
        REFERENCES core.live_sessions (live_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_live_products_product
        FOREIGN KEY (product_id)
        REFERENCES core.products (product_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_live_products_display_order
        CHECK (display_order >= 0 OR display_order IS NULL),

    CONSTRAINT chk_live_products_special_price
        CHECK (special_live_price >= 0 OR special_live_price IS NULL),

    CONSTRAINT chk_live_products_initial_stock
        CHECK (initial_stock >= 0 OR initial_stock IS NULL),

    CONSTRAINT chk_live_products_remaining_stock
        CHECK (remaining_stock >= 0 OR remaining_stock IS NULL)
);

COMMENT ON TABLE core.live_products IS
'Association table between live sessions and products presented during lives.';


CREATE TABLE IF NOT EXISTS core.live_comments (
    comment_id TEXT PRIMARY KEY,
    live_id TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    platform VARCHAR(50),
    username TEXT,
    comment_text TEXT,
    commented_at TIMESTAMP,
    comment_language VARCHAR(20),
    manual_intent_label VARCHAR(100),
    extracted_product_keyword TEXT,
    cleaned_at TIMESTAMP,
    data_quality_status VARCHAR(50),

    CONSTRAINT fk_live_comments_live
        FOREIGN KEY (live_id)
        REFERENCES core.live_sessions (live_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_live_comments_customer
        FOREIGN KEY (customer_id)
        REFERENCES core.customers (customer_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_live_comments_platform
        CHECK (platform IN ('tiktok', 'instagram', 'facebook_live', 'youtube_live', 'other') OR platform IS NULL),

    CONSTRAINT chk_live_comments_intent
        CHECK (
            manual_intent_label IN (
                'purchase_intent',
                'product_question',
                'payment_question',
                'shipping_question',
                'other',
                'unknown'
            )
            OR manual_intent_label IS NULL
        )
);

COMMENT ON TABLE core.live_comments IS
'Cleaned live comments table used later for purchase intent analysis.';


CREATE TABLE IF NOT EXISTS core.carts (
    cart_id TEXT PRIMARY KEY,
    live_id TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    cart_status VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    total_amount NUMERIC(12, 2),
    currency VARCHAR(10),
    cleaned_at TIMESTAMP,
    data_quality_status VARCHAR(50),

    CONSTRAINT fk_carts_live
        FOREIGN KEY (live_id)
        REFERENCES core.live_sessions (live_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_carts_customer
        FOREIGN KEY (customer_id)
        REFERENCES core.customers (customer_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_carts_status
        CHECK (cart_status IN ('open', 'paid', 'abandoned', 'cancelled') OR cart_status IS NULL),

    CONSTRAINT chk_carts_total_amount
        CHECK (total_amount >= 0 OR total_amount IS NULL),

    CONSTRAINT chk_carts_currency
        CHECK (currency IN ('EUR', 'USD', 'GBP', 'CAD', 'CHF') OR currency IS NULL)
);

COMMENT ON TABLE core.carts IS
'Cleaned carts table. A cart is linked to a live session and a customer.';


CREATE TABLE IF NOT EXISTS core.cart_items (
    cart_item_id TEXT PRIMARY KEY,
    cart_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER,
    unit_price NUMERIC(12, 2),
    line_total NUMERIC(12, 2),
    selected_size VARCHAR(50),
    selected_color VARCHAR(100),
    cleaned_at TIMESTAMP,
    data_quality_status VARCHAR(50),

    CONSTRAINT fk_cart_items_cart
        FOREIGN KEY (cart_id)
        REFERENCES core.carts (cart_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_cart_items_product
        FOREIGN KEY (product_id)
        REFERENCES core.products (product_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_cart_items_quantity
        CHECK (quantity >= 1 OR quantity IS NULL),

    CONSTRAINT chk_cart_items_unit_price
        CHECK (unit_price >= 0 OR unit_price IS NULL),

    CONSTRAINT chk_cart_items_line_total
        CHECK (line_total >= 0 OR line_total IS NULL)
);

COMMENT ON TABLE core.cart_items IS
'Cleaned cart items table. Contains products added to carts.';


CREATE TABLE IF NOT EXISTS core.orders (
    order_id TEXT PRIMARY KEY,
    cart_id TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    seller_id TEXT NOT NULL,
    order_status VARCHAR(50),
    order_amount NUMERIC(12, 2),
    currency VARCHAR(10),
    created_at TIMESTAMP,
    confirmed_at TIMESTAMP,
    cleaned_at TIMESTAMP,
    data_quality_status VARCHAR(50),

    CONSTRAINT fk_orders_cart
        FOREIGN KEY (cart_id)
        REFERENCES core.carts (cart_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES core.customers (customer_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_orders_seller
        FOREIGN KEY (seller_id)
        REFERENCES core.sellers (seller_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_orders_status
        CHECK (order_status IN ('pending', 'confirmed', 'paid', 'cancelled', 'refunded') OR order_status IS NULL),

    CONSTRAINT chk_orders_amount
        CHECK (order_amount >= 0 OR order_amount IS NULL),

    CONSTRAINT chk_orders_currency
        CHECK (currency IN ('EUR', 'USD', 'GBP', 'CAD', 'CHF') OR currency IS NULL)
);

COMMENT ON TABLE core.orders IS
'Cleaned orders table. Orders are created from carts.';


CREATE TABLE IF NOT EXISTS core.payments (
    payment_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    payment_provider VARCHAR(100),
    payment_status VARCHAR(50),
    payment_amount NUMERIC(12, 2),
    currency VARCHAR(10),
    payment_method VARCHAR(100),
    paid_at TIMESTAMP,
    transaction_reference TEXT,
    cleaned_at TIMESTAMP,
    data_quality_status VARCHAR(50),

    CONSTRAINT fk_payments_order
        FOREIGN KEY (order_id)
        REFERENCES core.orders (order_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT chk_payments_status
        CHECK (payment_status IN ('pending', 'succeeded', 'failed', 'cancelled', 'refunded') OR payment_status IS NULL),

    CONSTRAINT chk_payments_amount
        CHECK (payment_amount >= 0 OR payment_amount IS NULL),

    CONSTRAINT chk_payments_currency
        CHECK (currency IN ('EUR', 'USD', 'GBP', 'CAD', 'CHF') OR currency IS NULL)
);

COMMENT ON TABLE core.payments IS
'Cleaned payments table. No real banking data is stored.';


CREATE TABLE IF NOT EXISTS core.stock_movements (
    stock_movement_id TEXT PRIMARY KEY,
    product_id TEXT NOT NULL,
    live_id TEXT NOT NULL,
    movement_type VARCHAR(100),
    quantity_change INTEGER,
    movement_reason TEXT,
    created_at TIMESTAMP,
    cleaned_at TIMESTAMP,
    data_quality_status VARCHAR(50),

    CONSTRAINT fk_stock_movements_product
        FOREIGN KEY (product_id)
        REFERENCES core.products (product_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_stock_movements_live
        FOREIGN KEY (live_id)
        REFERENCES core.live_sessions (live_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

COMMENT ON TABLE core.stock_movements IS
'Cleaned stock movements table. Quantity changes may be positive or negative.';


CREATE TABLE IF NOT EXISTS core.live_events (
    event_id TEXT PRIMARY KEY,
    live_id TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    event_type VARCHAR(100),
    event_timestamp TIMESTAMP,
    event_value TEXT,
    source_system VARCHAR(100),
    cleaned_at TIMESTAMP,
    data_quality_status VARCHAR(50),

    CONSTRAINT fk_live_events_live
        FOREIGN KEY (live_id)
        REFERENCES core.live_sessions (live_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_live_events_customer
        FOREIGN KEY (customer_id)
        REFERENCES core.customers (customer_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_live_events_type
        CHECK (
            event_type IN (
                'comment_sent',
                'cart_opened',
                'payment_clicked',
                'payment_succeeded',
                'api_error',
                'product_viewed'
            )
            OR event_type IS NULL
        )
);

COMMENT ON TABLE core.live_events IS
'Cleaned live events table. Contains behavioral and technical events from the simulated Big Data source.';


-- -------------------------------------------------------------------
-- ANALYTICS SCHEMA
-- -------------------------------------------------------------------


CREATE TABLE IF NOT EXISTS analytics.dataset_final_live_sales (
    live_id TEXT PRIMARY KEY,
    seller_id TEXT NOT NULL,
    shop_name TEXT,
    seller_country VARCHAR(100),
    main_platform VARCHAR(50),
    seller_status VARCHAR(50),
    platform VARCHAR(50),
    live_title TEXT,
    live_status VARCHAR(50),
    live_date DATE,
    peak_viewers INTEGER,
    currency VARCHAR(10),

    total_comments INTEGER,
    purchase_intent_comments INTEGER,
    product_question_comments INTEGER,
    payment_question_comments INTEGER,
    shipping_question_comments INTEGER,
    other_comments INTEGER,
    unknown_intent_comments INTEGER,
    unique_comment_customers INTEGER,
    purchase_intent_rate NUMERIC(10, 4),

    total_carts INTEGER,
    paid_carts INTEGER,
    abandoned_carts INTEGER,
    open_carts INTEGER,
    cancelled_carts INTEGER,
    unique_cart_customers INTEGER,
    cart_abandonment_rate NUMERIC(10, 4),
    comment_to_cart_rate NUMERIC(10, 4),

    total_orders INTEGER,
    paid_orders INTEGER,
    confirmed_orders INTEGER,
    pending_orders INTEGER,
    cancelled_orders INTEGER,
    refunded_orders INTEGER,
    total_order_amount NUMERIC(12, 2),
    average_order_amount NUMERIC(12, 2),

    total_payments INTEGER,
    successful_payments INTEGER,
    failed_payments INTEGER,
    pending_payments INTEGER,
    cancelled_payments INTEGER,
    refunded_payments INTEGER,
    total_revenue NUMERIC(12, 2),
    payment_success_rate NUMERIC(10, 4),

    conversion_rate NUMERIC(10, 4),
    revenue_per_viewer NUMERIC(12, 4),
    revenue_per_order NUMERIC(12, 4),

    total_products_presented INTEGER,
    total_initial_stock NUMERIC(12, 2),
    total_remaining_stock NUMERIC(12, 2),
    estimated_sold_quantity NUMERIC(12, 2),
    average_live_product_price NUMERIC(12, 2),
    top_product_category TEXT,

    total_events INTEGER,
    comment_event_count INTEGER,
    cart_opened_events INTEGER,
    payment_clicked_events INTEGER,
    payment_succeeded_events INTEGER,
    api_error_events INTEGER,
    product_view_events INTEGER,
    unique_event_customers INTEGER,

    final_dataset_created_at TIMESTAMP,
    final_dataset_status VARCHAR(50),

    CONSTRAINT fk_dataset_final_live
        FOREIGN KEY (live_id)
        REFERENCES core.live_sessions (live_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_dataset_final_seller
        FOREIGN KEY (seller_id)
        REFERENCES core.sellers (seller_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_dataset_platform
        CHECK (platform IN ('tiktok', 'instagram', 'facebook_live', 'youtube_live', 'other') OR platform IS NULL),

    CONSTRAINT chk_dataset_main_platform
        CHECK (main_platform IN ('tiktok', 'instagram', 'facebook_live', 'youtube_live', 'other') OR main_platform IS NULL),

    CONSTRAINT chk_dataset_seller_status
        CHECK (seller_status IN ('active', 'inactive', 'suspended') OR seller_status IS NULL),

    CONSTRAINT chk_dataset_live_status
        CHECK (live_status IN ('scheduled', 'live', 'ended', 'cancelled') OR live_status IS NULL),

    CONSTRAINT chk_dataset_currency
        CHECK (currency IN ('EUR', 'USD', 'GBP', 'CAD', 'CHF') OR currency IS NULL),

    CONSTRAINT chk_dataset_non_negative_counts
        CHECK (
            COALESCE(peak_viewers, 0) >= 0
            AND COALESCE(total_comments, 0) >= 0
            AND COALESCE(total_carts, 0) >= 0
            AND COALESCE(total_orders, 0) >= 0
            AND COALESCE(total_payments, 0) >= 0
            AND COALESCE(total_events, 0) >= 0
        ),

    CONSTRAINT chk_dataset_non_negative_amounts
        CHECK (
            COALESCE(total_order_amount, 0) >= 0
            AND COALESCE(average_order_amount, 0) >= 0
            AND COALESCE(total_revenue, 0) >= 0
            AND COALESCE(revenue_per_viewer, 0) >= 0
            AND COALESCE(revenue_per_order, 0) >= 0
        ),

    CONSTRAINT chk_dataset_status
        CHECK (final_dataset_status IN ('ready_for_ai') OR final_dataset_status IS NULL)
);

COMMENT ON TABLE analytics.dataset_final_live_sales IS
'Final AI-ready analytical dataset. One row represents one live session.';


-- -------------------------------------------------------------------
-- AUDIT SCHEMA
-- -------------------------------------------------------------------


CREATE TABLE IF NOT EXISTS audit.import_batches (
    import_batch_id TEXT PRIMARY KEY,
    started_at TIMESTAMP NOT NULL,
    ended_at TIMESTAMP,
    status VARCHAR(50) NOT NULL,
    source_folder TEXT,
    total_tables INTEGER,
    total_rows_read INTEGER,
    total_rows_inserted INTEGER,
    error_message TEXT,

    CONSTRAINT chk_import_batches_status
        CHECK (status IN ('started', 'success', 'partial_success', 'failed'))
);

COMMENT ON TABLE audit.import_batches IS
'Technical table used to track global CSV import batches.';


CREATE TABLE IF NOT EXISTS audit.import_logs (
    import_log_id BIGSERIAL PRIMARY KEY,
    import_batch_id TEXT NOT NULL,
    schema_name VARCHAR(100) NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    source_file TEXT NOT NULL,
    rows_read INTEGER,
    rows_inserted INTEGER,
    status VARCHAR(50) NOT NULL,
    error_message TEXT,
    imported_at TIMESTAMP NOT NULL,

    CONSTRAINT fk_import_logs_batch
        FOREIGN KEY (import_batch_id)
        REFERENCES audit.import_batches (import_batch_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT chk_import_logs_status
        CHECK (status IN ('success', 'failed', 'skipped'))
);

COMMENT ON TABLE audit.import_logs IS
'Technical table used to track one import log per imported source file.';
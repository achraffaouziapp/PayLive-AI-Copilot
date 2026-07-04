-- -------------------------------------------------------------------
-- Schema creation script
-- Project: PayLive AI Copilot
-- Database: paylive_ai_copilot
--
-- This script creates the PostgreSQL schemas used by the project:
-- - core: cleaned business data;
-- - analytics: final aggregated AI dataset;
-- - audit: technical import logs.
--
-- Execution context:
-- This script must be executed on the paylive_ai_copilot database.
--
-- Docker execution example:
-- docker cp sql/02_create_schemas.sql paylive_postgres:/tmp/02_create_schemas.sql
-- docker exec -it paylive_postgres psql -U postgres -d paylive_ai_copilot -f /tmp/02_create_schemas.sql
-- -------------------------------------------------------------------


CREATE SCHEMA IF NOT EXISTS core;

COMMENT ON SCHEMA core IS
'Business schema containing cleaned PayLive AI Copilot datasets.';


CREATE SCHEMA IF NOT EXISTS analytics;

COMMENT ON SCHEMA analytics IS
'Analytics schema containing the final aggregated AI-ready dataset.';


CREATE SCHEMA IF NOT EXISTS audit;

COMMENT ON SCHEMA audit IS
'Audit schema containing technical import batches and import logs.';
-- -------------------------------------------------------------------
-- Database creation script
-- Project: PayLive AI Copilot
-- Database: paylive_ai_copilot
--
-- This script creates the final PostgreSQL database used to store:
-- - cleaned business datasets;
-- - the final aggregated AI dataset;
-- - import audit logs.
--
-- Execution context:
-- This script must be executed from the default PostgreSQL database:
-- postgres.
--
-- Docker execution example:
-- docker cp sql/01_create_database.sql paylive_postgres:/tmp/01_create_database.sql
-- docker exec -it paylive_postgres psql -U postgres -d postgres -f /tmp/01_create_database.sql
-- -------------------------------------------------------------------


SELECT
    'CREATE DATABASE paylive_ai_copilot
        WITH
        OWNER = postgres
        ENCODING = ''UTF8''
        CONNECTION LIMIT = -1;'
WHERE NOT EXISTS (
    SELECT 1
    FROM pg_database
    WHERE datname = 'paylive_ai_copilot'
)
\gexec


COMMENT ON DATABASE paylive_ai_copilot IS
'Final PostgreSQL database for the PayLive AI Copilot project. It stores cleaned business data, the final aggregated AI dataset and technical import audit information.';
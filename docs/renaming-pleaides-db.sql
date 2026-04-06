SELECT 
FROM pg_stat_activity
;

-- Disconnect all current connections to the pleiades DB
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'pleiades';

ALTER DATABASE pleiades RENAME TO pleiades_prod;
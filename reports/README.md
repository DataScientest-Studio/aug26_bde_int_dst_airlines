# Project reports

These documents describe the implemented data-engineering layer of the airport
area air-traffic project. 

Read them in this order:

1. [API evaluation and source selection](report.MD)  
   Evaluation of AF/KLM, Aviationstack, and other sources; explains why OpenSky
   and OpenWeather were selected.
2. [Dashboard data-product description](dashboard_description.md)  
   Defines the dashboard scope, available observations, identifiers, and
   source-driven limitations.
3. [Collectors and operational logging](collectors_and_logging.md)  
   Documents API collection, raw JSON storage, error handling, logging, and
   scheduled execution.
4. [Database documentation](database_documentation.MD)  
   Describes schemas, tables, lineage, constraints, indexes, and migrations.
5. [Ingestion and normalisation pipeline](ingestion_normalisation.md)  
   Describes raw-snapshot registration, normalisation, transactions, batching,
   idempotency, and recovery.
6. [Lessons learned](lessons_learned.md)  
   Summarises operational and design lessons from implementing and running the
   pipeline.

The SQL files in 'src/databases/' are the executable source of truth for the
database schema; the database report explains their intent.

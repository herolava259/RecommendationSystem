

## Star Schema 
- is a schema design in data warehouse
- Include:
  - Fact Table, (info): in the middle
  - Dimension Tables (dim/description): in around
- roles:
  - speed up query
  - optimize join
  - reduce data model complexity

## Catalog
- Where to save metadata of entire data
- catalog in dwh include:
    - table info: schema, description, name
    - column info: type, business sense, constraint, default value ( like declare of colum in SQL ->DDL)
    - lineage: source of table, flow: raw-> staging -> dim/fact
    - owner & steward: who responsible?, which team for maintenance?
    - version/ scheme evolution: what have columns recently added/drop/change-scheme? 
- Catalog in DWH vs Catalog in Data-Lake -> Diff:
  - In Warehouse(Snowflake/Redshift/BigQuery): internal metadata of the system. organizing:>> +schema, +table, +view, +procedures
  - In Data-Lake (Iceberg/Delta/Hudi): Catalog is not a built-in thing — it is a required component to manage files in object storage (S3, MinIO, HDFS).
- Benefit:
  - Standard Schema
  - Ease to access, query
  - Ease control lifecycle of data: data lineage, versioning, retention, audit logs
## 3NF Normalization
- 1-NF:
  - Atomic Column
  - No duplicate rows
  - has unique key
  - order of store data does not matter
- 2-NF:
  - 1-NF
  - No partial dependency exists, meaning every non-primary attribute must depend on the entire primary key

- 3-NF:
    - 2-NF
    - No transitive dependencies

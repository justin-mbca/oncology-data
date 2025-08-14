## Architecture Diagram

```mermaid
flowchart TD
	subgraph Ingestion
		FHIR[FHIR Server]
		VCF[VCF File]
	end
	subgraph API
		FastAPI[FastAPI App]
	end
	subgraph Processing
		Norm[Normalization (dbt, Great Expectations)]
		Genomics[Genomics Parsing & Annotation]
		QC[Data Quality Checks]
		HITL[HITL Approval]
	end
	subgraph Storage
		S3[S3/Local Storage]
		DBT[dbt Gold Tables]
		SQLite[HITL DB]
	end

	FHIR -->|/run/daily| FastAPI
	VCF -->|VCF Parse| FastAPI
	FastAPI --> Norm
	FastAPI --> Genomics
	FastAPI --> QC
	Norm --> DBT
	Genomics --> DBT
	QC --> DBT
	FastAPI --> HITL
	HITL --> SQLite
	FastAPI --> S3
	S3 --> Genomics
```
## Sample API Requests & Responses

### /run/daily (POST)
**Request:**
```json
{
	"fhir_url": "https://hapi.fhir.org/baseR4"
}
```
**Response (snippet):**
```json
{
	"ok": true,
	"data": {
		"observations": {"pointers": [...]},
		"genomics": {"n_annotated": 10},
		"qc": {"suite": "onc_silver", "stats": {"row_count": 12345}},
		...
	}
}
```

### /hitl/{task_id} (POST)
**Request:**
```json
{
	"approve": true
}
```
**Response:**
```json
{
	"task_id": "export-test",
	"status": "APPROVED"
}
```

## Role-Based Access Example

Endpoints require specific roles:
- `/run/daily`: requires `etl_runner`
- `/hitl/{task_id}`: requires `analyst`

Roles are stubbed in the code but can be integrated with OIDC or other auth providers.

## Human-in-the-Loop (HITL) Example

When the pipeline reaches a sensitive operation (e.g., data export), a HITL task is created:
```json
{
	"task_id": "export-test",
	"status": "PENDING"
}
```
An analyst can then approve or reject the task via `/hitl/{task_id}`.

## Data Quality/Validation Example

The pipeline runs Great Expectations checks. Example output:
```json
{
	"qc": {
		"suite": "onc_silver",
		"table": "silver.observation",
		"stats": {"row_count": 12345}
	}
}
```

## dbt/SQL Transformation Example

The project includes dbt models for transforming and aggregating data. Example (from `models/gold/variants.sql`):
```sql
select * from base
```
See the `transforms/dbt_project/models/` directory for more.

## Extending the Pipeline

- Add new endpoints in `api/app.py`
- Add new tools in the `tools/` directory
- Add new dbt models in `transforms/dbt_project/models/`
- Update settings in `common/settings.py`
## API Endpoints

- `GET /` — Health check, returns API status
- `POST /run/daily` — Run the daily pipeline (requires `fhir_url` in body)
- `POST /hitl/{task_id}` — Human-in-the-loop approval for a task

See [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for full interactive API documentation.

## Configuration

Key environment variables and settings (see `common/settings.py`):

- `FHIR_BASE_URL`: Default FHIR server URL (can be overridden per request)
- `S3_BUCKET`, `S3_ENDPOINT`: S3 storage settings (if used)
- `DBT_PROJECT_DIR`: Path to dbt project
- `DELTA_ROOT`: Local or S3 path for data
- `HITL_DB`: SQLite file for HITL queue

You can set these in a `.env` file or as environment variables.

## Troubleshooting

- **VCF parsing returns null:**
	- Ensure your VCF file is tab-delimited and in the correct location (`data/genomics_drop_test.vcf`).
	- Check server logs for errors.
- **FHIR errors:**
	- Make sure you use a valid FHIR URL (e.g., `https://hapi.fhir.org/baseR4`).
- **Dependency issues:**
	- Run `pip install -r requirements.txt` to install all dependencies.

## Contact

For questions or collaboration, contact [justin-mbca on GitHub](https://github.com/justin-mbca).
## Usage Examples

### Run the API server
```bash
python -m uvicorn api.app:app --reload
```

### Try the API
- Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive docs
- Example: Run the daily pipeline with a public FHIR server
	```bash
	curl -X POST "http://127.0.0.1:8000/run/daily" \
		-H "accept: application/json" \
		-H "Content-Type: application/json" \
		-d '{"fhir_url": "https://hapi.fhir.org/baseR4"}'
	```

### Genomics Support Example
The pipeline includes genomics processing steps such as VCF parsing and variant annotation. For demonstration, the `/run/daily` endpoint simulates:
- Discovering VCF files (e.g., from S3 or local storage)
- Parsing a VCF file and extracting variants
- Annotating variants (e.g., with gene, consequence, clinical significance)

You can see the genomics results in the `genomics` field of the `/run/daily` response. Example snippet:
```json
"genomics": {
	"n_annotated": 10
}
```
This means 10 variants were parsed and annotated in the demo pipeline. In a real deployment, you would connect to actual VCF files and annotation services.

# Oncology Data Pipeline

A FastAPI-based platform for ingesting, normalizing, and analyzing clinical and genomics data using FHIR, dbt, and modern data engineering tools.

## Features
- **FHIR Integration:** Ingests clinical data from FHIR servers (public or private)
- **Genomics Support:** Handles VCF parsing, annotation, and variant modeling
- **Data Normalization:** Uses dbt and Great Expectations for data quality and transformation
- **Role-Based Access Control:** Simple RBAC for ETL and analyst endpoints
- **HITL (Human-in-the-Loop):** Approval workflow for sensitive operations
- **Cloud & Local Ready:** Works with S3, Databricks, and local environments

## Tech Stack
- Python 3.10+
- FastAPI
- dbt
- Great Expectations
- Pydantic & pydantic-settings
- Docker (for FHIR server testing)

## Example Use Cases
- Clinical data ingestion and normalization for oncology research
- Genomic variant annotation and gold table creation
- Data quality validation and audit


## Installation
1. **Clone the repo:**
	```bash
	git clone https://github.com/justin-mbca/oncology-data.git
	cd oncology-data
	```
2. **(Recommended) Create a virtual environment:**
	```bash
	python3 -m venv venv
	source venv/bin/activate
	```
3. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```

## Usage Examples

### Run the API server
```bash
python -m uvicorn api.app:app --reload
```

### Try the API
- Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive docs
- Example: Run the daily pipeline with a public FHIR server
  ```bash
  curl -X POST "http://127.0.0.1:8000/run/daily" \
	 -H "accept: application/json" \
	 -H "Content-Type: application/json" \
	 -d '{"fhir_url": "https://hapi.fhir.org/baseR4"}'
  ```


## Example Resume Description
> Developed a modular FastAPI-based data pipeline for oncology research, integrating FHIR clinical data, genomics variant processing, and dbt-based normalization. Implemented data quality checks, role-based access, and HITL approval workflows. Designed for both cloud and local environments.

## License
MIT

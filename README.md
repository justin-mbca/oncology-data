
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

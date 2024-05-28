from fastapi import FastAPI, HTTPException, UploadFile

from src.logic import (CompanyDataUnavailable,
                       extract_and_compare_company_data_against_db)
from src.models import DataComparison

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/extract-and-compare", summary="Extract and company data")
def compare_with_existing_company_data(
    company_name: str, pdf_file: UploadFile
) -> list[DataComparison]:
    """
    Extract company data from PDF and compare with database values

    Steps done:
    1. Extracts data from PDF using an external service
    2. Fetches company data from the database for the given company
    3. Compares the data and returns the summary
    """
    filename = pdf_file.filename
    try:
        comparison = extract_and_compare_company_data_against_db(filename, company_name)
    except FileNotFoundError:
        raise HTTPException(400, f"Could not extract data from PDF file '{filename}'")
    except CompanyDataUnavailable:
        raise HTTPException(
            404, f"Data for company '{company_name}' does not exist in database"
        )
    return comparison

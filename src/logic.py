from src.database import fetch_company_data_summary_from_db
from src.pdf_service import PdfService


class CompanyDataUnavailable(Exception):
    pass


def extract_and_compare_company_data_against_db(
    filename: str, company_name: str
) -> list[dict]:
    # Extract data from PDF
    pdf_service = PdfService(key="TEST_KEY")
    filename = filename
    extracted_data = pdf_service.extract(file_path=filename)

    # Fetch existing data from the database
    existing_company_data = fetch_company_data_summary_from_db(company_name)
    if existing_company_data is None:
        raise CompanyDataUnavailable(
            f"Could not find company data for '{company_name}' in the database"
        )

    # Compare data
    comparison = compare_two_versions_of_data(existing_company_data, extracted_data)

    return comparison


def compare_two_versions_of_data(data1: dict, data2: dict) -> list[dict]:
    """
    Compares the values in two dictionaries, allowing for the fact that some keys may only be present in one of the dictionaries
    """
    all_keys = data1.keys() | data2.keys()
    comparisons = []
    for key in sorted(all_keys):
        data1_value = data1.get(key)
        if data1_value is not None:
            data1_value = str(data1_value)

        data2_value = data2.get(key)
        if data2_value is not None:
            data2_value = str(data2_value)

        if data1_value is not None and data2_value is not None:
            action = "no change" if data1_value == data2_value else "updated"
        elif data1_value is not None and data2_value is None:
            action = "deleted"
        elif data1_value is None and data2_value is not None:
            action = "added"
        comparisons.append(
            {
                "key": key,
                "action": action,
                "old_value": data1_value,
                "new_value": data2_value,
            }
        )
    return comparisons

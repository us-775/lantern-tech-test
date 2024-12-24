import csv
from typing import Optional


def fetch_company_data_summary_from_db(company_name: str) -> Optional[dict]:
    with open("data/database.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Company Name"] == company_name:
                return row

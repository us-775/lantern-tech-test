import unittest
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from src.main import app
from tests import TESTDATA_DIR

client = TestClient(app)


class TestAPI(unittest.TestCase):
    PDF_SERVICE_MOCK_DATA = {
        "Company Name": "RetailCo",
        "Industry": "Retail",
        "Market Capitalization": 2000,
        "Revenue (in millions)": 800,
        "EBITDA (in millions)": 150,
        "Net Income (in millions)": 40,
        "Debt (in millions)": 110,
        "Equity (in millions)": 400,
        "Enterprise Value (in millions)": 2100,
        "P/E Ratio": 20,
        "Revenue Growth Rate (%)": 8,
        "EBITDA Margin (%)": 18.75,
        "ROE (Return on Equity) (%)": 10,
        "ROA (Return on Assets) (%)": 6.5,
        "Current Ratio": 1.8,
        "Debt to Equity Ratio": 0.25,
        "Location": "Chicago, IL",
        "CEO": "Bob Johnson",
        "Number of Employees": 2000,
    }
    DEFAULT_HEADERS = {"X-API-Key": "abc123"}

    @patch("src.logic.PdfService")
    def test_valid_file(self, mock_pdf_service):
        pdf_service_mock = Mock(extract=Mock(return_value=self.PDF_SERVICE_MOCK_DATA))
        mock_pdf_service.return_value = pdf_service_mock

        filepath = TESTDATA_DIR / "retailco.pdf"
        with open(filepath, "rb") as f:
            files = {"pdf_file": f}
            response = client.post(
                "/extract-and-compare",
                params={"company_name": "RetailCo"},
                files=files,
                headers=self.DEFAULT_HEADERS,
            )

        assert response.status_code == 200, response.status_code
        expected_response = [
            {
                "field": "CEO",
                "action": "added",
                "old_value": None,
                "new_value": "Bob Johnson",
            },
            {
                "field": "Company Name",
                "action": "no change",
                "old_value": "RetailCo",
                "new_value": "RetailCo",
            },
            {
                "field": "Current Ratio",
                "action": "no change",
                "old_value": "1.8",
                "new_value": "1.8",
            },
            {
                "field": "Debt (in millions)",
                "action": "updated",
                "old_value": "100",
                "new_value": "110",
            },
            {
                "field": "Debt to Equity Ratio",
                "action": "no change",
                "old_value": "0.25",
                "new_value": "0.25",
            },
            {
                "field": "EBITDA (in millions)",
                "action": "no change",
                "old_value": "150",
                "new_value": "150",
            },
            {
                "field": "EBITDA Margin (%)",
                "action": "no change",
                "old_value": "18.75",
                "new_value": "18.75",
            },
            {
                "field": "Enterprise Value (in millions)",
                "action": "no change",
                "old_value": "2100",
                "new_value": "2100",
            },
            {
                "field": "Equity (in millions)",
                "action": "no change",
                "old_value": "400",
                "new_value": "400",
            },
            {
                "field": "Industry",
                "action": "no change",
                "old_value": "Retail",
                "new_value": "Retail",
            },
            {
                "field": "Location",
                "action": "updated",
                "old_value": "Chicago",
                "new_value": "Chicago, IL",
            },
            {
                "field": "Market Capitalization",
                "action": "no change",
                "old_value": "2000",
                "new_value": "2000",
            },
            {
                "field": "Net Income (in millions)",
                "action": "no change",
                "old_value": "40",
                "new_value": "40",
            },
            {
                "field": "Net Income Margin (%)",
                "action": "deleted",
                "old_value": "5",
                "new_value": None,
            },
            {
                "field": "Number of Employees",
                "action": "added",
                "old_value": None,
                "new_value": "2000",
            },
            {
                "field": "P/E Ratio",
                "action": "no change",
                "old_value": "20",
                "new_value": "20",
            },
            {
                "field": "ROA (Return on Assets) (%)",
                "action": "no change",
                "old_value": "6.5",
                "new_value": "6.5",
            },
            {
                "field": "ROE (Return on Equity) (%)",
                "action": "no change",
                "old_value": "10",
                "new_value": "10",
            },
            {
                "field": "Revenue (in millions)",
                "action": "no change",
                "old_value": "800",
                "new_value": "800",
            },
            {
                "field": "Revenue Growth Rate (%)",
                "action": "no change",
                "old_value": "8",
                "new_value": "8",
            },
        ]
        actual_response = response.json()
        assert actual_response == expected_response

    @patch("src.logic.PdfService")
    def test_file_that_cant_be_scraped_by_pdf_service(self, mock_pdf_service):
        pdf_service_mock = Mock(
            extract=Mock(
                side_effect=FileNotFoundError(
                    "Cannot extract data. Invalid file provided."
                )
            )
        )
        mock_pdf_service.return_value = pdf_service_mock

        filepath = TESTDATA_DIR / "file_that_cant_be_scraped.pdf"
        with open(filepath, "rb") as f:
            files = {"pdf_file": f}
            response = client.post(
                "/extract-and-compare",
                params={"company_name": "foobar"},
                files=files,
                headers=self.DEFAULT_HEADERS,
            )

        assert response.status_code == 400, response.status_code
        assert response.json() == {
            "detail": "Could not extract data from PDF file 'file_that_cant_be_scraped.pdf'"
        }

    @patch("src.logic.PdfService")
    def test_company_data_not_in_database(self, mock_pdf_service):
        pdf_service_mock = Mock(extract=Mock(return_value=self.PDF_SERVICE_MOCK_DATA))
        mock_pdf_service.return_value = pdf_service_mock
        filepath = TESTDATA_DIR / "retailco.pdf"
        with open(filepath, "rb") as f:
            files = {"pdf_file": f}
            response = client.post(
                "/extract-and-compare",
                params={"company_name": "Bad Company Name"},
                files=files,
                headers=self.DEFAULT_HEADERS,
            )

        assert response.status_code == 404, response.status_code
        assert response.json() == {
            "detail": "Data for company 'Bad Company Name' does not exist in database"
        }

    def test_no_api_key(self):
        filepath = TESTDATA_DIR / "retailco.pdf"
        with open(filepath, "rb") as f:
            files = {"pdf_file": f}
            response = client.post(
                "/extract-and-compare",
                params={"company_name": "Bad Company Name"},
                files=files,
            )

        assert response.status_code == 403, response.status_code

    def test_invalid_api_key(self):
        filepath = TESTDATA_DIR / "retailco.pdf"
        with open(filepath, "rb") as f:
            files = {"pdf_file": f}
            response = client.post(
                "/extract-and-compare",
                params={"company_name": "Bad Company Name"},
                files=files,
                headers={"X-API-Key": "bad-key"},
            )

        assert response.status_code == 401, response.status_code


if __name__ == "__main__":
    unittest.main()

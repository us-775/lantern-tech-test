# Data discrepancy checker

This task mirrors a system we recently built internally, and will give you an
idea of the problems we need to solve.

Every quarter, new company data is provided to us in PDF format. We need to use
an external service to extract this data from the PDF, and then validate it
against data we have on file from another source.

Complete the API so that:

A user can provide a PDF and a company name data is extracted from the PDF via
the external service and compared to the data stored on file a summary of the
data is returned, containing all fields from both sources, noting which fields
did not match.

A selection of example PDFs have been uploaded, and the PDF
extraction service has been mocked for use in `src/pdf_service.py` - DO NOT
EDIT THIS FILE. There is simple documentation of the service in
`PDF_SERVICE_DOCS.md`. You can treat this as just another microservice.

The existing data we have on file is available in the `data/database.csv` file.

Treat this code as if it will be deployed to production, following best
practices where possible.

## Setup using Poetry

The easiest way to set up the repository is to use `python-poetry`. The lock file
was generated using version `1.8.3`

1. Ensure `poetry` is installed
2. Run `make install`

## Setup without Poetry

Alternatively it's possible to `pip install` directly using the
`pyproject.toml` or `requirements.txt`.


## Usage
After starting the app by running `make dev`, navigate to http://localhost:8000/docs where you can use the new endpoint. Use 'abc123' as the API key in the header `X-API-Key`.

## Notes
* I changed pdf_service.py slightly to make the if conditions work with my endpoint code.
* Even though the pdf service has been mocked for simplicity, I decided to mock it in the tests anyway to treat it as an external service. Unit tests should not make real calls to external services so that's why mocking should be done.
* The PDF service is instantiated with a literal string passed for the key. A better way to do this would be to fetch the value from the environment variables to avoid hardcoding the key.

## Additional dependencies added
* I added ruff and isort for code formatting purposes.
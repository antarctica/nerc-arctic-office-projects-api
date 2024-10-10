import logging
from flask import request

from arctic_office_projects_api.logging import RequestFormatter


# def test_formatter_with_request_id(client, app):
#     # Create an instance of the formatter
#     formatter = RequestFormatter("%(url)s - %(request_id)s")

#     # Set up the request context
#     with app.test_request_context("/test"):
#         request.environ["HTTP_X_REQUEST_ID"] = "12345"

#         # Create a log record
#         record = logging.LogRecord(
#             "test", logging.INFO, "", 0, "Test message", None, None
#         )

#         # Format the record
#         formatted_message = formatter.format(record)

#         # Check the values
#         assert record.url == "/test"
#         assert record.request_id == "12345"
#         assert formatted_message == "/test - 12345"


def test_formatter_with_request_id(client, app):
    # Create an instance of the formatter
    formatter = RequestFormatter("%(url)s - %(request_id)s")

    # Set up the request context
    with app.test_request_context("/test"):
        request.environ["HTTP_X_REQUEST_ID"] = "12345"

        # Create a log record
        record = logging.LogRecord(
            "test", logging.INFO, "", 0, "Test message", None, None
        )

        # Format the record
        formatted_message = formatter.format(record)

        # Check the values
        assert record.url == "http://localhost/test"  # Adjusted to match full URL
        assert record.request_id == "12345"
        assert formatted_message == "http://localhost/test - 12345"


def test_formatter_no_request_context():
    # Create an instance of the formatter
    formatter = RequestFormatter("%(url)s - %(request_id)s")

    # Create a log record without a request context
    record = logging.LogRecord("test", logging.INFO, "", 0, "Test message", None, None)

    # Format the record
    formatted_message = formatter.format(record)

    # Check the values
    assert record.url == "NA"
    assert record.request_id == "NA"
    assert formatted_message == "NA - NA"

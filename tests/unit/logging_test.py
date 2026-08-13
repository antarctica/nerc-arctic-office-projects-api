import logging

from arctic_office_projects_api.utils import RequestFormatter


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

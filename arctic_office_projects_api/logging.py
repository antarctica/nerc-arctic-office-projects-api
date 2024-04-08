import logging

from flask import has_request_context, request, current_app as app


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = "NA"
        record.request_id = "NA"

        if has_request_context():
            record.url = request.url
            if app.config["APP_ENABLE_REQUEST_ID"]:
                record.request_id = request.environ.get("HTTP_X_REQUEST_ID")

        return super().format(record)

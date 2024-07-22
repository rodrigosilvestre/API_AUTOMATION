from behave import step, then, when

from QA.data.data_builder.data_string_parser import DataStringParser
from QA.data.data_validator.data_validation_class import DataValidation
from QA.request_class import Requests


# @when("I send a authenticated GET request to {URI}")
# def get_request(context, URI):
#     req = Requests()
#     req.get_request(context, URI)


@then("The status code is {status_code}")
def response_status_code(context, status_code):
    validate = DataValidation()
    validate.response_status_code(context, status_code)


@step("I have a new {data} from {URI}")
@step("I send a authenticated {request} request to {URI}")
@step("I send a authenticated {request} request to {URI} with {data}")
def authenticated_request(context, URI, data="base_data", request="POST"):
    data_parser = DataStringParser()
    parsed_data = data_parser.string_parser(data)
    req = Requests()
    req.data_selector(context, URI, request, parsed_data)
    req.authenticated_request(context, URI, request, data)


@then("The body will contain correct response for {data_validation}")
def check_event_response(context, data_validation=""):
    validate = DataValidation()
    validate.check_message_response(context, data_validation)

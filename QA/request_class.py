import re
import requests

from QA.data.data_builder.object_classes.register import Register
from QA.data.data_builder.object_classes.user import User


class Requests:
    def __init__(self):
        self.API_URL = "https://reqres.in"

    # def get_request(self, context, URI):
    #     # Simple GET request
    #     context.response = requests.get(self.API_URL + URI)

    def authenticated_request(self, context, URI, request, data):
        if request == "GET":
            context.response = requests.get(
                self.API_URL + self.format_URI(context, URI),
            )
        elif request == "POST":
            # print(f"\n data sent: {context.data}")
            context.response = requests.post(
                self.API_URL + URI,
                json=context.data
            )
            # print(f"\n data Recived: {context.response.text}")

            if int(context.response.status_code) in [200, 201, 204]:
                self.set_post_context_ids(context, data, URI)

    def format_URI(self, context, URI) -> None:
        COPY_URI = URI
        if re.search("{user_id}", URI):
            COPY_URI = COPY_URI.format(user_id=context.user_id)
        return COPY_URI


    def data_selector(self, context, URI, request, parsed_data):
        #
        # This function is used to select the data builder based on the URI
        #
        URI = URI.lower()
        if "users" in URI:
            generated_data = User(context).user_data_builder(context, request, URI, parsed_data)
        elif "register" in URI:
            generated_data = Register(context).register_data_builder(context, request, URI, parsed_data)

        else:
            raise ValueError(f"'{URI}' Not implemented on Data selector")

        context.data = generated_data

    def set_post_context_ids(self, context, data, URI):
        if data in [
            "optional_data",
            "base_data",
        ]:
            if "users" in URI:
                context.user_id = 2  # should be = context.response.json()["id"]

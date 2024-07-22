from QA.data.data_builder.base_object import BaseObject


class User(BaseObject):
    def __init__(self, context) -> None:
        self.user = {
            "name": {
                "type": "name",
                "min_length": 1,
                "max_length": 100,
                "required": True,
            },
            "job": {
                "type": "job",
                "min_length": 1,
                "max_length": 100,
                "required": False,
            }
        }

    def user_data_builder(self, context, request, URI, parsed_data):
        if request == "POST":
            self.object = self.generate_object(context, self.user, parsed_data)

        try:
            return self.object
        except AttributeError:
            return None

from QA.data.data_builder.base_object import BaseObject


class Register(BaseObject):
    def __init__(self, context) -> None:
        self.register = {
            "email": {
                "type": "alphaemails",
                "min_length": 1,
                "max_length": 100,
                "required": True,
            },
            "password": {
                "type": "password",
                "min_length": 10,
                "max_length": 100,
                "required": True,
            }
        }

    def register_data_builder(self, context, request, URI, parsed_data):
        if request == "POST":
            self.object = self.generate_object(context, self.register, parsed_data)

        try:
            return self.object
        except AttributeError:
            return None

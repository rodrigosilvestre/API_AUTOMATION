class BaseValidator:
    def validate(self, context, data, response):
        if "post" in data.lower():
            self.build_post_validator(context, data, response)
        elif "get" in data.lower():
            self.build_get_validator(context, data, response)
        else:
            raise ValueError("Invalid Request Type")
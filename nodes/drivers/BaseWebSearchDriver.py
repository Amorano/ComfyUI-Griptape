from griptape.drivers import BaseWebSearchDriver


class gtUIBaseWebSearchDriver:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {},
        }

    RETURN_TYPES = ("DRIVER",)
    RETURN_NAMES = ("DRIVER",)

    FUNCTION = "create"

    CATEGORY = "Griptape/Websearch Drivers"

    def create(
        self,
    ):
        driver = BaseWebSearchDriver()
        return (driver,)
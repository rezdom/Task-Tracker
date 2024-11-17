from datetime import datetime

class DateValidator:
    def __set_name__(self, owner, name):
            self.name = name
    def __set__(self, instance, value):
        if not isinstance(value, datetime):
            raise TypeError(
                 f"The object is of type [{type(value).__name__}], "
                "but a datetime object from the datetime module was expected."
            )
        instance.__dict__[self.name] = value
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)
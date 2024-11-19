from datetime import datetime

class TitleValidator:
    def __set_name__(self, owner, name):
        self.name = name
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(
                 f"The object is of type [{type(value).__name__}], "
                "but a [string] object was expected."
            )
        check = len(value)
        if check <= 4 or check > 64:
            raise ValueError(
                "The string of title must be between 4 and 64 chars long."
            )
        instance.__dict__[self.name] = value
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

class DescriptorValidator:
    def __set_name__(self, owner, name):
        self.name = name
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(
                 f"The object is of type [{type(value).__name__}], "
                "but a [string] object was expected."
            )
        if value != "no description":
            check = len(value)
            if check < 16 or check > 2048:
                raise ValueError(
                    "The string of description must be between 16 and 2048 chars long."
                )
        instance.__dict__[self.name] = value
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

class StatusValidator:
    def __set_name__(self, owner, name):
        self.name = name
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(
                 f"The object is of type [{type(value).__name__}], "
                "but a [integer] object was expected."
            )
        if not value in range(0,3):
            raise ValueError(
                "The value must be between 0 and 2, inclusive."
            )
        instance.__dict__[self.name] = value
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

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
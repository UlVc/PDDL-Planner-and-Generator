class Variable:
    """Representation of a typed variable."""
    def __init__(self, name, type, value=None):
        """
        :param name: Name of the variable. The names start with ?
        :param type: Type of the variable. It must be registered in the domain description.
        :param value: Object linked to this variable, if it's None the variable is free.
        """
        self.name = name
        self.type = type
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        """
        :param new_value: New value to assign.
        """
        if new_value and new_value.type != self.type:
            raise Exception(f"{new_value} is not of type {self.type}.")
        self._value = new_value

    @value.deleter
    def value(self):
        self._value = None

    def __str__(self):
        if self._value:
            return self._value.name
        return f'{self.name} - {self.type}'
    
    def __eq__(self, variable):
        if self.type == variable.type:
            if self._value:
                return self._value.name == variable._value.name
            return self.name == variable.name
        return False

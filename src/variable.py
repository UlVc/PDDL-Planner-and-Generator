class Variable:
    """ Variable tipada. """
    def __init__(self, nombre, tipo, valor=None):
        """
        :param nombre: símbolo nombre de esta variable.  Los nombres de variables inician con ?
        :param tipo: tipo de la variable, debe estar registrado en la descripción del dominio
        :param valor: objeto vinculado a esta variable, si es None la variable está libre
        """
        self.nombre = nombre
        self.tipo = tipo
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, valor_nuevo):
        """
        Permite asignar None o un valor de tipo de esta variable.
        """
        if valor_nuevo and valor_nuevo.tipo != self.tipo:
            raise Exception(f"{valor_nuevo} no es de tipo {self.tipo}")
        self._valor = valor_nuevo

    @valor.deleter
    def valor(self):
        self._valor = None

    def __str__(self):
        if self.valor:
            return self.valor.nombre
        return "{} - {}".format(self.nombre, self.tipo)
    
    def __eq__(self, variable):
        if self.tipo == variable.tipo:
            if self.valor:
                return self.valor.nombre == variable.valor.nombre
            return self.nombre == variable.nombre
        return False

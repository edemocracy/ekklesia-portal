class Cell:
    model_properties = []

    def __init__(self, model):
        self._model = model

    def __getattr__(self, name):
        if name in self.model_properties:
            return getattr(self._model, name)

        raise AttributeError(name)


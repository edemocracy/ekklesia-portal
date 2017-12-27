from ekklesia_portal.helper.cell import Cell


class ArgumentRelationCell(Cell):
    model_properties = ['proposition', 'argument']

    @property
    def proposition_url(self):
        return self.link(self._model.proposition)

    @property
    def argument_url(self):
        return self.link(self._model.argument)

    @property
    def proposition_title(self):
        return self.proposition.title

    @property
    def argument_title(self):
        return self.argument.title

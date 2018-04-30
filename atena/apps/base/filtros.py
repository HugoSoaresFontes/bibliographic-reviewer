from django import forms

class BaseFiltroForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop('queryset', None)
        return super(BaseFiltroForm, self).__init__(*args, **kwargs)

    def pesquisar(self):
        return self.queryset
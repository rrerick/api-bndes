from django import forms
from .models import Empresa


class CnpjForm(forms.Form):
    cnpj = forms.CharField(label='CNPJ', initial='14 digitos')

    def save(self, *args):
        context = Empresa(
            cnpj_id=int(self.data['cnpj'])
        )
        context.save()
        return context

    def __str__(self, *args, **kwargs):
        return self.data['cnpj']

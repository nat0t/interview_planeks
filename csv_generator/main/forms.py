from django import forms

from main.models import Schema, SchemaDetails


class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ('name', 'delimiter', 'quotes',)


SchemaDetailsFormSet = forms.inlineformset_factory(Schema, SchemaDetails, fields=('name', 'type', 'order',), extra=1)


class DatasetForm(forms.Form):
    class Meta:
        rows = forms.IntegerField()

    # def is_valid(self):
    #     if self.rows > 0:
    #         return super(DatasetForm, self).is_valid()
    #     else:
    #         return False

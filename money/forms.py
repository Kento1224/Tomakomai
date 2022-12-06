from django import forms
from .models import Money
class SpendingForm(forms.Form):
    choices = (
            ('食費', '食費'),
            ('学費', '学費'),
            ('交通費', '交通費'),
            ('趣味', '趣味'),
            )
    use_date = forms.DateTimeField(label='日付')
    cost = forms.IntegerField(label='金額')
    detail = forms.CharField(
            max_length=200,
            label='用途'
            )
    category = forms.ChoiceField(choices=choices, label='カテゴリー')

    choices2 = (
            ('青葉町', '青葉町'),
            ('明野新町', '明野新町'),
            ('明野元町', '明野元町'),
            ('あけぼの町', 'あけぼの町'),
            ('ウトナイ北','ウトナイ北')
            )
    location = forms.ChoiceField(choices=choices2, label='取引場所')
import datetime, requests

from django import forms


class CreateForm(forms.Form):
    response = requests.get('https://opentdb.com/api_category.php')
    data = response.json()
    categories = []
    for i in data['trivia_categories']:
        categories.append(i['name'])

    name = forms.CharField(label='Name', max_length=100)
    start_date = forms.DateField(initial=datetime.date.today)
    end_date = forms.DateField(initial=datetime.date.today() + datetime.timedelta(days=7))
    category = forms.ChoiceField(choices=[1,2,3,4,5,6,7,9])
    #difficulty = forms.ChoiceField(choices = ['Any', 'Easy', 'Medium', 'Hard'])

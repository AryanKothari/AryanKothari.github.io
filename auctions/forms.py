from django import forms

CATEGORY_CHOICES= [
    ('No Category', 'No Category'),
    ('Fashion', 'Fashion'),
    ('Sport', 'Sport'),
    ('Electronics', 'Electronics'),
    ('Accesories', 'Accesories'),
    ]
 
class NewListingForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(label="Description:", widget=forms.Textarea(attrs={"rows":10, "cols":80}))
    starting_bid = forms.IntegerField(label="Starting Bid ($):", min_value=1)
    category = forms.CharField(label="Category",max_length=100, widget=forms.Select(choices=CATEGORY_CHOICES))
    imageURL = forms.CharField(label="Image URL (Optional)", required=False, widget=forms.TextInput(attrs={'placeholder': 'https://blah-blah.jpg...'}))

    def __init__(self, *args, **kwargs):
        super(NewListingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NewCommentForm(forms.Form):
    body = forms.CharField(label="Type Your Comment Here:", widget=forms.Textarea(attrs={"rows":10, "cols":80}))
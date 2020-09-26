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
    starting_bid = forms.IntegerField(label="Starting Bid ($):")
    category = forms.CharField(label="Category",max_length=100, widget=forms.Select(choices=CATEGORY_CHOICES))
    image = forms.ImageField(label="Image (Optional)", required=False)

class NewCommentForm(forms.Form):
    body = forms.CharField(label="Type Your Comment Here:", widget=forms.Textarea(attrs={"rows":10, "cols":80}))

from django import forms

class NewListingForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(label="Description:", widget=forms.Textarea(attrs={"rows":10, "cols":80}))
    starting_bid = forms.IntegerField(label="Starting Bid ($):")
    category = forms.CharField(label="Category (Optional)",max_length=100, required=False)
    image = forms.ImageField(label="Image (Optional)", required=False)

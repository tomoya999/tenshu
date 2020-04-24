from django import forms
from .models import Shop
class ShopForm(forms.ModelForm):
    """ お店情報の入力フォーム """
    class Meta:
        model = Shop
        fields = (
                'name', 'slug', 'phone_number', 'access',
                'buisiness_time1', 'buisiness_time2',
                'non_buisiness_day', 'seats', 'park',
                'youtube_url', 'twitter_id', 'greeting',
                )
        labels = {
                'name': '店名　',
                'slug': '店名ローマ字',
                'phone_number': '電話番号',
                'access': 'アクセス',
                'buisiness_time1': '営業時間',
                'buisiness_time2': '',
                'non_buisiness_day': '定休日',
                'seats': '席数　',
                'park': '駐車場',
                'youtube_url': 'YouTube動画URL',
                'twitter_id': 'Twitterアカウント名',
                'greeting': '挨拶',
        }

        widgets = {
                'name': forms.TextInput(attrs={'placeholder': '例 : 麺屋武内'}),
                'slug': forms.TextInput(attrs={'placeholder': '例 : menyatakeuchi'}),
                'phone_number': forms.TextInput(attrs={'placeholder': '例 : 080xxxxxxxx'}),
                'access': forms.TextInput(attrs={'placeholder': '例 : 大宮駅から徒歩23分'}),
                'buisiness_time1': forms.TextInput(attrs={'placeholder': '例 : 11時 - 15時'}),
                'buisiness_time2': forms.TextInput(attrs={'placeholder': '例 : 17時 - 21時'}),
                'non_buisiness_day': forms.TextInput(attrs={'placeholder': '例 : 毎週月曜日'}),
                'seats': forms.TextInput(attrs={'placeholder': '例 : 6席'}),
                'park': forms.TextInput(attrs={'placeholder': '例 : 有り'}),
                'youtube_url': forms.TextInput(attrs={'placeholder': '例 : '}),
                'twitter_id': forms.TextInput(attrs={'placeholder': '例 : xxxxxxx  @は不要'}),
                'greeting': forms.Textarea(attrs={'placeholder': '例 : こんにちは、麺屋武内店主の武内友弥です。よろしくね！'}),
        }

                

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['labels'] = '店名'
        self.fields['slug'].widget.attrs['labels'] = '店名ローマ字'
        self.fields['phone_number'].widget.attrs['labels'] = '電話番号'
        self.fields['access'].widget.attrs['labels'] = 'アクセス'
        self.fields['buisiness_time1'].widget.attrs['labels'] = '営業時間'
        self.fields['buisiness_time2'].widget.attrs['labels'] = ''
        self.fields['non_buisiness_day'].widget.attrs['labels'] = '定休日'
        self.fields['seats'].widget.attrs['labels'] = '席数'
        self.fields['park'].widget.attrs['labels'] = '駐車場'
        self.fields['youtube_url'].widget.attrs['labels'] = 'YouTube動画URL'
        self.fields['twitter_id'].widget.attrs['labels'] = 'Twitterアカウント名'
        self.fields['greeting'].widget.attrs['labels'] = '挨拶'
        
        self.fields['youtube_url'].required = False
        self.fields['twitter_id'].required = False
        self.fields['greeting'].required = False
        
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
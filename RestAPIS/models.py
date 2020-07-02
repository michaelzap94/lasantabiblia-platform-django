from django.db import models
from django.conf import settings

class Label(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    _id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=10)
    permanent = models.IntegerField(default=0,blank=True, null=True)
    state = models.IntegerField(default=0,blank=True, null=True)

    # def create(self, validated_data): # If you implement this, you'll have to call .save on the Account object in the views.py file
    #     label = Label(
    #         email=validated_data['email'], 
    #         account_type=validated_data['account_type'],
    #         fullname=validated_data.get('fullname', None), 
    #         firstname=validated_data.get('firstname', None), 
    #         lastname=validated_data.get('lastname', None))
    #     account.set_unusable_password()
    #     account.save()
    #     return account

class Verses_Marked(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    _id = models.CharField(max_length=200)
    label_id = models.CharField(max_length=200)
    book_number = models.IntegerField()
    chapter = models.IntegerField()
    verseFrom = models.IntegerField()
    verseTo = models.IntegerField()
    label_name = models.CharField(max_length=200)
    label_color = models.CharField(max_length=200)
    label_permanent = models.IntegerField(default=0, blank=True)
    note = models.TextField(blank=True, null=True)
    date_created = models.CharField(max_length=200)
    date_updated = models.CharField(max_length=200)
    UUID = models.CharField(max_length=100)
    state = models.IntegerField(default=0,blank=True, null=True)

    # def save(self): # If you implement this, you'll have to call .save on the Account object in the views.py file
    #     account = Account(
    #         email=validated_data['email'], 
    #         account_type=validated_data['account_type'],
    #         fullname=validated_data.get('fullname', None), 
    #         firstname=validated_data.get('firstname', None), 
    #         lastname=validated_data.get('lastname', None))
    #     account.set_unusable_password()
    #     account.save()
    #     return account

class Verses_Learned(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    _id = models.CharField(max_length=200)
    UUID = models.CharField(max_length=100)
    label_id = models.CharField(max_length=200)
    learned = models.IntegerField(default=0,blank=True)
    priority = models.IntegerField(default=0,blank=True, null=True)
    state = models.IntegerField(default=0,blank=True, null=True)

    # def save(self): # If you implement this, you'll have to call .save on the Account object in the views.py file
    #     account = Account(
    #         email=validated_data['email'], 
    #         account_type=validated_data['account_type'],
    #         fullname=validated_data.get('fullname', None), 
    #         firstname=validated_data.get('firstname', None), 
    #         lastname=validated_data.get('lastname', None))
    #     account.set_unusable_password()
    #     account.save()
    #     return account

class Notes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    _id = models.CharField(max_length=200)
    label_id = models.CharField(max_length=200)
    title = models.CharField(max_length=400)
    content = models.TextField()
    date_created = models.CharField(max_length=200)
    date_updated = models.CharField(max_length=200)
    state = models.IntegerField(default=0,blank=True, null=True)
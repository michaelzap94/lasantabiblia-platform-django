from django.db import models
from django.conf import settings

class Label(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    _id = models.IntegerField()
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=10)
    permanent = models.IntegerField(default=0,blank=True, null=True)
    state = models.IntegerField(default=0,blank=True)

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
    _id = models.IntegerField()
    label_id = models.IntegerField()
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
    _id = models.IntegerField()
    UUID = models.CharField(max_length=100)
    label_id = models.IntegerField()
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


# CREATE TABLE labels (_id INTEGER PRIMARY KEY, name VARCHAR NOT NULL, color VARCHAR NOT NULL, permanent INTEGER DEFAULT 0);
# CREATE TABLE verses_marked (_id INTEGER PRIMARY KEY, label_id INTEGER NOT NULL, book_number INTEGER NOT NULL, chapter INTEGER NOT NULL, verseFrom INTEGER NOT NULL, verseTo INTEGER NOT NULL, label_name VARCHAR NOT NULL, label_color VARCHAR NOT NULL, label_permanent INTEGER DEFAULT 0, note VARCHAR, date_created datetime DEFAULT current_timestamp, date_updated datetime DEFAULT current_timestamp, UUID VARCHAR NOT NULL, state INTEGER DEFAULT 0, FOREIGN KEY (label_id) REFERENCES labels (_id) ON DELETE CASCADE);
# CREATE TABLE verses_learned (_id INTEGER PRIMARY KEY, UUID VARCHAR NOT NULL, label_id INTEGER NOT NULL, learned INTEGER DEFAULT 0, priority INTEGER DEFAULT 0);
from django.db import models
from datetime import datetime

class Resource(models.Model):
    def makeResourcePath(self, fileName):
        return 'resources/{type}/{lang}/{fileName}/'.format(type = self.resource_type, lang = self.language, fileName=fileName)

    name = models.CharField(max_length=100)
    language = models.CharField(max_length=20, choices=[('en', 'English'), ('es', 'Spanish'),('pt', 'Portuguese'), ('fr', 'French'), ('ko','Korean'), ('ru', 'Russian')])
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=50, choices=[('bibles', 'Bible'), ('concordances', 'Concordance'),('dictionaries', 'Dictionary'), ('maps', 'Map')])
    version = models.IntegerField(default=0)
    resource = models.FileField(upload_to=makeResourcePath)#folder inside the media folder.+ folder structure of date
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(auto_now=True) # default=datetime.now, blank=True
    #WILL BE AVAILABLE WHEN WE GET THE 'resource'
    size = models.IntegerField(default=0) # resource.size
    filename = models.CharField(blank=True, max_length=200) # os.path.basename(self.file.name)

    def __str__(self):
        return self.name

    #functions for specific Records in the Table Blog.
    def summary(self):
        return self.description[:100]

    def list_date_pretty(self):
        return self.list_date.strftime('%e %b %Y')

    def save(self, *args, **kwargs):
        self.version = self.version + 1
        if self.resource != None:
            self.size=self.resource.size
            self.filename=str(self.resource)
        super(Resource, self).save(*args, **kwargs)
    


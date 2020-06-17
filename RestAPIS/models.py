from django.db import models

class Label(models.Model):
    _id = models.IntegerField()
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=10)
    permanent = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Verses_Marked(models.Model):
    _id = models.IntegerField()
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=10)
    permanent = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Verses_Learned(models.Model):
    _id = models.IntegerField()
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=10)
    permanent = models.IntegerField(default=0)
    def __str__(self):
        return self.name

# CREATE TABLE labels (_id INTEGER PRIMARY KEY, name VARCHAR NOT NULL, color VARCHAR NOT NULL, permanent INTEGER DEFAULT 0);
# CREATE TABLE verses_marked (_id INTEGER PRIMARY KEY, label_id INTEGER NOT NULL, book_number INTEGER NOT NULL, chapter INTEGER NOT NULL, verseFrom INTEGER NOT NULL, verseTo INTEGER NOT NULL, label_name VARCHAR NOT NULL, label_color VARCHAR NOT NULL, label_permanent INTEGER DEFAULT 0, note VARCHAR, date_created datetime DEFAULT current_timestamp, date_updated datetime DEFAULT current_timestamp, UUID VARCHAR NOT NULL, state INTEGER DEFAULT 0, FOREIGN KEY (label_id) REFERENCES labels (_id) ON DELETE CASCADE);
# CREATE TABLE verses_learned (_id INTEGER PRIMARY KEY, UUID VARCHAR NOT NULL, label_id INTEGER NOT NULL, learned INTEGER DEFAULT 0, priority INTEGER DEFAULT 0);
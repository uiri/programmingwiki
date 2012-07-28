from django.db import models

# Create your models here.
class Page(models.Model):
    title = models.CharField(max_length=255)
    redirect = models.BooleanField()
    revision = models.PositiveIntegerField()
    contents = models.TextField()
    talkcontents = models.TextField()

    def __unicode__(self):
        return self.contents

    def talk(self):
        return self.talkcontents

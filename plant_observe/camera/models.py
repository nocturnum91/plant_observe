from django.db import models

# Create your models here.
class Image(models.Model):
    image_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str(self):
        return self.image_name

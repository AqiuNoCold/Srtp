from django.db import models

# Create your models here.
class SpiderDb(models.Model):
    topic = models.CharField(db_column='Topic', max_length=45)  # Field name made lowercase.
    origin = models.CharField(db_column='Origin', max_length=45)  # Field name made lowercase.
    author = models.CharField(db_column='Author', max_length=45)  # Field name made lowercase.
    abstract = models.CharField(db_column='Abstract', max_length=255, blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=255, blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='Url', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'spider_db'

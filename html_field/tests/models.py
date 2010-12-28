from django.db import models
from html_field.db.models import HTMLField
from html_field import html_cleaner

c = html_cleaner.HTMLCleaner(allow_tags=['a', 'img', 'em', 'strong'])

class NewsStory(models.Model):
	headline = models.CharField(max_length=200)
	pub_date = models.DateField(blank=True, null=True)
	body = HTMLField(c, blank=True)

def img_location(instance, filename):
	return 'news_images/story_%d/%s'%(instance.story.id, filename)

class NewsImage(models.Model):
	story = models.ForeignKey('NewsStory', related_name='images')
	credit = models.CharField(max_length=200, blank=True)
	caption = models.TextField(blank=True)
	image = models.ImageField(upload_to=img_location)
	public = models.BooleanField()




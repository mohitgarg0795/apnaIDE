from __future__ import unicode_literals

from django.db import models

class CodeHistory(models.Model):
	code=models.TextField()
	timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)
	status=models.CharField(max_length=5)
	time_used=models.DecimalField(max_digits=7,decimal_places=6)
	lang=models.CharField(max_length=10)
	web_link=models.URLField(max_length=50)
	output=models.TextField()

	def __unicode__(self):
		return self.web_link
	"""
	class Meta:			#to order the queryset directly or use .order_by() in the views while querying
		ordering=['-id']
	"""
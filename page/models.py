from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class CodeHistory(models.Model):
	username=models.ForeignKey(User,null=True)
	code=models.TextField()
	timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)
	status=models.CharField(max_length=5)
	time_used=models.DecimalField(max_digits=7,decimal_places=6)
	lang=models.CharField(max_length=10)
	web_link=models.URLField(max_length=50)
	output=models.TextField()
	code_id=models.CharField(max_length=6)
	code_input=models.TextField()

	def __unicode__(self):
		return self.web_link
"""
	class Meta:			#to order the queryset directly or use .order_by() in the views while querying
		ordering=['-id']
"""

"""class Users(models.Model):
	username=models.CharField(max_length=50,primary_key=True)
	email=models.EmailField()
	password=models.CharField(max_length=100)

	def __unicode__(self):
		return self.username
"""
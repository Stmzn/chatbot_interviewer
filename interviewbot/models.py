from django.db import models

# Create your models here.

class PersonalDetails(models.Model):
	interview_number = models.IntegerField()
	first_name = models.CharField(max_length = 200)
	email_id = models.CharField(max_length = 200)
	interview_type = models.CharField(max_length = 200)
	cv_file = models.FileField()
	initial_status = models.CharField(max_length=200)
	status = models.CharField(max_length = 200)
	user = models.CharField(max_length = 100)

class Interview(models.Model):
	interview_number = models.IntegerField()
	questions = models.CharField(max_length = 1000,null = True)
	answers = models.CharField(max_length = 1000,null = True)




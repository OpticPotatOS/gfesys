from django.db import models
import spirit.models.user
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractBaseUser
import spirit.models.user
from .memberusermanager import MemberUserManager
# Create your models here.
class Member(spirit.models.user.AbstractUser):
	objects = MemberUserManager()
	
	GravatarTypes = (('identicon', 'A geometric pattern based on an email hash'),
	('monsterid', "A generated 'monster' with different colors, faces, etc"),
	('wavatar', "Generated faces with differing features and backgrounds"),
	('retro', 'awesome generated, 8-bit arcade-style pixelated faces'))
	
	def __str__(self):
		nicky = " " if self.nick == "" else " \"" + self.nick +  "\" "
		return self.first_name + nicky + self.last_name
	
	nick = models.CharField(max_length=200)
	birthdate = models.CharField(max_length=200)
	
	phone = models.CharField(max_length=200)
	mobile = models.CharField(max_length=200)
	
	street = models.CharField(max_length=200)
	city = models.CharField(max_length=200)
	country_id = CountryField()
	zip = models.CharField(max_length=200)
	careof = models.CharField(max_length=200)	
	socialsecuritynumber = models.CharField(max_length=200)
	
	joinedon = models.DateTimeField('Joined on', auto_now_add=True)
	refreshedon = models.DateTimeField('Refreshed on')
	
	image = models.ImageField(max_length=500, width_field='image_width', height_field='image_height', upload_to='members')
	image_height = models.IntegerField(default=0)
	image_width = models.IntegerField(default=0)
	
	is_opt_in = models.BooleanField(default=False)
	use_gravatar = models.BooleanField(default=False)
	gravatar_type = models.CharField(default='identicon', max_length=20, choices=GravatarTypes)
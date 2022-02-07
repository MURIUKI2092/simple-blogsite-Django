from django.db.models.deletion import CASCADE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#model for the topic to be discussed in the site

class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

# model for the discussion which will happen
class Discussion(models.Model):
    #stores name of the user
    name=models.CharField(max_length=200)
    #stores the host of the discussion
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    # stores the topic of the discussion
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
#stores the description of the user
    description=models.TextField(null=True,blank=True)
    #stores the participants who  participates in the 
    participants=models.ManyToManyField(User,related_name='participants',blank=True)
    # stores the time a discussion was updated
    timeUpdated=models.DateTimeField(auto_now=True)
    # stores the time when the discussion was created 
    timeCreated=models.DateTimeField(auto_now_add=True)

    #arranging the last update to be the first to be shown
    class Meta:
        ordering=['-timeCreated','-timeUpdated']

    def __str__(self):
        return self.name

class  Blog(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    #stores the blog room/space that when the blog
    # is written it is stored in here.
    # with cascade all the blogs will be deleted once the
    #Discussion is deleted
    discuss=models.ForeignKey(Discussion,on_delete=models.CASCADE)
    # the actual message/body
    body=models.TextField()
    # stores the time a discussion was updated
    timeUpdated=models.DateTimeField(auto_now=True)
    #stores the time the discussion was created
    timeCreated=models.DateTimeField(auto_now_add=True)


      

# deals with the ordering of the class.
    class Meta:
        ordering=['-timeCreated','-timeUpdated']
# returns the body with the specified   characters no clattering all over.
    def __str__(self):
        return self.body[0:50]
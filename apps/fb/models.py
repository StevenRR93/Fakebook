#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
import datetime
import re

class UsersManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        #print(Users.objects.filter(email = postData['email']).exists())
        if len(postData['first_name']) < 2:
            errors["first_name"]="First name should have more than 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"]= "Last name should have more than 2 characters"
        if len(postData['password'])< 8:
            errors['password']= "Password should be more than 8 characters"
        if (not re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', postData['email'])):
            errors['email'] = "E-mail address should be a valid e-mail address"
        if (Users.objects.filter(email= postData['email']).exists()):
            errors['email']= "E-mail address already used"
        if postData['birthday']== None:
            errors['birtday']= "Date of birth is not valid"
        g = postData.get('gender', None)
        if not ((g == "male") | (g == "female") | (g == "other")):
            errors['gender']= "Please select a gender"
        # print postData
        return errors

class FriendManager(models.Manager):
    def basic_validator(self, id1, id2):
        errors = {}
        if (id1 == id2):
            errors["friend1_id"]= "You cannot add yourself"
        elif (Friendship.objects.filter(friend1_id= int(id1), friend2_id = int(id2)).exists()):
            errors["friend1_id"]= "You are already friends"
        return errors

class MessageManager(models.Manager):
    def basic_validator(self, postData, id):
        errors = {}
        if id == postData['userval']:
            errors['userval'] = "You can't message yourself"
        if len(postData['msg']) < 1:
            errors['msg']= 'You cant send a blank message'
        return errors

class ThreadManager(models.Manager):
    def basic_validator(self, postData, id):
        errors = {}
        if id == postData['userval']:
            errors['userval'] = "You can't message yourself"
        return errors

class PostManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['pst']) < 1:
            errors['pst']= 'You cant make a blank post'
        return errors

class CommentManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['cmnt']) < 1:
            errors['cmnt']= 'You cant make a blank post'
        return errors

class Users(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    job = models.CharField(max_length=255, blank = True)
    workplace = models.CharField(max_length=255, blank = True)
    education = models.CharField(max_length=255, blank = True)
    location = models.CharField(max_length=255, blank = True)
    birthplace = models.CharField(max_length=255, blank = True)
    is_logged_in = models.BooleanField(max_length=255, default = False)
    image = models.ImageField(default= None)
    friend1 = models.ManyToManyField("Users", related_name= "friend2")
    notifications = models.ManyToManyField("Users", related_name = "friendrequest")
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    def __repr__(self):
        return "<Users object: {} {} {} {}>".format(self.id,self.first_name,self.last_name,self.email)

    # *************************
    objects = UsersManager()
    # *************************



# class Friendship(models.Model):
#     friend1 = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="friend1")
#     friend2 = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="friend2")
#     created_at = models.DateTimeField(auto_now_add= True)
#     updated_at = models.DateTimeField(auto_now= True)
#     def __repr__(self):
#         return"<Friendship object: {}{}>".format(self.friend1.id,self.friend2.id)
#     # *************************
#     objects = FriendManager()
#     # *************************

class Post(models.Model):
    pstsender = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="pstreceiver")
    pstreceiver = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="pstsender")
    pst = models.TextField()
    image = models.ImageField(default= None)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    def __repr__(self):
        return"<Post object: {} {} {}>".format(self.pstsender,self.pstreceiver, self.pst)
    # *************************
    objects = PostManager()
    # *************************


class Comment(models.Model):
    cmntsender = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="cmntreceiver")
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comment")
    cmnt = models.TextField()
    likes = models.ManyToManyField(Users, related_name = "liked_by")
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    def __repr__(self):
        return"<Comment object: {}{}>".format(self.cmntsender,self.cmnt, self.cmnt)
    # *************************
    objects = CommentManager()
    # *************************

class Thread(models.Model):
    user1 = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user2")
    user2 = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user1")
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    def __repr__(self):
        return"<Thread object: {} {}>".format(self.user1.id, self.user2.id)
    # *************************
    objects = ThreadManager()
    # *************************

class Message(models.Model):
    msgsender = models.ForeignKey(Users ,on_delete=models.CASCADE, related_name="msgreceiver")
    msgreceiver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="msgsender")
    msg = models.TextField()
    thread =  models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="message")
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    def __repr__(self):
         return"<Message object: {} {} {}>".format(self.msgsender,self.msgreceiver, self.msg)
    # *************************
    objects = MessageManager()
    # *************************


from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db import models
from django.db.models.signals import post_save

"""
An extended user profile for TDE, with custom fields and methods
"""

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    role = models.TextField(null=True)


"""
Create a profile upon user creation
"""

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

"""
A Model representing a directional relationship between two users.
Used for user-to-user interactions such as messaging

Will be referred to as UUR for brevity
"""
class UserToUserRelationship(models.Model):
    subject_user = models.ForeignKey('auth.User', related_name="subject_users")
    object_user  = models.ForeignKey('auth.User', related_name="object_users")

    class Meta:
        unique_together = ('subject_user', 'object_user')

"""
A Model for a user-to-user message, which uses the UUR as a foreign key

The next and previous message fields create a doubly-linked list of messages and their replies
"""
class Message(models.Model):
    users = models.ForeignKey('UserToUserRelationship')
    title = models.TextField()
    content = models.TextField()
    sent_at = models.DateTimeField('Sent at')
    previous_message = models.ForeignKey('Message', null=True, related_name="previous_messages")
    next_message = models.ForeignKey('Message', null=True, related_name="next_messages")

"""
A Model for a design method. The contents of a method is broken down as follows:

Purpose: what is the method used for? what design problems does it solve?
Procedure: how do you apply the method?
Principles: what kinds of design principles is this method based on? why does it work?
"""

class Method(models.Model):
    title = models.TextField()
    purpose = models.TextField()
    procedure = models.TextField()
    principles = models.TextField()

    # TODO figure out constraints

    # find author
    def author(self):
        return UserToMethodRelationship.objects.get(
            method = self,
            is_author = True).user

"""
A Model for a relationship between a method and a user (non-directional)

This gives a flexible way to map various ways that users can be related to a method, such as
rating, favoriting, creating, commenting, and other future functions. It also keeps the database
in BCNF and makes it extendable to additional features.

For the sake of efficiency, one-to-one relationships with no extra information are stored here

Will be referred to as UMR for brevity
"""

class UserToMethodRelationship(models.Model):
    user = models.ForeignKey('auth.User')
    method = models.ForeignKey('Method')

    # one-to-one fields with no extra content
    is_author = models.BooleanField()
    is_favorite = models.BooleanField()

    class Meta:
        unique_together = ('user', 'method')

"""
A Model for a rating on a method, using the UMR as a foreign key
"""

class MethodRating(models.Model):
    umr = models.ForeignKey('UserToMethodRelationship')
    rating = models.IntegerField()

"""
A Model for a comment, using the UMR as a foreign key

Users can comment on both methods and method comments
"""

class Comment(models.Model):
    umr = models.ForeignKey('UserToMethodRelationship')
    content = models.TextField()
    reply_to = models.ForeignKey('Comment', null=True, related_name="replies")

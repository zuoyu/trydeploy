from django.db import models
from author.models import Author

class FollowManager(models.Manager):
    # call this by Follows.objects.getFollowers(user id)

    def getFollowers(self, user):
        return self.get_queryset().filter(followed=user)

    def getFollowing(self, user):
        return self.get_queryset().filter(follower=user)

    def is_friends(self, user1, user2):
        return False

    def get_friends(self, user):
        return []

    def mutualFollow(self, follower1, follower2):
        firstcase = self.isFollowing(follower1, follower2)
        reversecase = self.isFollowing(follower2, follower1)

        if not firstcase and not reversecase:
            self.follow(follower1, follower2)
            self.follow(follower2, follower1)
        elif not firstcase and reversecase:
            self.follow(follower1, follower2)
        elif firstcase and not reversecase:
            self.follow(follower2, follower1)
        else:
            print("dont add any")

    def mutualUnFollow(self, follower1, follower2):
        firstcase = self.isFollowing(follower1, follower2)
        reversecase = self.isFollowing(follower2, follower1)

        if not firstcase and not reversecase:
            self.unfollow(follower1, follower2)
            self.unfollow(follower2, follower1)
        elif not firstcase and reversecase:
            self.unfollow(follower1, follower2)
        elif firstcase and not reversecase:
            self.unfollow(follower2, follower1)
        else:
            print("dont add any")

    def follow(self, follower1, follower2):
        follow = self.create(followed=follower2, follower=follower1)
        return follow

    def unfollow(self, follower1, follower2):
        try:
            self.get(followed=follower1, follower=follower2).delete()
            return True
        except:
            return False

    def isFollowing(self, follower1, follower2):
        follow_exist = self.get_queryset().filter(followed=follower1, follower=follower2).exists()
        if follow_exist:
            return True
        else:
            return False


class Follows(models.Model):
    
    followed = models.ForeignKey(Author, related_name='followed')
    follower = models.ForeignKey(Author, related_name='follower')
    objects = FollowManager()

    class Meta:
        verbose_name = "Following"
        verbose_name_plural = "Followers"
        unique_together = (('followed', 'follower'),)

    def __unicode__(self):  # For Python 2, use __str__ on Python 3
        try:
            return "{sender} is followed by {reciever}\n".format(sender=self.followed, reciever=self.follower)
        # return "{reciever\n}".format(reciever=self.reciever)
        except:
            return "{solo} prob has no followers)".format(solo=self.followed)

    def getafollowing(self):
        return self.followed

    def getafollower(self):
        return self.follower

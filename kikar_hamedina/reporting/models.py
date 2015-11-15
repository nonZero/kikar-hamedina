from django.db import models
from django.contrib.auth.models import User

from facebook_feeds.models import Facebook_Status


class WeeklyReportRecipients(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField(null=False, unique=True)
    is_active = models.BooleanField(null=False, default=True)
    is_beta = models.BooleanField(null=False, default=False)
    date_joined = models.DateTimeField(auto_now=True)


class RSSFeedKeyWord(models.Model):
    user = models.ForeignKey(User, related_name='words_in_rss_feed')
    keyword = models.CharField(max_length=64, blank=False, null=False, unique=True)


class RSSFeedExcludeStatuses(models.Model):
    user = models.ForeignKey(User, related_name='excluded_statuses')
    status = models.ForeignKey(Facebook_Status, related_name='excluded_by_users')

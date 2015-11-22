import datetime
import os

from autotag import autotag
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django_pandas.managers import DataFrameManager
from slugify import slugify
from taggit.managers import TaggableManager
from unidecode import unidecode

from facebook_feeds.managers import Facebook_StatusManager, \
    Facebook_FeedManager
from kikartags.managers import _KikarTaggableManager
from kikartags.models import TaggedItem

DEFAULT_THRESHOLD = 0

IS_ELECTIONS_MODE = getattr(settings, 'IS_ELECTIONS_MODE', False)

# needs_refresh - Constants for quick status refresh
MAX_STATUS_AGE_FOR_REFRESH = getattr(settings, 'MAX_STATUS_AGE_FOR_REFRESH',
                                     60 * 60 * 24 * 2)  # 2 days
MIN_STATUS_REFRESH_INTERVAL = getattr(settings, 'MIN_STATUS_REFRESH_INTERVAL',
                                      5)  # 5 seconds
MAX_STATUS_REFRESH_INTERVAL = getattr(settings, 'MAX_STATUS_REFRESH_INTERVAL',
                                      60 * 10)  # 10 minutes

# tag name regex
TAG_NAME_CHARSET = ur'[\w\s\-:"\'!\?&\.#\u2010-\u201f\u05f3\u05f4]'
TAG_NAME_REGEX = u'^%s+$' % TAG_NAME_CHARSET


class Facebook_Persona(models.Model):
    # Relation to MKs objects
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey()

    # Relation to Candidates objects
    alt_content_type = models.ForeignKey(ContentType, related_name='alt',
                                         null=True, blank=True)
    alt_object_id = models.PositiveIntegerField(null=True, blank=True)
    alt_content_object = generic.GenericForeignKey(ct_field="alt_content_type",
                                                   fk_field="alt_object_id")

    main_feed = models.SmallIntegerField(null=True, default=0, blank=True)

    @property
    def get_main_feed(self):
        try:
            return Facebook_Feed.objects.get(id=self.main_feed)
        except:
            return None  # TODO: What should we return here when no main feed is defined/ no feeds exist?

    @property
    def owner(self):
        return self.alt_content_object if IS_ELECTIONS_MODE else self.content_object

    @property
    def owner_id(self):
        return self.alt_object_id if IS_ELECTIONS_MODE else self.object_id

    def __unicode__(self):
        if IS_ELECTIONS_MODE:
            return "Facebook_Persona: %s %s %s %s" % (
            self.content_type, self.object_id,
            self.alt_content_type, self.alt_object_id)
        return "Facebook_Persona: %s %s" % (self.content_type, self.object_id)


class Facebook_Feed(models.Model):
    FEED_TYPES = (
        ('PP', 'Public Page'),
        ('UP', 'User Profile'),
        ('NA', 'Unavailable Profile'),
        ('DP', 'Deprecated Profile'),
    )

    DEFAULT_DAYS_BACK_FOR_POPULARITY_DIF = getattr(settings,
                                                   'DEFAULT_DAYS_BACK_FOR_POPULARITY_DIF',
                                                   7)

    persona = models.ForeignKey('Facebook_Persona', related_name='feeds')
    vendor_id = models.TextField(null=True, blank=True)
    username = models.TextField(null=True, default=None, blank=True)
    birthday = models.TextField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True, max_length=2000)
    picture_square = models.URLField(null=True, blank=True, max_length=2000)
    picture_large = models.URLField(null=True, blank=True, max_length=2000)
    feed_type = models.CharField(null=False, max_length=2, choices=FEED_TYPES,
                                 default='PP')
    requires_user_token = models.BooleanField(default=False, null=False)
    is_current = models.BooleanField(default=True, null=False)
    current_fan_count = models.IntegerField(default=0, null=False)
    locally_updated = models.DateTimeField(blank=True,
                                           default=timezone.datetime(1970, 1,
                                                                     1),
                                           null=True)

    # Public Page Only
    about = models.TextField(null=True, blank=True, default='')
    website = models.URLField(null=True, blank=True, max_length=2000)

    objects = DataFrameManager()

    current_feeds = Facebook_FeedManager()

    class Meta:
        ordering = [
            'feed_type']  # This will create a preference for Public Page over User Profile when both exist.

    def __unicode__(self):
        return "%s %s (%s)" % (slugify(self.username), self.vendor_id, self.id)

    def save(self, *args, **kwargs):
        '''On save, update locally_updated fields'''
        self.locally_updated = timezone.now()
        return super(Facebook_Feed, self).save(*args, **kwargs)

    @property
    def get_current_fan_count(self):
        popularity = 0
        if self.feed_type == 'PP':
            try:
                popularity = Feed_Popularity.objects.filter(feed=self).latest(
                    'date_of_creation').fan_count
            except Feed_Popularity.DoesNotExist:
                pass
        return popularity

    def popularity_dif(self, days_back, return_value='all_dict'):

        dif_dict = {'fan_count_dif_nominal': 0,
                    'fan_count_dif_growth_rate': 0.0,
                    'fan_count_at_requested_date': 0,
                    'is_interpolated': False,
                    'date_of_value': datetime.date.today()}

        dif_dict_default = dif_dict.copy()

        is_interpolated = False

        feed_current_count = self.current_fan_count
        asked_for_date_of_value = timezone.now() - datetime.timedelta(
            days=days_back)

        try:
            popularity_history_timeseries = self.feed_popularity_set.to_timeseries(
                'fan_count',
                index='date_of_creation')
            first_value = popularity_history_timeseries.iloc[
                -1].name.to_pydatetime()
            last_value = popularity_history_timeseries.iloc[
                0].name.to_pydatetime()

            if (asked_for_date_of_value < first_value) or \
                    (asked_for_date_of_value > last_value) or \
                    (popularity_history_timeseries.count().fan_count <= 1):
                # if history starts after date of request, or there isn't enough data, don't extrapolate.
                fan_count_at_requested_date = 0

            else:
                resampled_history_raw = popularity_history_timeseries.resample(
                    'D')
                if resampled_history_raw.loc[
                    asked_for_date_of_value.date()].isnull().fan_count:
                    # if requested date's data is missing - interpolate from existing data
                    is_interpolated = True
                    resampled_history_interpolated = resampled_history_raw.interpolate()
                    fan_count_at_requested_date = \
                    resampled_history_interpolated.loc[
                        asked_for_date_of_value.date()].fan_count
                else:
                    fan_count_at_requested_date = resampled_history_raw.loc[
                        asked_for_date_of_value.date()].fan_count

            fan_count_dif_nominal = int(
                feed_current_count) - fan_count_at_requested_date
            if fan_count_at_requested_date != 0:
                fan_count_dif_growth_rate = float(
                    fan_count_dif_nominal) / fan_count_at_requested_date
            else:
                fan_count_dif_growth_rate = 0.0

            dif_dict['fan_count_dif_nominal'] = fan_count_dif_nominal
            dif_dict[
                'fan_count_at_requested_date'] = fan_count_at_requested_date
            dif_dict['date_of_value'] = asked_for_date_of_value
            dif_dict['is_interpolated'] = is_interpolated
            dif_dict['fan_count_dif_growth_rate'] = fan_count_dif_growth_rate
        except IndexError:
            dif_dict = dif_dict_default

        finally:
            if return_value == 'all_dict':
                return dif_dict
            else:
                try:
                    return dif_dict[return_value]
                except KeyError:
                    return dif_dict

    @property
    def popularity_dif_week_nominal(self,
                                    days_back=DEFAULT_DAYS_BACK_FOR_POPULARITY_DIF):
        return self.popularity_dif(days_back)['fan_count_dif_nominal']

    @property
    def popularity_dif_week_growth_rate(self,
                                        days_back=DEFAULT_DAYS_BACK_FOR_POPULARITY_DIF):
        return self.popularity_dif(days_back)['fan_count_dif_growth_rate']


class Feed_Popularity(models.Model):
    feed = models.ForeignKey('Facebook_Feed')
    date_of_creation = models.DateTimeField(default=timezone.now)
    # PublicPage Only
    talking_about_count = models.IntegerField(default=0)
    fan_count = models.IntegerField(default=0)
    # UserProfile Only
    followers_count = models.IntegerField(default=0)
    friends_count = models.IntegerField(default=0)

    objects = DataFrameManager()

    class Meta:
        ordering = ['-date_of_creation']
        verbose_name_plural = 'Feed_Popularities'

    def __unicode__(self):
        return slugify(self.feed.name) + " " + str(
            self.date_of_creation.date())
        # strftime("%Y_%M_%D_%H:%m:%s", self.date_of_creation)


class Facebook_Status(models.Model):
    TYPE_CHOICES = (
        (11, 'Group created'),
        (12, 'Event created'),
        (46, 'Status update'),
        (56, 'Post on wall from another user'),
        (66, 'Note created'),
        (80, 'Link posted'),
        (128, 'Video posted'),
        (247, 'Photos posted'),
        (237, 'App story'),
        (257, 'Comment created'),
        (272, 'App story'),
        (285, 'Checkin to a place'),
        (308, 'Post in Group'),
        (0, 'Kikar - missing data')
    )

    feed = models.ForeignKey('Facebook_Feed')
    status_id = models.CharField(unique=True, max_length=128)
    content = models.TextField()
    like_count = models.PositiveIntegerField(default=0, blank=True)
    comment_count = models.PositiveIntegerField(default=0, blank=True)
    share_count = models.PositiveIntegerField(default=0, blank=True)
    published = models.DateTimeField()
    updated = models.DateTimeField()
    status_type = models.CharField(null=True, blank=True, default=None,
                                   max_length=128)
    story = models.TextField(null=True, blank=True)
    story_tags = models.TextField(null=True, blank=True)
    is_comment = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False, null=False)
    locally_updated = models.DateTimeField(blank=True,
                                           default=timezone.datetime(1970, 1,
                                                                     1))

    objects = Facebook_StatusManager()  # Filters out all rows with is_comment=True. Inherits from DataFrame Manager.
    objects_no_filters = DataFrameManager()  # default Manager with DataFrameManager, does not filter out is_comment=True.

    tags = TaggableManager(through=TaggedItem, manager=_KikarTaggableManager)

    def __unicode__(self):
        return self.status_id

    def save(self, *args, **kwargs):
        '''On save, update locally_updated fields'''
        self.locally_updated = timezone.now()
        return super(Facebook_Status, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('status-detail', args=[self.status_id])

    @property
    def get_link(self):
        """
        Returns a link to this post.
        """
        split_status_id = self.status_id.split('_')
        return 'https://www.facebook.com/%s/posts/%s' % (
        split_status_id[0], split_status_id[1])

    @property
    def has_attachment(self):
        try:
            if self.attachment:
                return True
            else:
                return False
        except Exception:
            return False

    @property
    def set_is_comment(self):
        """
        A Method for deciding whether a status is a comment or not, according to the method's logic.
        Returns True or False.
        """
        # Some formatting and printing
        story_string = unidecode(self.story or '')

        # Check for strings indicative of comment activity
        feed_name = unidecode((self.feed and self.feed.name) or '')
        for sp in Status_Comment_Pattern.objects.all():
            pattern = sp.pattern
            try:
                if pattern.format(name=feed_name) in story_string:
                    # print 'Comment:', self, pattern, ':', story_string
                    return True
            except (KeyError, IndexError) as e:
                print 'Format error', self, sp, e
        # print 'Not a comment', self
        return False

    @property
    def needs_refresh(self):
        """Returns whether the status needs a refresh from FB based on its age.
        A status that was just created is updated every 5 seconds, a 2 days old
        status is updated every 10 minutes. Older status don't get updated here
        and they rely on a background process that runs every 10 minutes."""
        now = timezone.now()
        age_secs = max((now - self.published).total_seconds(), 0)
        if age_secs > MAX_STATUS_AGE_FOR_REFRESH:
            return False  # Old status - don't refresh here
        normalized_age = age_secs / MAX_STATUS_AGE_FOR_REFRESH
        refresh_range = MAX_STATUS_REFRESH_INTERVAL - MIN_STATUS_REFRESH_INTERVAL
        refresh_interval = (
                           normalized_age * refresh_range) + MIN_STATUS_REFRESH_INTERVAL
        need_refresh = self.locally_updated + timezone.timedelta(
            seconds=refresh_interval) < now
        # print 'Refresh? %s age=%.3f norm=%.5f int=%.1f updated=%s now=%s' % (
        # need_refresh, age_secs, normalized_age, refresh_interval, self.locally_updated, now)
        return need_refresh

    def suggested_tags(self, n=3):
        my_path = os.path.join(settings.CLASSIFICATION_DATA_ROOT)
        at = autotag.AutoTag(my_path)
        suggestions = at.test_doc({'text': self.content}, at.get_tags(),
                                  DEFAULT_THRESHOLD)
        suggestions_dict = dict((id, percent) for (percent, id) in suggestions)
        tags = Tag.objects.filter(id__in=[sug[1] for sug in suggestions[:]])
        for tag in tags:
            tag.percent = int(suggestions_dict[str(tag.id)] * 100)
        return tags

    class Meta:
        verbose_name_plural = 'Facebook_Statuses'


# status_with_photo = '161648040544835_720225251353775'
# status_with_youtube_link = '161648040544835_723225304387103'
# status_with_link_to_newspaper = '161648040544835_719797924729841'
# status_with_no_multimedia = '161648040544835_718801471496153'

ATTACHMENT_MEDIA_TYPES = (
    ('status', 'Status'),
    ('video', 'Video'),
    ('photo', 'Photo'),
    ('link', 'Link'),
)


# """
#
# https://developers.facebook.com/docs/reference/fql/stream/
#
# The type of this story. Possible values are:
# 11 - Group created
# 12 - Event created
# 46 - Status update    # Relevant
# 56 - Post on wall from another user
# 66 - Note created
# 80 - Link posted     # Relevant
# 128 -Video posted      # Relevant
# 247 - Photos posted     # Relevant
# 237 - App story
# 257 - Comment created
# 272 - App story
# 285 - Checkin to a place
# 308 - Post in Group
# """


class Facebook_Status_Attachment(models.Model):
    status = models.OneToOneField(Facebook_Status, related_name='attachment')
    name = models.TextField(null=True, blank=True)  # name
    caption = models.TextField(null=True, blank=True)  # caption
    description = models.TextField(null=True, blank=True)  # description
    link = models.TextField(null=False)  # link
    facebook_object_id = models.CharField(unique=False, null=True, blank=True,
                                          max_length=128)  # object_id (exists only for internal links)
    type = models.CharField(null=True, blank=True,
                            choices=ATTACHMENT_MEDIA_TYPES,
                            max_length=16)  # type
    picture = models.TextField(null=True, blank=True)  # picture
    source = models.TextField(null=True, blank=True)  # full_size picture
    source_width = models.PositiveSmallIntegerField(null=True, blank=True)
    source_height = models.PositiveSmallIntegerField(null=True, blank=True)

    @property
    def is_internal_link(self):
        return 'https://www.facebook.com/' in self.link


def later():
    return timezone.now() + timezone.timedelta(days=60)


class User_Token(models.Model):
    token = models.CharField(max_length=256, unique=True)
    user_id = models.TextField(unique=True)
    date_of_creation = models.DateTimeField(default=timezone.now)
    date_of_expiration = models.DateTimeField(default=later)
    feeds = models.ManyToManyField(Facebook_Feed, related_name='tokens')

    @property
    def is_expired(self):
        if self.date_of_expiration - timezone.now() <= 0:
            return True
        else:
            return False

    def __unicode__(self):
        return 'token_' + self.user_id


class Status_Comment_Pattern(models.Model):
    pattern = models.CharField(max_length=128)

    def __unicode__(self):
        return self.pattern


# Deprecated Tags
class Tag(models.Model):
    name = models.CharField(unique=True, max_length=128)
    statuses = models.ManyToManyField(Facebook_Status, related_name='old_tags')
    is_for_main_display = models.BooleanField(default=True, null=False)

    def __unicode__(self):
        return self.name

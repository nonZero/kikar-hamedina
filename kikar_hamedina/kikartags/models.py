from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from slugify import slugify as default_slugify

from django.utils.translation import ugettext_lazy as _
from taggit.models import TagBase, GenericTaggedItemBase

from kikartags.managers import TagManager


class Tag(TagBase):
    is_for_main_display = models.BooleanField(default=True, null=False)
    logo = models.ImageField(upload_to='tags_logos', null=True, blank=True)
    is_suggestion = models.BooleanField(default=False, null=False)

    objects = TagManager()

    def __unicode__(self):
        return self.name

    # inherit slugify from TagBase
    def slugify(self, tag, i=None):
        slug = default_slugify(tag)
        if i is not None:
            slug += "_%d" % i
        return slug

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class TaggedItem(GenericTaggedItemBase):
    # TaggedWhatever can also extend TaggedItemBase or a combination of
    # both TaggedItemBase and GenericTaggedItemBase. GenericTaggedItemBase
    # allows using the same tag for different kinds of objects, in this
    # example Food and Drink.
    #
    # # Here is where you provide your custom Tag class.
    tag = models.ForeignKey(Tag,
                            related_name="%(app_label)s_%(class)s_items")
    tagged_by = models.ForeignKey(User, related_name='tagged', null=True, default=None)
    date_of_tagging = models.DateTimeField(null=True, default=timezone.now)

    def __unicode__(self):
        super_str = super(TaggedItem, self).__unicode__()
        return 'User: %s, ' % self.tagged_by + super_str


## Open-Knesset.auxilary.models
class TagSynonym(models.Model):
    tag = models.ForeignKey(Tag, related_name='proper_form_of_tag', unique=True)  # synonym_roper_tag
    proper_form_of_tag = models.ForeignKey(Tag, related_name='synonyms')  # synonym_synonym_tag

    class Meta:
        unique_together = ("tag", "proper_form_of_tag")

    def __unicode__(self):
        return 'Synonym: %s of main tag %s' % (default_slugify(self.tag.name), default_slugify(self.proper_form_of_tag.name))
#
#
# class TagSuggestion(models.Model):
#     name = models.TextField(unique=True)
#     suggested_by = models.ForeignKey(User, verbose_name=_('Suggested by'),
#                                      related_name='tagsuggestion', blank=True,
#                                      null=True)
#     content_type = models.ForeignKey(ContentType)
#     object_id    = models.PositiveIntegerField(db_index=True)
#     object       = generic.GenericForeignKey('content_type', 'object_id')


class HasSynonymError(Exception):
    def __init__(self, message, redirect_url):

        # Call the base class constructor with the parameters it needs
        super(HasSynonymError, self).__init__(message)

        # Now for your custom code...
        self.redirect_url = redirect_url



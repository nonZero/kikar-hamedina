from tastypie import fields
from tastypie.resources import ModelResource, Bundle
from mks.models import Knesset
from facebook_feeds.models import Facebook_Status, Facebook_Feed, Tag as OldTag, User_Token, Feed_Popularity
from kikartags.models import Tag as Tag
from planet.models import Blog
from core.models import MEMBER_MODEL, PARTY_MODEL
from tastypie.constants import ALL, ALL_WITH_RELATIONS


class MemberResource(ModelResource):
    pass


class Facebook_StatusResource(ModelResource):
    pass


def get_resource_uri(obj, field):
    if obj is None:
        return None
    resource = field.get_related_resource(obj)
    return resource.dehydrate_resource_uri(Bundle(obj=obj))


class KikarResource(ModelResource):
    class Meta:
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']


class KnessetResource(ModelResource):
    class Meta:
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        queryset = Knesset.objects.all()
        resource_name = 'knesset'


class PartyResource(ModelResource):
    knesset = fields.ForeignKey(KnessetResource, 'knesset', null=True, blank=True)
    all_members = fields.ManyToManyField(MemberResource, 'all_members', null=True, blank=True)

    class Meta:
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        queryset = PARTY_MODEL.objects.all()
        resource_name = 'party'


class Facebook_FeedResource(ModelResource):
    owner = fields.ToOneField(MemberResource, attribute='owner', null=True)

    class Meta:
        queryset = Facebook_Feed.objects.all()
        resource_name = 'facebook_feed'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']

    def dehydrate_owner(self, bundle):
        persona = bundle.obj.persona
        if persona is not None:
            return get_resource_uri(persona.owner, self.owner)
        return None


class MemberResource(ModelResource):
    current_party = fields.ForeignKey(PartyResource, 'current_party', null=True, blank=True)
    if hasattr(MEMBER_MODEL, 'parties'):
        parties = fields.ManyToManyField(PartyResource, 'parties')
    main_feed = fields.ToOneField(Facebook_FeedResource, attribute='main_feed', null=True)

    class Meta:
        queryset = MEMBER_MODEL.objects.all()
        resource_name = 'member'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']

    def dehydrate_main_feed(self, bundle):
        persona = bundle.obj.facebook_persona
        if persona is not None:
            return get_resource_uri(persona.get_main_feed, self.main_feed)
        return None


class TagResource(ModelResource):
    statuses = fields.ManyToManyField(Facebook_StatusResource, 'statuses', null=True)

    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']


class Facebook_StatusResource(ModelResource):
    feed = fields.ForeignKey(Facebook_FeedResource, 'feed')
    tags = fields.ManyToManyField(TagResource, 'tags')

    class Meta:
        queryset = Facebook_Status.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'facebook_status'
        filtering = {
            "status_id": ["exact"],
            "feed": ["exact"],
            "content": ["exact", "startswith", "contains"],
            "published": ['exact', 'gt', 'gte', 'lt', 'lte', 'range']
        }

    def dehydrate(self, bundle):
        bundle.data['facebook_link'] = bundle.obj.get_link
        bundle.data['member'] = bundle.obj.feed.persona.owner.name
        bundle.data['party'] = bundle.obj.feed.persona.owner.current_party.name
        if bundle.obj.has_attachment:
            bundle.data['attachment'] = "Attachment"
        return bundle

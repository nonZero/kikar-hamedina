# encoding: utf-8

from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.utils import timezone

from django.db.models import Q

from csv import DictWriter
from facebook_feeds.models import Facebook_Feed, Facebook_Status


class Command(BaseCommand):
    help = "helper script that calculates top statuses for candidates, and writes them into a csv file. Work in progress"
    # args = '<file_name>'

    def save_data_to_csv(self, histogram, field_names, file_name):
        print 'Output file name:', file_name
        f = open('data_for_mary_-_%s.csv' % file_name, 'wb')

        csv_data = DictWriter(f, field_names)
        headers = {field_name: field_name for field_name in field_names}
        csv_data.writerow(headers)

        for feed, result in histogram:
            row_keys = field_names
            row_values = [feed.persona.owner.name,
                          feed.persona.owner.current_party.name,
                          feed.id,
                          feed.name,
                          feed.link,
                          feed.current_fan_count,
                          result]
            csv_data.writerow({x[0]: unicode(x[1]).encode('utf-8') for x in zip(row_keys, row_values)})

        f.close()

    def calculate_and_save_data_for_keyword(self, range_qs, joined_q_objects, file_name):
        filterd_qs = range_qs.filter(joined_q_objects)

        histogram = []

        for feed in Facebook_Feed.objects.filter(is_current=True):
            statuses = filterd_qs.filter(feed__id=feed.id)
            count = statuses.count()
            histogram.append(
                (feed, count),
            )

        histogram = sorted(histogram, key=lambda x: x[1], reverse=True)

        field_names = ['member',
                       'party',
                       'feed_id',
                       'feed_name',
                       'facebook_link',
                       'like_count',
                       u'num_of_statuses_with_terms'
                       ]

        self.save_data_to_csv(histogram, field_names, file_name)

    def handle(self, *args, **options):

        print 'Start.'
        start_time = timezone.datetime(2014, 9, 01, 0, 0, 0, 0, tzinfo=timezone.get_current_timezone())
        end_time = timezone.datetime(2015, 8, 31, 23, 59, 0, 0, tzinfo=timezone.get_current_timezone())

        range_qs = Facebook_Status.objects.filter(published__range=(start_time, end_time))

        # Shkifut
        print 'doing shkifut'
        STR_SEARCH_TERMS = [u'שקיפות', ]
        q_objects = [Q(content__icontains=x) for x in STR_SEARCH_TERMS]
        joined_q_objects = q_objects[0]  # | q_objects[1] | q_objects[2]
        self.calculate_and_save_data_for_keyword(range_qs, joined_q_objects, file_name='shkifut')
        # Hasadna
        print 'doing shkifut'
        STR_SEARCH_TERMS = [u'כנסת פתוחה', u'לידע ציבורי', u'מפתח התקציב', u'תקציב פתוח', u'התקציב הפתוח']
        q_objects = [Q(content__icontains=x) for x in STR_SEARCH_TERMS]
        joined_q_objects = q_objects[0] | q_objects[1] | q_objects[2] | q_objects[3] | q_objects[4]
        self.calculate_and_save_data_for_keyword(range_qs, joined_q_objects, file_name='hasadna_terms')
        # Democracy
        print 'doing Democracy'
        STR_SEARCH_TERMS = [u'דמוקרטיה', ]
        q_objects = [Q(content__icontains=x) for x in STR_SEARCH_TERMS]
        joined_q_objects = q_objects[0]
        self.calculate_and_save_data_for_keyword(range_qs, joined_q_objects, file_name='democracy')
        # all
        print 'doing all'
        joined_q_objects = Q()
        self.calculate_and_save_data_for_keyword(range_qs, joined_q_objects, file_name='total')

        print 'Done.'

from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.utils import timezone
from csv import DictWriter
from facebook_feeds.models import Facebook_Feed


class Command(BaseCommand):
    help = "helper script that calculates top statuses for candidates, and writes them into a csv file. Work in progress"

    def handle(self, *args, **options):

        print 'Start.'

        feed_history_data = list()
        start_date = timezone.datetime(2014, 10, 25, 0, 0, 0, 0, tzinfo=timezone.get_current_timezone())
        for feed in Facebook_Feed.objects.all():
            for pop in feed.feed_popularity_set.order_by('date_of_creation').filter(date_of_creation__gte=start_date):
                feed_history_data.append({
                    'feed_id': feed.id,
                    'feed_name': getattr(feed.persona.owner, 'name', None),
                    'feed_type': feed.feed_type,
                    'date': pop.date_of_creation.strftime("%Y-%m-%d %T"),
                    'fan_count': pop.fan_count,
                    'talking_about_count': getattr(pop, 'talking_about_count', -1)
                })

        print 'num of rows:', len(feed_history_data)

        field_names = ['feed_id',
                       'feed_name',
                       'feed_type',
                       'date',
                       'fan_count',
                       'talking_about_count'
        ]

        file_name = 'data_for_hadas'
        print 'Output file name:', file_name
        f = open('%s.csv' % file_name, 'wb')

        csv_data = DictWriter(f, field_names)
        headers = {field_name: field_name for field_name in field_names}
        csv_data.writerow(headers)

        for row in feed_history_data:
            row_keys = field_names
            row_values = row.values()
            csv_data.writerow({x[0]: unicode(x[1]).encode('utf-8') for x in zip(row_keys, row_values)})

        f.close()
        print 'Done.'
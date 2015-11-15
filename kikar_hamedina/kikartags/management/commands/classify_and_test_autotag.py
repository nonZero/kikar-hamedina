from random import shuffle, sample
from optparse import make_option

from django.core.management.base import BaseCommand
from django.db.models import Count
from django.conf import settings

from autotag_app import autotag as autotag
# from autotag import autotag as autotag

from facebook_feeds.models import Facebook_Status
from kikartags.models import Tag
from kikartags.utils import build_classifier_format

NUM_OF_NEGATIVE_OR_POSITIVE_STATUSES = 100
MINIMAL_NUM_OF_POSITIVE_STATUSES_FOR_TRAIN = 50
MINIMAL_NUM_OF_POSITIVE_STATUSES_FOR_TEST = 10

TOTAL_TRAIN = 100
TOTAL_TEST = 100

CLASSIFICATION_DATA_PATH = settings.CLASSIFICATION_DATA_ROOT


class Command(BaseCommand):
    help = "Train the classifier for a given tag id."
    args = '<tag_id>'

    option_list = BaseCommand.option_list + (
        make_option('-e',
                    '--all-eligible',
                    action='store_true',
                    dest='all_eligible',
                    default=False,
                    help='When flag is set to True, runs on all eligible tags for classification'),
    )

    def get_all_tags_above_threshold(self):
        return Tag.objects.annotate(num_of_statuses=Count('kikartags_taggeditem_items')).filter(
            num_of_statuses__gte=MINIMAL_NUM_OF_POSITIVE_STATUSES_FOR_TEST + MINIMAL_NUM_OF_POSITIVE_STATUSES_FOR_TRAIN).order_by(
            '-num_of_statuses')

    def create_groups_for_test_and_train(self, tag_id):

        # Prepare positive data:

        positive_statuses = Facebook_Status.objects.filter(tagged_items__tag__id=tag_id)
        print 'num of postive statuses:', positive_statuses.count()
        if positive_statuses.count() < MINIMAL_NUM_OF_POSITIVE_STATUSES_FOR_TRAIN + MINIMAL_NUM_OF_POSITIVE_STATUSES_FOR_TEST:
            raise Exception('Not enough positive statuses.')

        positive_status_data = [build_classifier_format(x) for x in positive_statuses]
        shuffle(positive_status_data)

        if positive_status_data > MINIMAL_NUM_OF_POSITIVE_STATUSES_FOR_TRAIN * 2:
            positive_status_data = positive_status_data[:(MINIMAL_NUM_OF_POSITIVE_STATUSES_FOR_TRAIN * 2) + 1]

        train_positive_statuses = positive_status_data[:MINIMAL_NUM_OF_POSITIVE_STATUSES_FOR_TRAIN]
        test_positive_statuses = positive_status_data[MINIMAL_NUM_OF_POSITIVE_STATUSES_FOR_TRAIN:]

        print 'train_positive_statuses: %s, test_positive_statuses: %s' % (
            len(train_positive_statuses), len(test_positive_statuses))

        # prepare negative data:

        missing_train = TOTAL_TRAIN - len(train_positive_statuses)
        missing_test = TOTAL_TEST - len(test_positive_statuses)

        status_ids = [x[0] for x in Facebook_Status.objects.filter(tagged_items__isnull=False).exclude(
            tagged_items__tag__id=tag_id).values_list('status_id')]
        rand_ids = sample(status_ids, missing_train + missing_test)
        negative_statuses = Facebook_Status.objects.filter(status_id__in=rand_ids)

        negative_statuses_data = [build_classifier_format(x) for x in negative_statuses[:missing_test + missing_train]]

        train_statuses = train_positive_statuses + negative_statuses_data[:missing_train]
        test_statuses = test_positive_statuses + negative_statuses_data[missing_train:]

        print 'train_statuses: %s, test_statuses: %s' % (len(train_statuses), len(test_statuses))

        if len(train_statuses + test_statuses) < MINIMAL_NUM_OF_POSITIVE_STATUSES_FOR_TRAIN:
            raise Exception('Not enough statuses: %d' % len(train_statuses + test_statuses))

        return train_statuses, test_statuses

    def handle(self, *args, **options):
        print 'start.'
        # all_statuses = Facebook_Status.objects.filter(tagged_items__isnull=False).order_by('?')
        # train_statuses = all_statuses[0:int(math.floor(all_statuses.count() / 2.0))]
        # test_statuses = all_statuses[int(math.floor(all_statuses.count() / 2.0)):]
        # print all_statuses.count()


        if options['all_eligible']:
            for x in self.get_all_tags_above_threshold():
                print x.id, x.num_of_statuses
            tag_ids = [x.id for x in self.get_all_tags_above_threshold()]
        else:
            if len(args) == 0:
                raise Exception('Missing Tag ID')
            elif len(args) > 1:
                raise Exception('Too many Tag IDs')

            tag_ids = [args[0]]
        print 'tag_ids:', tag_ids

        for tag_id in tag_ids:
            train_statuses, test_statuses = self.create_groups_for_test_and_train(tag_id)
            at = autotag.AutoTag(CLASSIFICATION_DATA_PATH)
            print 'start training.'
            at.classify(train_statuses, MINIMAL_NUM_OF_POSITIVE_STATUSES_FOR_TRAIN, tags=[tag_id])
            print 'finished classifying! Start testing'

            a = at.test(test_statuses, [str(tag_id)])
        print a
        print 'done.'


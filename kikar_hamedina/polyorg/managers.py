import difflib
from django.core.cache import cache
from django.db import models


class KnessetManager(models.Manager):
    """This is a manager for Knesset class"""

    def __init__(self):
        super(KnessetManager, self).__init__()
        self._current_knesset = None

    def current_knesset(self):
        if self._current_knesset is None:
            try:
                self._current_knesset = self.get_queryset().order_by('-number')[0]
            except IndexError:
                #FIX: should document when and why this should happen
                return None
        return self._current_knesset


class BetterManager(models.Manager):
    def __init__(self):
        super(BetterManager, self).__init__()
        self._names = []

    def find(self, name):
        ''' looks for a member with a name that resembles 'name'
            the returned array is ordered by similiarity
        '''
        names = cache.get('%s_names' % self.model.__name__)
        if not names:
            names = self.values_list('name', flat=True)
            cache.set('%s_names' % self.model.__name__, names)
        possible_names = difflib.get_close_matches(
            name, names, cutoff=0.5, n=5)
        qs = self.filter(name__in=possible_names)
        # used to establish size, overwritten later
        ret = range(qs.count())
        for m in qs:
            if m.name == name:
                return [m]
            ret[possible_names.index(m.name)] = m
        return ret


class CurrentKnessetCandidateListManager(models.Manager):

    def __init__(self):
        super(CurrentKnessetCandidateListManager, self).__init__()
        self._current = None

    def get_queryset(self):
        # caching won't help here, as the query set will be re-run on each
        # request, and we may need to further run queries down the road
        from polyorg.models import ElectedKnesset
        qs = super(CurrentKnessetCandidateListManager, self).get_queryset()
        qs = qs.filter(knesset=ElectedKnesset.objects.current_knesset())
        return qs

    @property
    def current_candidate_lists(self):
        if self._current is None:
            self._current = list(self.get_queryset())

        return self._current


class CurrentKnessetCandidatesManager(models.Manager):
    "Adds the ability to filter on current knesset"

    def get_queryset(self):
        from mks.models import Knesset
        qs = super(CurrentKnessetCandidatesManager, self).get_queryset()
        qs = qs.filter(candidates_list__knesset=Knesset.objects.current_knesset())
        return qs

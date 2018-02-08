# coding: utf-8
import math
from functools import reduce

from django.core.paginator import Paginator, QuerySetPaginator, Page, InvalidPage

__all__ = ('DiggPaginator',)


class ExPaginator(Paginator):
    """Adds a ``softlimit`` option to ``page()``. If True, querying a
    page number larger than max. will not fail, but instead return the
    last available page.

    This is useful when the data source can not provide an exact count
    at all times (like some search engines), meaning the user could
    possibly see links to invalid pages at some point which we wouldn't
    want to fail as 404s.
    """

    def _ensure_int(self, num, e):
        print(num)
        # see Django #7307
        try:
            return int(num)
        except ValueError:
            raise e

    def page(self, number, softlimit=False):
        try:
            return super(ExPaginator, self).page(number)
        except InvalidPage as e:
            number = self._ensure_int(number, e)
            if number > self.num_pages and softlimit:
                return self.page(self.num_pages, softlimit=False)
            else:
                raise e


class DiggPaginator(ExPaginator):
    """
    Based on Django's default paginator, it adds "Digg-style" page ranges
    with a leading block of pages, an optional middle block, and another
    block at the end of the page range.
    """

    def __init__(self, *args, **kwargs):
        self.body = kwargs.pop('body', 10)
        self.tail = kwargs.pop('tail', 2)

        print(self.body, self.tail)
        self.align_left = kwargs.pop('align_left', False)
        self.margin = kwargs.pop('margin', 4)  # TODO: make the default relative to body?
        # validate padding value
        max_padding = int(math.ceil(self.body / 2.0) - 1)
        self.padding = kwargs.pop('padding', min(4, max_padding))
        if self.padding > max_padding:
            raise ValueError('padding too large for body (max %d)' % max_padding)
        super(DiggPaginator, self).__init__(*args, **kwargs)

    def page(self, number, *args, **kwargs):
        """Return a standard ``Page`` instance with custom, digg-specific
        page ranges attached.
        """

        page = super(DiggPaginator, self).page(number, *args, **kwargs)
        number = int(number)  # we know this will work

        # easier access
        num_pages, body, tail, padding, margin = \
            self.num_pages, self.body, self.tail, self.padding, self.margin

        # put active page in middle of main range
        main_range = list(map(int, [
            math.floor(number - body / 2.0) + 1,  # +1 = shift odd body to right
            math.floor(number + body / 2.0)]))
        # adjust bounds
        if main_range[0] < 1:
            main_range = list(map(abs(main_range[0] - 1).__add__, main_range))
        if main_range[1] > num_pages:
            main_range = list(map((num_pages - main_range[1]).__add__, main_range))

        if main_range[0] <= tail + margin:
            leading = []
            main_range = [1, max(body, min(number + padding, main_range[1]))]
            main_range[0] = 1
        else:
            leading = range(1, tail + 1)
        # basically same for trailing range, but not in ``left_align`` mode
        if self.align_left:
            trailing = []
        else:
            if main_range[1] >= num_pages - (tail + margin) + 1:
                trailing = []
                if not leading:
                    # ... but handle the special case of neither leading nor
                    # trailing ranges; otherwise, we would now modify the
                    # main range low bound, which we just set in the previous
                    # section, again.
                    main_range = [1, num_pages]
                else:
                    main_range = [min(num_pages - body + 1, max(number - padding, main_range[0])), num_pages]
            else:
                trailing = range(num_pages - tail + 1, num_pages + 1)

        # finally, normalize values that are out of bound; this basically
        # fixes all the things the above code screwed up in the simple case
        # of few enough pages where one range would suffice.
        main_range = [max(main_range[0], 1), min(main_range[1], num_pages)]

        # make the result of our calculations available as custom ranges
        # on the ``Page`` instance.
        page.main_range = range(main_range[0], main_range[1] + 1)
        page.leading_range = leading
        page.trailing_range = trailing
        page.page_range = reduce(lambda x, y: x + ((x and y) and [False]) + y,
                                 [list(page.leading_range), list(page.main_range), list(page.trailing_range)])

        page.__class__ = DiggPage
        return page


class DiggPage(Page):
    def __str__(self):
        return " ... ".join(filter(None, [
            " ".join(list(map(str, self.leading_range))),
            " ".join(list(map(str, self.main_range))),
            " ".join(list(map(str, self.trailing_range)))]))


class QuerySetDiggPaginator(DiggPaginator, QuerySetPaginator):
    pass

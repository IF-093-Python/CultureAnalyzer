from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

DEFAULT_PAGE = 1


class SafePaginator(Paginator):

    def page(self, number):
        page_number = DEFAULT_PAGE
        try:
            page_number = int(number)
        except (PageNotAnInteger, ValueError):
            pass
        except EmptyPage:
            if number > 1:
                page_number = self.num_pages
        return super(SafePaginator, self).page(page_number)

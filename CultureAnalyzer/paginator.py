from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

__all__ = ['SafePaginator', ]

DEFAULT_PAGE = 1


class SafePaginator(Paginator):

    def page(self, number):
        page_number = DEFAULT_PAGE
        try:
            page_number = int(number)
            self.validate_number(page_number)
        except (PageNotAnInteger, ValueError):
            pass
        except EmptyPage:
            if page_number > 1:
                page_number = self.num_pages
            else:
                page_number = DEFAULT_PAGE
        return super(SafePaginator, self).page(page_number)

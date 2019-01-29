from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class SafePaginator(Paginator):

    def page(self, number):
        try:
            number = int(number)
            return super(SafePaginator, self).page(number)
        except (PageNotAnInteger, ValueError):
            return self.page(1)
        except EmptyPage:
            if number > 1:
                return self.page(self.num_pages)
            else:
                return self.page(1)

from django.views.generic import ListView

from CultureAnalyzer.paginator import SafePaginator

__all__ = ['SafePaginationListView', ]


class SafePaginationListView(ListView):
    paginator_class = SafePaginator

    def paginate_queryset(self, queryset, page_size):
        """Removed page validation from view"""
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = paginator.page(
            self.kwargs.get(page_kwarg) or self.request.GET.get(
                page_kwarg) or 1)
        return paginator, page, page.object_list, page.has_other_pages()

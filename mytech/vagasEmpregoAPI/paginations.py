
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'perpage'
    page_query_param = 'page'
    max_page_size = 100

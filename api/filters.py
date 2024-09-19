from rest_framework import filters


class ComfortableOrderingFilter(filters.OrderingFilter):
    def __init__(self, *args, **kwargs):
        self.ordering_fields = {
            'default': '-created_at',
            'username': 'user__username',
            'email': 'user__email',
            '-username': '-user__username',
            '-email': '-user__email',
            'created': 'created_at',
            'updated': 'updated_at', 
            '-updated': '-updated_at'
        }
        super().__init__(*args, **kwargs)


    def get_ordering(self, request, *args, **kwargs):
        ordering = request.query_params.get('ordering', None)
        if ordering:
            return [self.ordering_fields.get(o, o) for o in ordering.split(',')]
        
        return None

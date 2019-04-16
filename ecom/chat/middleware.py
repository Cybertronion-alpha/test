import datetime
from django.core.cache import cache
from django.conf import settings

from accounts.models import GenralData


class ActiveUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = datetime.datetime.now()
            current_user = request.user
            
            cache.set('last_seen_%s' % current_user.username, now,
                    settings.USER_LASTSEEN_TIMEOUT)
        response = self.get_response(request)
        return response

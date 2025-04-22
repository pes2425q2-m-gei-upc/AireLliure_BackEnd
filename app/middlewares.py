from django.conf import settings

from .utils import (
    actualitzar_activitats_culturals,
    actualitzar_estacions_qualitat_aire,
    actualitzar_rutes,
)


class ActualitzarRutes:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not getattr(settings, "DISABLE_AUTO_UPDATE", False):
            actualitzar_rutes()
        return self.get_response(request)


class ActualitzarEstacionsQualitatAire:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not getattr(settings, "DISABLE_AUTO_UPDATE", False):
            actualitzar_estacions_qualitat_aire()
        return self.get_response(request)


class ActualitzarActivitatsCulturals:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not getattr(settings, "DISABLE_AUTO_UPDATE", False):
            actualitzar_activitats_culturals()
        return self.get_response(request)

from .utils import actualitzar_rutes, actualitzar_estacions_qualitat_aire, actualitzar_activitats_culturals

class ActualitzarRutes:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        actualitzar_rutes()  # Se ejecuta en cada request si es necesario
        return self.get_response(request)

class ActualitzarEstacionsQualitatAire:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        actualitzar_estacions_qualitat_aire()  # Se ejecuta en cada request si es necesario
        return self.get_response(request)

class ActualitzarActivitatsCulturals:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        actualitzar_activitats_culturals()  # Se ejecuta en cada request si es necesario
        return self.get_response(request)
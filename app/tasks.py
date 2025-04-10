from celery import shared_task
from .utils import actualitzar_rutes, actualitzar_estacions_qualitat_aire, actualitzar_activitats_culturals

@shared_task
def tasca_actualitzar_rutes():
    actualitzar_rutes()
    print("Rutes actualitzades.")

@shared_task
def tasca_actualitzar_estacions_qualitat_aire():
    actualitzar_estacions_qualitat_aire()
    print("Estacions de qualitat d'aire actualitzades.")

# @shared_task
# def tasca_actualitzar_activitats_culturals():
#     actualitzar_activitats_culturals()
#     print("Activitats culturals actualitzades.")
# pylint: disable=W0718, C0303
from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    host = "https://airelliure-backend.onrender.com"
    wait_time = between(1, 2)

    @task
    def on_start(self):
        try:
            response = self.client.post(
                "/login/",
                json={
                    "correu": "aguilera@example.com",
                    "password": "ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f",
                },
            )
            if response.status_code == 200:
                print("Login exitoso")
            else:
                print(f"Error en login: {response.status_code}")
        except Exception as e:
            print(f"Error completo: {str(e)}")

    @task
    def test_categories(self):
        response = self.client.get("/categories/")
        if response.status_code != 200:
            print(f"Error en categories: {response.status_code}")

    @task
    def test_dificultats(self):
        response = self.client.get("/dificultats-esportiva/")
        if response.status_code != 200:
            print(f"Error endifficulties: {response.status_code}")

    @task
    def test_dificultats_by_pk(self):
        response = self.client.get("/dificultats-esportiva/Baja/")
        if response.status_code != 200:
            print(f"Error endifficulties: {response.status_code}")

    @task
    def test_accessibilitats(self):
        response = self.client.get("/accessibilitats-respiratoria/")
        if response.status_code != 200:
            print(f"Error en accessibilitats: {response.status_code}")

    @task
    def test_accessibilitats_by_pk(self):
        response = self.client.get("/accessibilitats-respiratoria/Moderada/")
        if response.status_code != 200:
            print(f"Error en accessibilitats: {response.status_code}")

    @task
    def test_usuaris(self):
        response = self.client.get("/usuaris/")
        if response.status_code != 200:
            print(f"Error en usuaris: {response.status_code}")

    @task
    def get_all_deshabilitat(self):
        response = self.client.get("/deshabilitats/")
        if response.status_code != 200:
            print(f"Error en deshabilitats: {response.status_code}")

    @task
    def get_all_habilitats(self):
        response = self.client.get("/habilitats/")
        if response.status_code != 200:
            print(f"Error en habilitats: {response.status_code}")

    @task
    def get_usuari_by_pk(self):
        response = self.client.get("/usuaris/aguilera@example.com/")
        if response.status_code != 200:
            print(f"Error en usuari: {response.status_code}")

    @task
    def get_amdins(self):
        response = self.client.get("/admins/")
        if response.status_code != 200:
            print(f"Error en amdins: {response.status_code}")

    @task
    def get_amdins_by_pk(self):
        response = self.client.get("/admins/aguilera@example.com/")
        if response.status_code != 200:
            print(f"Error en amdins: {response.status_code}")

    @task
    def get_all_bloqueigs(self):
        response = self.client.get("/bloqueigs/")
        if response.status_code != 200:
            print(f"Error en bloqueigs: {response.status_code}")

    @task
    def get_all_amistats(self):
        response = self.client.get("/amistats/")
        if response.status_code != 200:
            print(f"Error en amistats: {response.status_code}")

    @task
    def get_all_rutes(self):
        response = self.client.get("/rutas/")
        if response.status_code != 200:
            print(f"Error en rutas: {response.status_code}")

    @task
    def get_ruta_by_pk(self):
        response = self.client.get("/rutas/615851413/")
        if response.status_code != 200:
            print(f"Error en ruta: {response.status_code}")

    @task
    def get_info_ruta(self):
        response = self.client.get("/rutas/615851413/info/")
        if response.status_code != 200:
            print(f"Error en ruta: {response.status_code}")

    @task
    def get_presencies(self):
        response = self.client.get("/presencies/")
        if response.status_code != 200:
            print(f"Error en presencies: {response.status_code}")

    @task
    def get_index_qualitat_aire(self):
        response = self.client.get("index-qualitat-aire-taula/")
        if response.status_code != 200:
            print(f"Error en index qualitat aire: {response.status_code}")

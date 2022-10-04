# Bar

Cette API créée avec Django REST nous permet de gérer le fonctionnement d'un bar.
D'une part du côté consommateur avec le menu ainsi que les commandes, d'autre part les employés peuvent gérer les 
stocks, références et commandes.


## Installation et lancement avec git :

```bash
$ git clone https://github.com/TheHarryPop/Bar.git
$ cd EPIC_Events
$ python3 -m venv env (Sous Windows => python -m venv env)
$ source env/bin/activate (Sous Windows => env\Scripts\activate)
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

## Endpoints :

Ci-dessous, la liste des endpoints disponibles.

- http://127.0.0.1:8000/admin
  - *You have to create a superuser with commande ```python manage.py createsuperuser```*

- http://127.0.0.1:8000/api/login/


- http://127.0.0.1:8000/api/signup/


- http://127.0.0.1:8000/api/bars/
  - **get** : IsAuthenticated


- http://127.0.0.1:8000/api/bar/{{bar_id}}/
  - **get** : Is_staff
  - **post** : Is_staff
  - **put** : Is_staff
  - **delete** : Is_staff


- http://127.0.0.1:8000/api/references/
  - **get** : IsAuthenticated/Is_staff


- http://127.0.0.1:8000/api/reference/{{reference_id}}/
  - **get** : Is_staff
  - **post** : Is_staff
  - **put** : Is_staff
  - **delete** : Is_staff


- http://127.0.0.1:8000/api/stock/{{bar_id}}/
  - **get** : IsAuthenticated


- http://127.0.0.1:8000/api/menu/
  - **get** : AlloyAny


- http://127.0.0.1:8000/api/menu/{{bar_id}}/
  - **get** : AlloyAny


- http://127.0.0.1:8000/api/orders/
  - **get** : IsAuthenticated


- http://127.0.0.1:8000/api/order/{{order_id}}/
  - **get** : IsAuthenticated
  - **post** : Anonymous


- http://127.0.0.1:8000/api/bars/ranking/*
  - **get** : IsAuthenticated


- http://127.0.0.1:8000/api/orders/bars/ranking
  - **get** : IsAuthenticated

## Filtres de recherche :

Ci-dessous la liste des filtres disponibles pour chaque URL.

- http://127.0.0.1:8000/api/bars/?{{value=}} : 'name'
- http://127.0.0.1:8000/api/bars/?{{value=}} : 'ref', 'name', 'description'
- http://127.0.0.1:8000/api/menu/?{{value=}} : 'ref', 'name', 'description'

## Tri de recherche :

Ci-dessous la liste des tris disponibles pour chaque URL.

- http://127.0.0.1:8000/api/bars/?ordering= : 'name'
- http://127.0.0.1:8000/api/bars/?ordering= : 'ref', 'name', 'description'
- http://127.0.0.1:8000/api/menu/?ordering= : 'ref', 'name', 'description'

## Pagination :

Le nombre maximum de résultats affichés par page est de cinq. Ce paramètre est modifiable dans le fichier 
```Bar/CovageDRF/settings.py```

## Tests :

Les tests sont stockés dans le dossier ```Bar/tests```.

Commande de lancement :
```bash 
$ pytest
```
Les tests sont paramétrés dans le fichier ```Bar/pytest.ini```, et réalisés avec des fixtures stockées dans le fichier 
```Bar/tests/conftest.py```.

### Liste des tests :
- test_barview.py :
  - test 'get' bars avec utilisateur connecté : *test_get_bar_auth*
  - test 'get' bars avec utilisateur non connecté : *test_get_bar_no_auth*
  - test 'post' bar avec utilisateur staff : *test_post_bar_is_staff*
  - test 'post' bar avec utilisateur connecté : *test_post_bar_user*
  - test 'put' bar avec utilisateur staff : *test_put_bar_is_staff*
  - test 'put' bar avec utilisateur connecté : *test_put_bar_user*
  

- test_orderview.py :
  - test 'get' orders avec utilisateur connecté : *test_get_orders_auth*
  - test 'get' orders avec utilisateur non connecté : *test_get_orders_no_auth*
  - test 'retrieve' order avec utilsateur connecté : *test_retrieve_order_details_auth*
  - test 'retrieve' order avec utilsateur non connecté : *test_retrieve_order_details_no_auth*
  - test 'post' order avec utiliateur connecté : *test_post_order_details_auth*
  - test 'post' order avec utiliateur non connecté : *test_post_order_details_no_auth*
  - test affichage message si stock inférieur à 2 bières : *test_low_stock*
  

- test_rankingview.py :
  - test 'get' bars ranking avec utilisateur connecté : *test_get_ranking_auth*
  - test 'get' bars ranking avec utilisateur non connecté : *test_get_ranking_no_auth*
  - test 'get' orders bars ranking avec utilisateur connecté : *test_get_ranking_orders_auth*
  - test 'get' orders bars ranking avec utilisateur non connecté : *test_get_ranking_orders_no_auth*


- test_referenceview.py :
  - test 'get' reference avec utilisateur connecté : *test_get_ref_auth*
  - test 'get' reference avec utilisateur non connecté : *test_get_ref_no_auth*
  - test 'post' reference avec utilisateur staff : *test_post_ref_is_staff*
  - test 'post' reference avec utilisateur connecté : *test_post_ref_user*
  - test 'put' reference avec utilisateur staff : *test_put_ref_is_staff*
  - test 'put' reference avec utilisateur connecté : *test_put_ref_user*
  - test 'delete' reference = 'delete' stock : *test_delete_ref_in_stock*


- test_stockview.py :
  - test 'retrieve' stock avec utilisateur connecté : *test_retrieve_stock_auth*
  - test 'retrieve' stock avec utilisateur non connecté : *test_retrieve_stock_no_auth*


- test_userview.py :
  - test register user : *test_register_user*
  - test login user : *test_login_user*
  - test login user with wrong password : *test_login_user__wrong_password*

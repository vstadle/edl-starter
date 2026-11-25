"""
Tests API TaskFlow - TP 1

Apprenez en faisant ! Ce fichier vous montre comment écrire des tests, puis vous en écrirez de similaires.

Structure de chaque test :
1. ARRANGE - Préparer les données de test
2. ACT - Faire la requête API
3. ASSERT - Vérifier la réponse
"""

import pytest


# =============================================================================
# PARTIE 1 : TESTS EXEMPLES (Apprenez de ceux-ci !)
# =============================================================================

def test_root_endpoint(client):
    """
    EXEMPLE : Tester un point de terminaison GET simple.

    Ce test vous montre le pattern de base :
    1. Faire une requête avec client.get()
    2. Vérifier le code de statut
    3. Vérifier les données de la réponse
    """
    # ACT : Faire une requête GET
    response = client.get("/")

    # ASSERT : Vérifier la réponse
    assert response.status_code == 200
    assert "Welcome to TaskFlow API" in response.json()["message"]


def test_health_check(client):
    """EXEMPLE : Un autre test de point de terminaison GET simple."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_task(client):
    """
    EXEMPLE : Tester un point de terminaison POST (création de données).

    Pattern pour les requêtes POST :
    1. Préparer les données comme un dictionnaire Python
    2. Les envoyer avec client.post()
    3. Vérifier le code de statut (201 = Créé)
    4. Vérifier les données retournées
    """
    # ARRANGE : Préparer les données
    new_task = {
        "title": "Acheter des courses",
        "description": "Lait, œufs, pain"
    }

    # ACT : Envoyer la requête POST
    response = client.post("/tasks", json=new_task)

    # ASSERT : Vérifier la réponse
    assert response.status_code == 201  # 201 = Créé

    task = response.json()
    assert task["title"] == "Acheter des courses"
    assert task["description"] == "Lait, œufs, pain"
    assert task["status"] == "todo"  # Valeur par défaut
    assert "id" in task  # Le serveur génère un ID


def test_list_tasks(client):
    """
    EXEMPLE : Tester GET avec préparation de données.

    Parfois vous devez créer des données d'abord, puis tester leur listage.
    """
    # ARRANGE : Créer quelques tâches d'abord
    client.post("/tasks", json={"title": "Tâche 1"})
    client.post("/tasks", json={"title": "Tâche 2"})

    # ACT : Obtenir la liste des tâches
    response = client.get("/tasks")

    # ASSERT : Vérifier qu'on a bien les deux tâches
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2


def test_get_task_by_id(client):
    """
    EXEMPLE : Tester GET pour une ressource spécifique.

    Pattern :
    1. Créer une tâche d'abord
    2. Obtenir son ID depuis la réponse
    3. Utiliser cet ID pour récupérer la tâche
    """
    # ARRANGE : Créer une tâche
    create_response = client.post("/tasks", json={"title": "Trouve-moi"})
    task_id = create_response.json()["id"]

    # ACT : Obtenir la tâche spécifique
    response = client.get(f"/tasks/{task_id}")

    # ASSERT : Vérifier qu'on a la bonne tâche
    assert response.status_code == 200
    assert response.json()["title"] == "Trouve-moi"


# =============================================================================
# PARTIE 2 : À VOUS ! (Exercices 1 et 2)
# =============================================================================
#
# Écrivez d'abord ces tests : ils échouent, car delete_task() et update_task()
# ne sont pas encore écrites dans src/app.py. Puis écrivez ces fonctions
# jusqu'à ce que les tests passent.
#
# Pour chaque test : supprimez la ligne pytest.fail(...), puis écrivez
# ARRANGE / ACT / ASSERT. La docstring dit ce qu'il faut vérifier.

# --- Exercice 1 : supprimer une tâche ---

def test_delete_task(client):
    """Supprimer une tâche existante renvoie 204, puis la tâche n'existe plus (GET → 404)."""

    create_response = client.post("/tasks", json={"title": "À supprimer"})
    task_id = create_response.json()["id"]

    # ARRANGE
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200

    # ACT
    delete_response = client.delete(f"/tasks/{task_id}")

    # ASSERT
    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_task(client):
    """Supprimer une tâche qui n'existe pas renvoie 404."""

    # ARRANGE
    nonexistent_id = 9999

    # ACT
    delete_response = client.delete(f"/tasks/{nonexistent_id}")

    # ASSERT
    assert delete_response.status_code == 404


# --- Exercice 2 : modifier une tâche ---

def test_update_task_title(client):
    """Modifier le titre d'une tâche renvoie 200 et la tâche avec le nouveau titre."""
    create_response = client.post("/tasks", json={"title": "Ancien titre"})
    task_id = create_response.json()["id"]

    # ARRANGE
    update_data = {"title": "Nouveau titre"}

    # ACT
    update_response = client.put(f"/tasks/{task_id}", json=update_data)

    # ASSERT
    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["title"] == "Nouveau titre"


def test_update_only_changes_sent_fields(client):
    """Créez une tâche avec un titre, une description et une priorité,
    puis envoyez seulement {"status": "done"} : le statut change,
    mais le titre, la description et la priorité restent identiques."""
    create_response = client.post("/tasks", json={
        "title": "Tâche à modifier",
        "description": "Description initiale",
        "priority": "medium"
    })
    task_id = create_response.json()["id"]

    # ARRANGE
    update_data = {"status": "done"}

    # ACT
    update_response = client.put(f"/tasks/{task_id}", json=update_data)

    # ASSERT
    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["status"] == "done"
    assert updated_task["title"] == "Tâche à modifier"
    assert updated_task["description"] == "Description initiale"
    assert updated_task["priority"] == "medium"


def test_update_nonexistent_task(client):
    """Modifier une tâche qui n'existe pas renvoie 404."""
    # ARRANGE
    nonexistent_id = 9999
    update_data = {"title": "Nouveau titre"}

    # ACT
    update_response = client.put(f"/tasks/{nonexistent_id}", json=update_data)

    # ASSERT
    assert update_response.status_code == 404


# =============================================================================
# PARTIE 3 : À VOUS ! (Exercice 3)
# =============================================================================
#
# Écrivez ces tests. Pour chacun : supprimez la ligne pytest.fail(...),
# puis écrivez ARRANGE / ACT / ASSERT. La docstring dit ce qu'il faut vérifier.

def test_create_task_with_empty_title(client):
    """Créer une tâche avec un titre vide ("") est refusé : 422."""
    
    # ARRANGE
    new_task = {"title": ""}

    # ACT
    response = client.post("/tasks", json=new_task)

    # ASSERT
    assert response.status_code == 422


def test_get_nonexistent_task(client):
    """Demander une tâche qui n'existe pas renvoie 404."""

    # ARRANGE
    nonexistent_id = 9999

    # ACT
    response = client.get(f"/tasks/{nonexistent_id}")

    # ASSERT
    assert response.status_code == 404


def test_update_task_with_invalid_priority(client):
    """Mettre à jour une tâche avec priority="urgent" est refusé : 422.
    (Les priorités valides sont "low", "medium" et "high".)"""

    # ARRANGE
    new_task = {"title": "Tâche à modifier", "priority": "urgent"}

    # ACT
    response = client.post("/tasks", json=new_task)

    # ASSERT
    assert response.status_code == 422


def test_filter_tasks_by_status(client):
    """Créez une tâche "todo" et une tâche "done" : GET /tasks?status=done
    ne renvoie qu'une seule tâche, celle qui est terminée."""

    # ARRANGE
    todo_task = {"title": "Tâche à faire", "status": "todo"}
    done_task = {"title": "Tâche terminée", "status": "done"}

    client.post("/tasks", json=todo_task)
    client.post("/tasks", json=done_task)

    # ACT
    response = client.get("/tasks?status=done")

    # ASSERT
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["status"] == "done"


# =============================================================================
# BONUS (si vous avez fini)
# =============================================================================
#
# Supprimez la ligne @pytest.mark.skip(...) pour activer un test.

def test_filter_by_status_and_priority(client):
    """GET /tasks?status=todo&priority=high combine les deux filtres."""

    # ARRANGE
    client.post("/tasks", json={"title": "À faire, urgente", "status": "todo", "priority": "high"})
    client.post("/tasks", json={"title": "À faire, pas urgente", "status": "todo", "priority": "low"})
    client.post("/tasks", json={"title": "Terminée, urgente", "status": "done", "priority": "high"})

    # ACT
    response = client.get("/tasks?status=todo&priority=high")

    # ASSERT
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "À faire, urgente"


def test_create_task_with_title_too_long(client):
    """Le titre est limité à 200 caractères : 200 est accepté (201), 201 est refusé (422).
    Astuce : "a" * 200 crée un texte de 200 caractères."""

    # ARRANGE
    title_200 = "a" * 200
    title_201 = "a" * 201

    # ACT
    response_200 = client.post("/tasks", json={"title": title_200})
    response_201 = client.post("/tasks", json={"title": title_201})

    # ASSERT
    assert response_200.status_code == 201
    assert response_201.status_code == 422


# --- Bonus TDD : recherche par titre ---

def test_search_tasks_by_title(client):
    """GET /tasks?search=rapport renvoie les tâches dont le titre contient
    « rapport », sans tenir compte des majuscules."""

    # ARRANGE
    client.post("/tasks", json={"title": "Rapport mensuel"})
    client.post("/tasks", json={"title": "Relire le RAPPORT de stage"})
    client.post("/tasks", json={"title": "Faire les courses"})

    # ACT
    response = client.get("/tasks?search=rapport")

    # ASSERT
    assert response.status_code == 200
    titles = [task["title"] for task in response.json()]
    assert titles == ["Rapport mensuel", "Relire le RAPPORT de stage"]


# --- Bonus parametrize : plusieurs priorités invalides en un seul test ---

@pytest.mark.parametrize("priority", ["urgent", "", "HIGH"])
def test_create_task_with_invalid_priority(client, priority):
    """Créer une tâche avec une priorité invalide qui doit être refusé : 422."""

    # ARRANGE
    new_task = {"title": "Tâche", "priority": priority}

    # ACT
    response = client.post("/tasks", json=new_task)

    # ASSERT
    assert response.status_code == 422


# --- Bonus couverture à 100 % ---

def test_filter_tasks_by_assignee(client):
    """GET /tasks?assignee=... ne renvoie que les tâches de cette personne."""

    # ARRANGE
    client.post("/tasks", json={"title": "Tâche de Toto", "assignee": "toto@toto.com"})
    client.post("/tasks", json={"title": "Tâche de Donald", "assignee": "donald@duck.com"})

    # ACT
    response = client.get("/tasks?assignee=toto@toto.com")

    # ASSERT
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["assignee"] == "toto@toto.com"


def test_create_task_with_whitespace_title(client):
    """Un titre fait seulement d'espaces est refusé par le code : 422."""

    # ARRANGE
    new_task = {"title": "   "}

    # ACT
    response = client.post("/tasks", json=new_task)

    # ASSERT
    assert response.status_code == 422


# =============================================================================
# ASTUCES & CONSEILS
# =============================================================================

"""
PATTERNS COURANTS :

1. Tester POST (Créer) :
   response = client.post("/tasks", json={"title": "..."})
   assert response.status_code == 201

2. Tester GET (Lire) :
   response = client.get("/tasks")
   assert response.status_code == 200

3. Tester PUT (Mettre à jour) :
   response = client.put(f"/tasks/{id}", json={"title": "..."})
   assert response.status_code == 200

4. Tester DELETE (Supprimer) :
   response = client.delete(f"/tasks/{id}")
   assert response.status_code == 204

5. Tester les erreurs de validation :
   response = client.post("/tasks", json={"bad": "data"})
   assert response.status_code == 422

6. Tester les erreurs 404 (la ressource demandée n'existe pas) :
   assert response.status_code == 404

CODES DE STATUT COURANTS :
- 200 : OK (GET/PUT réussi)
- 201 : Créé (POST réussi)
- 204 : Pas de Contenu (DELETE réussi)
- 404 : Non Trouvé (la ressource n'existe pas)
- 422 : Erreur de Validation (données invalides)

RAPPELEZ-VOUS :
- La fixture `client` est automatiquement fournie par conftest.py
- Les tâches sont automatiquement effacées avant/après chaque test (fixture clean_tasks)
- Les tests doivent être indépendants (ne pas dépendre d'autres tests)
"""

# =============================================================================
# TEST E2E
# =============================================================================
@pytest.mark.e2e
def test_complete_task_lifecycle(client):
    """Test E2E : Créer plusieurs tâches et les lister."""
    # Créer la première tâche
    response = client.post("/tasks", json={
        "title": "Tâche E2E 1",
        "description": "Première tâche"
    })
    assert response.status_code == 201
    task1_id = response.json()["id"]

    # Créer la deuxième tâche
    response = client.post("/tasks", json={
        "title": "Tâche E2E 2",
        "description": "Deuxième tâche"
    })
    assert response.status_code == 201
    task2_id = response.json()["id"]

    # Lister toutes les tâches
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 2

    # Vérifier que nos deux tâches sont dans la liste
    task_ids = [task["id"] for task in tasks]
    assert task1_id in task_ids
    assert task2_id in task_ids

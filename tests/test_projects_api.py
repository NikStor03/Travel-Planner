import respx
from httpx import Response

AIC_BASE = "https://api.artic.edu/api/v1"

def test_create_project_with_places_success(client):
    with respx.mock:
        respx.get(f"{AIC_BASE}/artworks/27992").mock(
            return_value=Response(200, json={"data": {"id": 27992, "title": "Nighthawks"}})
        )

        resp = client.post("/projects", json={
            "name": "My Trip",
            "places": [{"external_id": 27992, "notes": "Must see"}]
        })

    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "My Trip"
    assert len(data["places"]) == 1
    assert data["places"][0]["external_id"] == 27992
    assert data["places"][0]["notes"] == "Must see"
    assert data["completed"] is False

def test_create_project_with_nonexistent_place_fails(client):
    with respx.mock:
        respx.get(f"{AIC_BASE}/artworks/999999999").mock(
            return_value=Response(404, json={"detail": "Not found"})
        )

        resp = client.post("/projects", json={
            "name": "Bad Trip",
            "places": [{"external_id": 999999999}]
        })

    assert resp.status_code == 400
    assert "not found" in resp.json()["detail"].lower()

def test_project_places_limit_max_10(client):
    with respx.mock:
        # mock all 11 ids as existing
        for i in range(1, 12):
            respx.get(f"{AIC_BASE}/artworks/{i}").mock(
                return_value=Response(200, json={"data": {"id": i, "title": f"Art {i}"}})
            )

        resp = client.post("/projects", json={
            "name": "Too Many",
            "places": [{"external_id": i} for i in range(1, 12)]
        })

    assert resp.status_code == 400
    assert "more than 10" in resp.json()["detail"].lower() or "between" in resp.json()["detail"].lower()

def test_delete_project_blocked_if_any_place_visited(client):
    # create project
    with respx.mock:
        respx.get(f"{AIC_BASE}/artworks/1").mock(
            return_value=Response(200, json={"data": {"id": 1, "title": "Art 1"}})
        )
        create = client.post("/projects", json={"name": "Trip", "places": [{"external_id": 1}]})
    pid = create.json()["id"]
    place_id = create.json()["places"][0]["id"]

    # mark place visited
    patch = client.patch(f"/projects/{pid}/places/{place_id}", json={"visited": True})
    assert patch.status_code == 200
    assert patch.json()["visited"] is True

    # try delete
    delete = client.delete(f"/projects/{pid}")
    assert delete.status_code == 409

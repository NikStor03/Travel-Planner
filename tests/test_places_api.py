import respx
from httpx import Response

AIC_BASE = "https://api.artic.edu/api/v1"

def test_add_place_to_existing_project(client):
    with respx.mock:
        respx.get(f"{AIC_BASE}/artworks/10").mock(
            return_value=Response(200, json={"data": {"id": 10, "title": "Art 10"}})
        )
        created = client.post("/projects", json={"name": "Trip"})
    pid = created.json()["id"]

    with respx.mock:
        respx.get(f"{AIC_BASE}/artworks/11").mock(
            return_value=Response(200, json={"data": {"id": 11, "title": "Art 11"}})
        )
        resp = client.post(f"/projects/{pid}/places", json={"external_id": 11, "notes": "Later"})
    assert resp.status_code == 201
    assert resp.json()["external_id"] == 11

def test_prevent_duplicate_external_place_in_project(client):
    with respx.mock:
        respx.get(f"{AIC_BASE}/artworks/20").mock(
            return_value=Response(200, json={"data": {"id": 20, "title": "Art 20"}})
        )
        created = client.post("/projects", json={"name": "Trip", "places": [{"external_id": 20}]})
    pid = created.json()["id"]

    with respx.mock:
        respx.get(f"{AIC_BASE}/artworks/20").mock(
            return_value=Response(200, json={"data": {"id": 20, "title": "Art 20"}})
        )
        resp = client.post(f"/projects/{pid}/places", json={"external_id": 20})
    assert resp.status_code in (409, 400)
    assert "already" in resp.json()["detail"].lower()

def test_project_completed_when_all_places_visited(client):
    # create with 2 places
    with respx.mock:
        respx.get(f"{AIC_BASE}/artworks/1").mock(return_value=Response(200, json={"data": {"id": 1, "title": "A1"}}))
        respx.get(f"{AIC_BASE}/artworks/2").mock(return_value=Response(200, json={"data": {"id": 2, "title": "A2"}}))
        created = client.post("/projects", json={"name": "Trip", "places": [{"external_id": 1}, {"external_id": 2}]})

    pid = created.json()["id"]
    p1, p2 = created.json()["places"][0]["id"], created.json()["places"][1]["id"]

    # visit first
    client.patch(f"/projects/{pid}/places/{p1}", json={"visited": True})
    proj_mid = client.get(f"/projects/{pid}").json()
    assert proj_mid["completed"] is False

    # visit second -> project becomes completed
    client.patch(f"/projects/{pid}/places/{p2}", json={"visited": True})
    proj_done = client.get(f"/projects/{pid}").json()
    assert proj_done["completed"] is True
    assert proj_done["completed_at"] is not None

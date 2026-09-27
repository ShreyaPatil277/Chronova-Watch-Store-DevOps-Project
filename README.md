# Chronova — Premium Watch Store ⭐

An end-to-end DevOps demo project: a small e-commerce watch store with a complete CI/CD pipeline from source code to a running, monitored deployment.

**Repository:** https://github.com/ShreyaPatil277/Chronova-Watch-Store-DevOps-Project

---

## Pipeline Overview

```
Developer → GitHub → Jenkins → Build & Test → Docker Image → Deployment → Monitoring
```

| Stage | Tool | What happens |
|---|---|---|
| Source control | GitHub | Code, Dockerfile, and Jenkinsfile are version controlled on the `main` branch |
| CI/CD | Jenkins (2.568.3 LTS) | Pipeline job automatically checks out code, installs dependencies, runs tests, builds a Docker image, and deploys a new container |
| Containerization | Docker (Engine 29.x) | App is packaged into a `chronova-watch-store` image using a `python:3.11-slim` base |
| Deployment | Docker (via Jenkins) | Jenkins runs the freshly built image as `chronova-watch-store-container`, exposed on port `5001` |
| Monitoring | `docker stats` / `docker logs` | Live CPU/memory usage and request logs for the running container |

---

## Tech Stack

- **Backend:** Python 3, Flask
- **Database:** SQLite (file-based, seeded automatically on first run)
- **Frontend:** Server-rendered HTML/CSS/JS (Jinja2 templates), cart state via browser `localStorage`
- **Testing:** pytest
- **CI/CD:** Jenkins (Declarative Pipeline)
- **Containerization:** Docker

---

## Application Features

- **Storefront (`/`)** — displays watches with product photos, brand, name, and price in ₹ (INR)
- **Cart (`/cart`)** — add/remove items, adjust quantities, view running total, demo checkout button
- **REST API:**
  - `GET /watches` — list all watches
  - `GET /watches/<id>` — get one watch
  - `POST /watches` — add a new watch
  - `POST /orders` — place an order
  - `GET /health` — health check endpoint used for monitoring

---

## Project Structure

```
chronova-watch-store/
├── app.py                 # Flask application (routes, DB logic)
├── requirements.txt        # Python dependencies
├── test_app.py             # pytest test suite
├── templates/
│   ├── index.html           # Storefront page
│   └── cart.html            # Shopping cart page
├── Dockerfile               # Container build definition
├── .dockerignore             # Excludes local db/venv from image
├── .gitignore                 # Excludes local db/venv from Git
└── Jenkinsfile                 # CI/CD pipeline definition
```

---

## Running It Yourself

### 1. Clone the repo
```bash
git clone https://github.com/ShreyaPatil277/Chronova-Watch-Store-DevOps-Project.git
cd Chronova-Watch-Store-DevOps-Project
```

### 2. Run locally (without Docker)
```bash
python -m venv venv
source venv/bin/activate      # venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
pytest
python app.py
```
Visit `http://localhost:5000/`

### 3. Run with Docker
```bash
docker build -t chronova-watch-store:latest .
docker run -d --name chronova-container -p 5000:5000 chronova-watch-store:latest
```
Visit `http://localhost:5000/`

### 4. Run the full CI/CD pipeline (Jenkins)
```bash
docker volume create jenkins_home

docker run -d --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v //var/run/docker.sock:/var/run/docker.sock \
  -u root \
  jenkins/jenkins:2.568.3-lts-jdk21
```
1. Open `http://localhost:8080` and complete the setup wizard
2. Create a Pipeline job named `chronova-watch-store-pipeline`
3. Point it at this repo's GitHub URL, branch `main`, script path `Jenkinsfile`
4. Click **Build Now**

Once the build succeeds, the app is live at `http://localhost:5001/`

---

## Monitoring Commands

```bash
docker stats chronova-watch-store-container   # live CPU/memory
docker logs -f chronova-watch-store-container # live request logs
curl http://localhost:5001/health             # health check
```

---

## Pipeline Diagram

```
Developer --> GitHub (Chronova-Watch-Store-DevOps-Project)
    --> Jenkins (Build & Test) --> Docker Image (chronova-watch-store)
    --> Deployment (auto-run container on port 5001)
    --> Monitoring (docker stats / docker logs)
```

---

*This is a student DevOps demo project. Product images are used for illustrative/UI purposes only.*

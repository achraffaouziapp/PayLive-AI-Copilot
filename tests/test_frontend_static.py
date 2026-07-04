from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = BASE_DIR / "frontend"


def test_frontend_files_exist():
    expected_files = [
        FRONTEND_DIR / "index.html",
        FRONTEND_DIR / "css" / "styles.css",
        FRONTEND_DIR / "js" / "app.js",
        FRONTEND_DIR / "Dockerfile",
        FRONTEND_DIR / "nginx.conf",
    ]

    for file_path in expected_files:
        assert file_path.exists(), f"Fichier manquant : {file_path}"


def test_index_contains_required_sections():
    index_path = FRONTEND_DIR / "index.html"
    content = index_path.read_text(encoding="utf-8")

    required_texts = [
        "PayLive AI Copilot",
        "Configuration API",
        "Prédiction d’intention",
        "Informations modèle",
        "Métriques modèle",
        "Monitoring IA",
        "commentText",
        "predictBtn",
        "modelInfoBtn",
        "modelMetricsBtn",
        "openDashboardBtn",
        "downloadAlertsBtn",
    ]

    for text in required_texts:
        assert text in content, f"Élément attendu absent dans index.html : {text}"


def test_javascript_calls_ai_api_routes():
    js_path = FRONTEND_DIR / "js" / "app.js"
    content = js_path.read_text(encoding="utf-8")

    required_routes = [
        "/predict-intent",
        "/model-info",
        "/model-metrics",
        "/monitoring/dashboard",
        "/monitoring/alerts",
    ]

    for route in required_routes:
        assert route in content, f"Route API IA absente du JavaScript : {route}"

    assert "X-API-Key" in content
    assert "localStorage" in content
    assert "is_low_confidence" in content


def test_css_contains_responsive_and_accessibility_rules():
    css_path = FRONTEND_DIR / "css" / "styles.css"
    content = css_path.read_text(encoding="utf-8")

    required_rules = [
        "@media",
        "max-width",
        "grid-template-columns: 1fr",
        "button:hover",
        "overflow: auto",
        "word-break",
    ]

    for rule in required_rules:
        assert rule in content, f"Règle CSS attendue absente : {rule}"


def test_nginx_proxies_api_and_health():
    nginx_path = FRONTEND_DIR / "nginx.conf"
    content = nginx_path.read_text(encoding="utf-8")

    assert "proxy_pass http://api:8000/health" in content
    assert "proxy_pass http://api:8000/api/" in content
    assert "try_files $uri $uri/ /index.html" in content


def test_frontend_dockerfile_uses_nginx():
    dockerfile_path = FRONTEND_DIR / "Dockerfile"
    content = dockerfile_path.read_text(encoding="utf-8")

    assert "FROM nginx" in content
    assert "COPY index.html" in content
    assert "COPY css" in content
    assert "COPY js" in content
    assert "COPY nginx.conf" in content
    assert "EXPOSE 80" in content

def test_api_key_validation_uses_protected_route():
    js_path = FRONTEND_DIR / "js" / "app.js"
    content = js_path.read_text(encoding="utf-8")

    assert "/model-info" in content
    assert "Clé API invalide" in content
    assert "response.status === 403" in content
    assert "fetch(\"/health\")" not in content
const config = {
  apiBaseUrl: localStorage.getItem("paylive_api_base_url") || "/api/v1/ai",
  apiKey: localStorage.getItem("paylive_api_key") || "paylive-dev-api-key",
};

const apiBaseUrlInput = document.getElementById("apiBaseUrl");
const apiKeyInput = document.getElementById("apiKey");
const connectionStatus = document.getElementById("connectionStatus");

const commentText = document.getElementById("commentText");
const predictionResult = document.getElementById("predictionResult");
const predictedIntent = document.getElementById("predictedIntent");
const confidenceScore = document.getElementById("confidenceScore");
const responseTime = document.getElementById("responseTime");
const modelVersion = document.getElementById("modelVersion");
const lowConfidenceMessage = document.getElementById("lowConfidenceMessage");

const modelInfoOutput = document.getElementById("modelInfoOutput");
const modelMetricsOutput = document.getElementById("modelMetricsOutput");
const monitoringStatus = document.getElementById("monitoringStatus");

apiBaseUrlInput.value = config.apiBaseUrl;
apiKeyInput.value = config.apiKey;

function getHeaders() {
  return {
    "Content-Type": "application/json",
    "X-API-Key": apiKeyInput.value.trim(),
  };
}

function getApiBaseUrl() {
  return apiBaseUrlInput.value.trim().replace(/\/$/, "");
}

function formatJson(data) {
  return JSON.stringify(data, null, 2);
}

function showError(target, error) {
  target.textContent = `Erreur : ${error.message}`;
  target.style.color = "#b91c1c";
}

document.getElementById("saveConfigBtn").addEventListener("click", () => {
  localStorage.setItem("paylive_api_base_url", getApiBaseUrl());
  localStorage.setItem("paylive_api_key", apiKeyInput.value.trim());

  connectionStatus.textContent = "Configuration enregistrée.";
  connectionStatus.style.color = "#047857";
});

document.getElementById("healthBtn").addEventListener("click", async () => {
  try {
    connectionStatus.textContent = "Test de connexion sécurisée en cours...";
    connectionStatus.style.color = "#111827";

    const response = await fetch(`${getApiBaseUrl()}/model-info`, {
      method: "GET",
      headers: getHeaders(),
    });

    if (response.status === 401) {
      throw new Error("Clé API absente.");
    }

    if (response.status === 403) {
      throw new Error("Clé API invalide.");
    }

    if (!response.ok) {
      throw new Error(`Connexion refusée : ${response.status}`);
    }

    await response.json();

    connectionStatus.textContent = "API IA disponible et clé API valide.";
    connectionStatus.style.color = "#047857";
  } catch (error) {
    showError(connectionStatus, error);
  }
});

document.getElementById("predictBtn").addEventListener("click", async () => {
  const text = commentText.value.trim();

  if (!text) {
    alert("Veuillez saisir un commentaire.");
    return;
  }

  try {
    predictionResult.classList.add("hidden");

    const response = await fetch(`${getApiBaseUrl()}/predict-intent`, {
      method: "POST",
      headers: getHeaders(),
      body: JSON.stringify({
        comment_text: text,
      }),
    });

    if (!response.ok) {
      throw new Error(`Erreur API : ${response.status}`);
    }

    const data = await response.json();

    predictedIntent.textContent = data.predicted_intent || "-";
    confidenceScore.textContent =
      data.confidence_score !== undefined
        ? Number(data.confidence_score).toFixed(4)
        : "-";
    responseTime.textContent =
      data.response_time_ms !== undefined
        ? `${Number(data.response_time_ms).toFixed(2)} ms`
        : "-";
    modelVersion.textContent = data.model_version || "-";

    if (data.is_low_confidence === true) {
      lowConfidenceMessage.classList.remove("hidden");
    } else {
      lowConfidenceMessage.classList.add("hidden");
    }

    predictionResult.classList.remove("hidden");
  } catch (error) {
    alert(error.message);
  }
});

document.getElementById("clearBtn").addEventListener("click", () => {
  commentText.value = "";
  predictionResult.classList.add("hidden");
  lowConfidenceMessage.classList.add("hidden");
});

document.getElementById("modelInfoBtn").addEventListener("click", async () => {
  try {
    modelInfoOutput.textContent = "Chargement...";

    const response = await fetch(`${getApiBaseUrl()}/model-info`, {
      headers: getHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Erreur API : ${response.status}`);
    }

    const data = await response.json();
    modelInfoOutput.textContent = formatJson(data);
  } catch (error) {
    modelInfoOutput.textContent = error.message;
  }
});

document.getElementById("modelMetricsBtn").addEventListener("click", async () => {
  try {
    modelMetricsOutput.textContent = "Chargement...";

    const response = await fetch(`${getApiBaseUrl()}/model-metrics`, {
      headers: getHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Erreur API : ${response.status}`);
    }

    const data = await response.json();
    modelMetricsOutput.textContent = formatJson(data);
  } catch (error) {
    modelMetricsOutput.textContent = error.message;
  }
});

document.getElementById("openDashboardBtn").addEventListener("click", async () => {
  try {
    monitoringStatus.textContent = "Ouverture du dashboard...";
    monitoringStatus.style.color = "#111827";

    const response = await fetch(`${getApiBaseUrl()}/monitoring/dashboard`, {
      headers: {
        "X-API-Key": apiKeyInput.value.trim(),
      },
    });

    if (!response.ok) {
      throw new Error(`Erreur API : ${response.status}`);
    }

    const html = await response.text();
    const blob = new Blob([html], { type: "text/html" });
    const url = URL.createObjectURL(blob);

    window.open(url, "_blank");

    monitoringStatus.textContent = "Dashboard ouvert dans un nouvel onglet.";
    monitoringStatus.style.color = "#047857";
  } catch (error) {
    showError(monitoringStatus, error);
  }
});

document.getElementById("downloadAlertsBtn").addEventListener("click", async () => {
  try {
    monitoringStatus.textContent = "Téléchargement des alertes...";
    monitoringStatus.style.color = "#111827";

    const response = await fetch(`${getApiBaseUrl()}/monitoring/alerts`, {
      headers: {
        "X-API-Key": apiKeyInput.value.trim(),
      },
    });

    if (!response.ok) {
      throw new Error(`Erreur API : ${response.status}`);
    }

    const csv = await response.text();
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "model_monitoring_alerts.csv";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    monitoringStatus.textContent = "Alertes téléchargées.";
    monitoringStatus.style.color = "#047857";
  } catch (error) {
    showError(monitoringStatus, error);
  }
});
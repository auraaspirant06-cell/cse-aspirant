/**
 * CSE Aspirant - Web Dashboard Main Controller
 */
import { api } from "./api.js";
import { webPlayer } from "./player.js";
import { updateMetricCard, renderKeyBadge } from "./components.js";

async function refreshMetrics() {
  try {
    const data = await api.fetchOverview();
    updateMetricCard("val-streams", data.active_audio_players);
    updateMetricCard("val-commands", data.counters.commands_total || 0);
    updateMetricCard("val-cpu", `${data.system_resources.cpu_percent}%`);
    updateMetricCard("val-mem", `${data.system_resources.memory_used_mb} MB`);
  } catch (e) {
    console.warn("Metrics polling offline / backend loading");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  refreshMetrics();
  setInterval(refreshMetrics, 3000);

  const btnStream = document.getElementById("btn-stream");
  const streamInput = document.getElementById("stream-input") as HTMLInputElement;
  const statusBar = document.getElementById("player-status-bar");

  btnStream?.addEventListener("click", async () => {
    if (!streamInput?.value) return;
    if (statusBar) statusBar.textContent = "Processing audio stream...";
    const res = await webPlayer.triggerPlay(123456, streamInput.value);
    if (statusBar) statusBar.textContent = res;
    streamInput.value = "";
  });

  const btnGenKey = document.getElementById("btn-gen-key");
  const keyDisplay = document.getElementById("key-display");

  btnGenKey?.addEventListener("click", async () => {
    if (keyDisplay) keyDisplay.textContent = "Generating NextGen key...";
    const res = await api.generateApiKey(987654, "PRO");
    if (res.data?.key && keyDisplay) {
      keyDisplay.innerHTML = renderKeyBadge(res.data.key);
    }
  });
});


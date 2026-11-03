/**
 * CSE Aspirant - Web Dashboard API Client
 */
export interface SystemOverview {
  counters: Record<string, number>;
  active_audio_players: number;
  system_resources: {
    uptime_seconds: number;
    cpu_percent: number;
    memory_percent: number;
    memory_used_mb: number;
  };
}

export class DashboardAPI {
  private baseUrl = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
  private apiKey = import.meta.env.VITE_API_KEY || "";

  private headers(): Record<string, string> {
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (this.apiKey) {
      headers["X-API-Key"] = this.apiKey;
    }
    return headers;
  }

  async fetchOverview(): Promise<SystemOverview> {
    const res = await fetch(`${this.baseUrl}/api/v1/analytics/overview`);
    const json = await res.json();
    return json.data;
  }

  async playTrack(chatId: number, query: string): Promise<any> {
    const res = await fetch(`${this.baseUrl}/api/v1/music/play`, {
      method: "POST",
      headers: this.headers(),
      body: JSON.stringify({ chat_id: chatId, query_or_url: query, requester_id: 1 })
    });
    return res.json();
  }

  async generateApiKey(userId: number, tier: string = "PRO"): Promise<any> {
    const res = await fetch(`${this.baseUrl}/api/v1/keys/generate`, {
      method: "POST",
      headers: this.headers(),
      body: JSON.stringify({ user_id: userId, tier })
    });
    return res.json();
  }
}

export const api = new DashboardAPI();


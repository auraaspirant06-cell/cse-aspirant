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

  private async parseResponse<T>(res: Response): Promise<T> {
    const json = await res.json();
    if (!res.ok) {
      throw new Error(json.detail || json.message || `Request failed with HTTP ${res.status}`);
    }
    return json;
  }

  async fetchOverview(): Promise<SystemOverview> {
    const res = await fetch(`${this.baseUrl}/api/v1/analytics/overview`, {
      headers: this.headers()
    });
    const json = await this.parseResponse<{ data: SystemOverview }>(res);
    return json.data;
  }

  async playTrack(chatId: number, query: string): Promise<any> {
    const res = await fetch(`${this.baseUrl}/api/v1/music/play`, {
      method: "POST",
      headers: this.headers(),
      body: JSON.stringify({ chat_id: chatId, query_or_url: query, requester_id: 1 })
    });
    return this.parseResponse(res);
  }

  async generateApiKey(userId: number, tier: string = "PRO"): Promise<any> {
    const res = await fetch(`${this.baseUrl}/api/v1/keys/generate`, {
      method: "POST",
      headers: this.headers(),
      body: JSON.stringify({ user_id: userId, tier })
    });
    return this.parseResponse(res);
  }
}

export const api = new DashboardAPI();


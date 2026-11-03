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
  private baseUrl = "http://localhost:8000";

  async fetchOverview(): Promise<SystemOverview> {
    const res = await fetch(`${this.baseUrl}/api/v1/analytics/overview`);
    const json = await res.json();
    return json.data;
  }

  async playTrack(chatId: number, query: string): Promise<any> {
    const res = await fetch(`${this.baseUrl}/api/v1/music/play`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-API-Key": "CSE_ASPIRANT_OWNER_KEY" },
      body: JSON.stringify({ chat_id: chatId, query_or_url: query, requester_id: 1 })
    });
    return res.json();
  }

  async generateApiKey(userId: number, tier: string = "PRO"): Promise<any> {
    const res = await fetch(`${this.baseUrl}/api/v1/keys/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-API-Key": "CSE_ASPIRANT_OWNER_KEY" },
      body: JSON.stringify({ user_id: userId, tier })
    });
    return res.json();
  }
}

export const api = new DashboardAPI();


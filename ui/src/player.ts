/**
 * CSE Aspirant - Web Player Controls
 */
import { api } from "./api.js";

export class WebPlayerController {
  async triggerPlay(chatId: number, query: string): Promise<string> {
    try {
      const res = await api.playTrack(chatId, query);
      return res.message || "Track queued.";
    } catch (err) {
      return `Playback failed: ${err}`;
    }
  }
}

export const webPlayer = new WebPlayerController();


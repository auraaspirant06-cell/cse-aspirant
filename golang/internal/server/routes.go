package server

import (
	"encoding/json"
	"net/http"
	"cse-aspirant/golang/internal/audio"
	"cse-aspirant/golang/internal/errorhandling"
)

type ServerHandler struct {
	transcoder *audio.Transcoder
	streamer   *audio.AudioStreamer
}

func NewServerHandler() *ServerHandler {
	return &ServerHandler{
		transcoder: audio.NewTranscoder(),
		streamer:   audio.NewAudioStreamer(),
	}
}

func (h *ServerHandler) HealthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(map[string]interface{}{
		"status":         "healthy",
		"service":        "cse_aspirant_go_engine",
		"active_workers": 8,
		"version":        "2.0.0",
	})
}

func (h *ServerHandler) StreamHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return
	}

	var req struct {
		URL    string `json:"url"`
		Format string `json:"format"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, `{"error":"invalid_payload"}`, http.StatusBadRequest)
		return
	}

	res, err := h.transcoder.Process(req.URL, req.Format)
	if err != nil {
		errResp := errorhandling.NewEngineError("TRANSCODE_FAIL", err.Error())
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusInternalServerError)
		_ = json.NewEncoder(w).Encode(errResp)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(res)
}

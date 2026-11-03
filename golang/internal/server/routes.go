package server

import (
	"crypto/rand"
	"fmt"
	"encoding/json"
	"net/http"
	"net/url"
	"os"
	"strconv"
	"strings"
	"encoding/hex"
	"cse-aspirant/golang/internal/audio"
	"cse-aspirant/golang/internal/errorhandling"
)

type ServerHandler struct {
	transcoder *audio.Transcoder
	streamer   *audio.AudioStreamer
	publicURL  string
	token      string
}

func NewServerHandler() *ServerHandler {
	return &ServerHandler{
		transcoder: audio.NewTranscoder(),
		streamer:   audio.NewAudioStreamer(),
		publicURL:  strings.TrimRight(os.Getenv("GO_ENGINE_PUBLIC_URL"), "/"),
		token:      os.Getenv("GO_ENGINE_TOKEN"),
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

	if !h.authorized(r) {
		http.Error(w, `{"error":"unauthorized"}`, http.StatusUnauthorized)
		return
	}

	var req struct {
		URL    string `json:"url"`
		Format string `json:"format"`
		Position int `json:"position"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, `{"error":"invalid_payload"}`, http.StatusBadRequest)
		return
	}

	if req.Position < 0 {
		http.Error(w, `{"error":"invalid_position"}`, http.StatusBadRequest)
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

	publicURL := h.publicURL
	if publicURL == "" {
		publicURL = "http://localhost:8080"
	}
	streamID, err := newStreamID()
	if err != nil {
		http.Error(w, `{"error":"stream_id_generation_failed"}`, http.StatusInternalServerError)
		return
	}
	if _, err := h.streamer.OpenStream(streamID, req.URL); err != nil {
		http.Error(w, `{"error":"invalid_stream_url"}`, http.StatusBadRequest)
		return
	}
	streamURL := fmt.Sprintf("%s/api/v1/stream/audio?id=%s&position=%d", publicURL, url.QueryEscape(streamID), req.Position)
	res.StreamURL = streamURL
	res.StreamID = streamID
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(res)
}

func (h *ServerHandler) AudioHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return
	}
	streamID := r.URL.Query().Get("id")
	session, ok := h.streamer.GetStream(streamID)
	if !ok {
		http.Error(w, `{"error":"stream_not_found"}`, http.StatusNotFound)
		return
	}
	defer h.streamer.CloseStream(streamID)
	position, err := strconv.Atoi(r.URL.Query().Get("position"))
	if err != nil {
		position = 0
	}
	if err := h.streamer.Stream(r.Context(), w, session.URL, position); err != nil {
		return
	}
}

func (h *ServerHandler) StreamSessionHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodDelete {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return
	}
	if !h.authorized(r) {
		http.Error(w, `{"error":"unauthorized"}`, http.StatusUnauthorized)
		return
	}
	id := strings.TrimPrefix(r.URL.Path, "/api/v1/stream/")
	if id == "" || id == "audio" {
		http.Error(w, `{"error":"invalid_stream_id"}`, http.StatusBadRequest)
		return
	}
	h.streamer.CloseStream(id)
	w.WriteHeader(http.StatusNoContent)
}

func (h *ServerHandler) authorized(r *http.Request) bool {
	if h.token == "" {
		return false
	}
	return r.Header.Get("Authorization") == "Bearer "+h.token
}

func newStreamID() (string, error) {
	var raw [16]byte
	if _, err := rand.Read(raw[:]); err != nil {
		return "", err
	}
	return hex.EncodeToString(raw[:]), nil
}

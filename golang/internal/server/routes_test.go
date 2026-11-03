package server

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

const testEngineToken = "test-engine-token-012345678901234567890"

func TestHealthAndStreamAuthentication(t *testing.T) {
	t.Setenv("GO_ENGINE_TOKEN", testEngineToken)
	t.Setenv("GO_ENGINE_PUBLIC_URL", "https://audio.example.test")
	handler := NewServerHandler()
	server := NewEngineServer(8080)
	server.handler = handler
	httpHandler := server.SetupRoutes()

	health := httptest.NewRecorder()
	httpHandler.ServeHTTP(health, httptest.NewRequest(http.MethodGet, "/health", nil))
	if health.Code != http.StatusOK {
		t.Fatalf("health status = %d, want %d", health.Code, http.StatusOK)
	}

	unauthorized := httptest.NewRecorder()
	request := httptest.NewRequest(http.MethodPost, "/api/v1/stream", strings.NewReader(`{"url":"https://1.1.1.1/audio.mp3","format":"opus"}`))
	httpHandler.ServeHTTP(unauthorized, request)
	if unauthorized.Code != http.StatusUnauthorized {
		t.Fatalf("unauthorized status = %d, want %d", unauthorized.Code, http.StatusUnauthorized)
	}

	authorized := httptest.NewRecorder()
	request = httptest.NewRequest(http.MethodPost, "/api/v1/stream", strings.NewReader(`{"url":"https://1.1.1.1/audio.mp3","format":"opus"}`))
	request.Header.Set("Authorization", "Bearer "+testEngineToken)
	httpHandler.ServeHTTP(authorized, request)
	if authorized.Code != http.StatusOK {
		t.Fatalf("authorized status = %d, want %d: %s", authorized.Code, authorized.Body.String())
	}

	var response struct {
		Status    string `json:"status"`
		StreamURL string `json:"stream_url"`
		StreamID  string `json:"stream_id"`
	}
	if err := json.Unmarshal(authorized.Body.Bytes(), &response); err != nil {
		t.Fatalf("decode stream response: %v", err)
	}
	if response.Status != "READY" || response.StreamID == "" || !strings.HasPrefix(response.StreamURL, "https://audio.example.test/api/v1/stream/audio?") {
		t.Fatalf("unexpected stream response: %+v", response)
	}
}
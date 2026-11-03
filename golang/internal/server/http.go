package server

import (
	"fmt"
	"net/http"
	"cse-aspirant/golang/internal/errorhandling"
)

type EngineServer struct {
	addr    string
	handler *ServerHandler
}

func NewEngineServer(port int) *EngineServer {
	return &EngineServer{
		addr:    fmt.Sprintf(":%d", port),
		handler: NewServerHandler(),
	}
}

func (s *EngineServer) SetupRoutes() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("/health", s.handler.HealthHandler)
	mux.HandleFunc("/api/v1/stream", s.handler.StreamHandler)
	mux.HandleFunc("/api/v1/stream/", s.handler.StreamSessionHandler)
	mux.HandleFunc("/api/v1/stream/audio", s.handler.AudioHandler)
	return errorhandling.HTTPRecoveryMiddleware(mux)
}

func (s *EngineServer) ListenAndServe() error {
	return http.ListenAndServe(s.addr, s.SetupRoutes())
}

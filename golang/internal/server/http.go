package server

import (
	"fmt"
	"net/http"
	"time"
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
	server := &http.Server{
		Addr:              s.addr,
		Handler:           s.SetupRoutes(),
		ReadHeaderTimeout: 5 * time.Second,
		ReadTimeout:       10 * time.Second,
		WriteTimeout:      5 * time.Minute,
		IdleTimeout:       60 * time.Second,
	}
	return server.ListenAndServe()
}

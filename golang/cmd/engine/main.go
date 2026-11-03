package main

import (
	"log"
	"os"
	"strconv"
	"cse-aspirant/golang/internal/server"
	"cse-aspirant/golang/internal/worker"
)

func main() {
	port := 8080
	if envPort := os.Getenv("GO_ENGINE_PORT"); envPort != "" {
		if p, err := strconv.Atoi(envPort); err == nil {
			port = p
		}
	}

	log.Printf("[CSE ASPIRANT GO ENGINE] Initializing audio worker pool (8 workers)...")
	pool := worker.NewWorkerPool(8, 1024)
	pool.Start()
	defer pool.Stop()

	srv := server.NewEngineServer(port)
	log.Printf("[CSE ASPIRANT GO ENGINE] Audio Streaming Engine listening on :%d", port)
	if err := srv.ListenAndServe(); err != nil {
		log.Fatalf("Server terminated: %v", err)
	}
}

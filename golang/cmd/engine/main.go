package main

import (
	"log"
	"net/url"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"cse-aspirant/golang/internal/server"
	"cse-aspirant/golang/internal/worker"
)

func main() {
	port := 8080
	token := os.Getenv("GO_ENGINE_TOKEN")
	if len(token) < 32 {
		log.Fatal("GO_ENGINE_TOKEN must contain at least 32 characters")
	}
	publicURL := os.Getenv("GO_ENGINE_PUBLIC_URL")
	if publicURL == "" {
		log.Fatal("GO_ENGINE_PUBLIC_URL must be configured before starting the Go audio engine")
	}
	parsedPublicURL, err := url.ParseRequestURI(publicURL)
	if err != nil || parsedPublicURL.Hostname() == "" ||
		(parsedPublicURL.Scheme != "http" && parsedPublicURL.Scheme != "https") ||
		strings.ContainsAny(publicURL, "\r\n") {
		log.Fatal("GO_ENGINE_PUBLIC_URL must be an HTTP(S) URL with a hostname")
	}
	ffmpegPath := os.Getenv("FFMPEG_PATH")
	if ffmpegPath == "" {
		ffmpegPath = "ffmpeg"
	}
	if _, err := exec.LookPath(ffmpegPath); err != nil {
		log.Fatal("FFMPEG_PATH executable is not accessible")
	}
	if envPort := os.Getenv("GO_ENGINE_PORT"); envPort != "" {
		if p, err := strconv.Atoi(envPort); err == nil {
			if p < 1 || p > 65535 {
				log.Fatal("GO_ENGINE_PORT must be between 1 and 65535")
			}
			port = p
		} else {
			log.Fatal("GO_ENGINE_PORT must be an integer")
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

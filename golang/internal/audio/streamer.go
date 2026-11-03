package audio

import (
	"context"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"os/exec"
	"strconv"
	"sync"
	"time"
)

type StreamSession struct {
	ID        string    `json:"session_id"`
	URL       string    `json:"url"`
	Buffer    *RingBuffer
	IsLive    bool      `json:"is_live"`
	CreatedAt time.Time `json:"created_at"`
}

type AudioStreamer struct {
	mu          sync.RWMutex
	sessions    map[string]*StreamSession
	ffmpegPath  string
}

func NewAudioStreamer() *AudioStreamer {
	ffmpegPath := os.Getenv("FFMPEG_PATH")
	if ffmpegPath == "" {
		ffmpegPath = "ffmpeg"
	}
	return &AudioStreamer{
		sessions:   make(map[string]*StreamSession),
		ffmpegPath: ffmpegPath,
	}
}

func (s *AudioStreamer) OpenStream(id string, url string) (*StreamSession, error) {
	parsed, err := urlpkg(url)
	if err != nil {
		return nil, err
	}
	if parsed.Scheme != "http" && parsed.Scheme != "https" {
		return nil, fmt.Errorf("only HTTP(S) stream URLs are supported")
	}
	if url == "" {
		return nil, fmt.Errorf("invalid stream url")
	}

	session := &StreamSession{
		ID:        id,
		URL:       url,
		Buffer:    NewRingBuffer(256),
		IsLive:    true,
		CreatedAt: time.Now(),
	}
	s.mu.Lock()
	cutoff := time.Now().Add(-10 * time.Minute)
	for sessionID, existing := range s.sessions {
		if existing.CreatedAt.Before(cutoff) {
			delete(s.sessions, sessionID)
		}
	}
	s.sessions[id] = session
	s.mu.Unlock()
	return session, nil
}

func (s *AudioStreamer) CloseStream(id string) {
	s.mu.Lock()
	defer s.mu.Unlock()
	delete(s.sessions, id)
}

func (s *AudioStreamer) GetStream(id string) (*StreamSession, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	session, ok := s.sessions[id]
	return session, ok
}

func (s *AudioStreamer) Stream(ctx context.Context, w http.ResponseWriter, source string, position int) error {
	if position < 0 {
		return fmt.Errorf("invalid stream position")
	}
	if _, err := urlpkg(source); err != nil {
		return err
	}

	args := []string{"-hide_banner", "-loglevel", "error"}
	if position > 0 {
		args = append(args, "-ss", strconv.Itoa(position))
	}
	args = append(args,
		"-i", source,
		"-vn",
		"-c:a", "libopus",
		"-b:a", "128k",
		"-f", "ogg",
		"pipe:1",
	)
	cmd := exec.CommandContext(ctx, s.ffmpegPath, args...)
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		return err
	}
	if err := cmd.Start(); err != nil {
		return fmt.Errorf("start ffmpeg: %w", err)
	}
	w.Header().Set("Content-Type", "audio/ogg")
	w.Header().Set("Cache-Control", "no-store")
	_, copyErr := io.Copy(w, stdout)
	waitErr := cmd.Wait()
	if copyErr != nil {
		return copyErr
	}
	if waitErr != nil {
		return fmt.Errorf("ffmpeg exited: %w", waitErr)
	}
	return nil
}

func urlpkg(raw string) (*url.URL, error) {
	parsed, err := url.ParseRequestURI(raw)
	if err != nil || parsed.Host == "" {
		return nil, fmt.Errorf("invalid stream URL")
	}
	return parsed, nil
}

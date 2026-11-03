package audio

import (
	"fmt"
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
	sessions map[string]*StreamSession
}

func NewAudioStreamer() *AudioStreamer {
	return &AudioStreamer{
		sessions: make(map[string]*StreamSession),
	}
}

func (s *AudioStreamer) OpenStream(id string, url string) (*StreamSession, error) {
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
	s.sessions[id] = session
	return session, nil
}

func (s *AudioStreamer) CloseStream(id string) {
	delete(s.sessions, id)
}

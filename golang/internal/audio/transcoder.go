package audio

import (
	"fmt"
	"time"
)

type TranscodeResult struct {
	OriginalURL string        `json:"original_url"`
	TargetCodec string        `json:"target_codec"`
	BitrateKbps int           `json:"bitrate_kbps"`
	Duration    time.Duration `json:"duration"`
	Status      string        `json:"status"`
	StreamURL   string        `json:"stream_url,omitempty"`
	StreamID    string        `json:"stream_id,omitempty"`
}

type Transcoder struct{}

func NewTranscoder() *Transcoder {
	return &Transcoder{}
}

func (t *Transcoder) Process(streamURL string, targetCodec string) (*TranscodeResult, error) {
	if streamURL == "" {
		return nil, fmt.Errorf("empty stream URL")
	}
	if targetCodec == "" {
		targetCodec = "opus"
	}
	if targetCodec != "opus" {
		return nil, fmt.Errorf("unsupported target codec: %s", targetCodec)
	}

	return &TranscodeResult{
		OriginalURL: streamURL,
		TargetCodec: targetCodec,
		BitrateKbps: 128,
		Duration:    0,
		Status:      "READY",
	}, nil
}

package errorhandling

import (
	"errors"
	"fmt"
	"time"
)

var (
	ErrStreamNotFound  = errors.New("audio stream not found or unreachable")
	ErrTranscodeFailed = errors.New("transcoding operation failed")
	ErrBufferOverflow  = errors.New("audio ring buffer overflow")
	ErrWorkerTimeout   = errors.New("worker job timed out")
)

type EngineError struct {
	Code      string    `json:"code"`
	Message   string    `json:"message"`
	Timestamp time.Time `json:"timestamp"`
}

func (e *EngineError) Error() string {
	return fmt.Sprintf("[%s] %s (at %s)", e.Code, e.Message, e.Timestamp.Format(time.RFC3339))
}

func NewEngineError(code, message string) *EngineError {
	return &EngineError{
		Code:      code,
		Message:   message,
		Timestamp: time.Now(),
	}
}

package errorhandling

import (
	"log"
	"net/http"
	"runtime/debug"
)

// SafeGo runs a goroutine with panic recovery
func SafeGo(fn func()) {
	go func() {
		defer func() {
			if r := recover(); r != nil {
				log.Printf("[PANIC RECOVERED] %v\nStack: %s", r, debug.Stack())
			}
		}()
		fn()
	}()
}

// HTTPRecoveryMiddleware catches panics in HTTP endpoints
func HTTPRecoveryMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			if err := recover(); err != nil {
				log.Printf("[HTTP PANIC RECOVERED] %v", err)
				http.Error(w, `{"error":"internal_server_error"}`, http.StatusInternalServerError)
			}
		}()
		next.ServeHTTP(w, r)
	})
}

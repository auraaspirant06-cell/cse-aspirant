package audio

import (
	"sync"
)

// RingBuffer stores streaming audio chunks in memory
type RingBuffer struct {
	mu       sync.RWMutex
	data     [][]byte
	capacity int
}

func NewRingBuffer(capacity int) *RingBuffer {
	return &RingBuffer{
		data:     make([][]byte, 0, capacity),
		capacity: capacity,
	}
}

func (b *RingBuffer) Push(chunk []byte) {
	b.mu.Lock()
	defer b.mu.Unlock()

	if len(b.data) >= b.capacity {
		b.data = b.data[1:] // Discard oldest chunk
	}
	b.data = append(b.data, chunk)
}

func (b *RingBuffer) Drain() [][]byte {
	b.mu.Lock()
	defer b.mu.Unlock()

	res := b.data
	b.data = make([][]byte, 0, b.capacity)
	return res
}

func (b *RingBuffer) Size() int {
	b.mu.RLock()
	defer b.mu.RUnlock()
	return len(b.data)
}

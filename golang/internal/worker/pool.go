package worker

import (
	"context"
	"fmt"
	"log"
	"sync"
)

type WorkerPool struct {
	concurrency int
	jobQueue    chan Job
	wg          sync.WaitGroup
	ctx         context.Context
	cancel      context.CancelFunc
	stopOnce    sync.Once
}

func NewWorkerPool(concurrency int, queueCap int) *WorkerPool {
	ctx, cancel := context.WithCancel(context.Background())
	return &WorkerPool{
		concurrency: concurrency,
		jobQueue:    make(chan Job, queueCap),
		ctx:         ctx,
		cancel:      cancel,
	}
}

func (wp *WorkerPool) Start() {
	for i := 0; i < wp.concurrency; i++ {
		wp.wg.Add(1)
		go wp.runWorker()
	}
}

func (wp *WorkerPool) runWorker() {
	defer wp.wg.Done()
	for {
		select {
		case <-wp.ctx.Done():
			return
		case job, ok := <-wp.jobQueue:
			if !ok {
				return
			}
			if err := job.Execute(wp.ctx); err != nil {
				log.Printf("audio job %s failed: %v", job.ID(), err)
			}
		}
	}
}

func (wp *WorkerPool) Submit(job Job) error {
	select {
	case <-wp.ctx.Done():
		return fmt.Errorf("worker pool is stopped")
	case wp.jobQueue <- job:
		return nil
	}
}

func (wp *WorkerPool) Stop() {
	wp.stopOnce.Do(func() {
		wp.cancel()
		close(wp.jobQueue)
		wp.wg.Wait()
	})
}

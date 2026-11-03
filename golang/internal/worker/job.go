package worker

import "context"

type Job interface {
	ID() string
	Execute(ctx context.Context) error
}

type AudioJob struct {
	JobID    string
	URL      string
	Action   string
	ResultCh chan error
}

func (j *AudioJob) ID() string {
	return j.JobID
}

func (j *AudioJob) Execute(ctx context.Context) error {
	// Worker processes audio chunk or stream health
	return nil
}

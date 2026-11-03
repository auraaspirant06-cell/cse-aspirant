.PHONY: build run test clean

build:
	go build -o bin/music-engine cmd/engine/main.go

run:
	go run cmd/engine/main.go

test:
	go test ./...

clean:
	rm -rf bin/

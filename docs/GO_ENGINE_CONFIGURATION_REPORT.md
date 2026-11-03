# Go Audio Engine Configuration Report

## Source-derived runtime

- Binary: `/usr/local/bin/music-engine` in the Docker image.
- Listen address: `:8080` by default, which binds all container interfaces.
- Compose service: `golang-engine`.
- Compose mapping: host port `8080` to container port `8080`.
- Health: `GET /health`.
- Create stream: authenticated `POST /api/v1/stream` with `{url, format, position}`.
- Read audio: unauthenticated `GET /api/v1/stream/audio?id=<id>&position=<seconds>`.
- Close session: authenticated `DELETE /api/v1/stream/<id>`.
- Authentication: exact `Authorization: Bearer <GO_ENGINE_TOKEN>` header.
- FFmpeg: `FFMPEG_PATH`, defaulting to `ffmpeg`; startup checks it with `exec.LookPath`.
- Docker FFmpeg: installed by `deployment/Dockerfile` with Debian `apt-get`.

## Configuration profiles

| Profile | `GO_ENGINE_URL` | `GO_ENGINE_PUBLIC_URL` | `GO_ENGINE_PORT` | `FFMPEG_PATH` |
| --- | --- | --- | --- | --- |
| Windows local | `http://127.0.0.1:8080` | `http://127.0.0.1:8080` for a local client only | `8080` | `ffmpeg` only if FFmpeg is on `PATH` |
| Docker Compose | `http://golang-engine:8080` | The real host URL reachable by Telegram, for example `https://audio.example.com` | `8080` | `ffmpeg` |
| Linux VPS/EC2 | `http://127.0.0.1:8080` when Python runs on the host, or `http://golang-engine:8080` when both run in Compose | The real public DNS/TLS URL for the Go audio endpoint, for example `https://audio.example.com` | `8080` | `ffmpeg` if installed, otherwise an absolute installed binary path |

`GO_ENGINE_TOKEN` has no source-derived literal value. Generate one per deployment and copy the same value to Python and Go. Do not commit it or expose it to frontend variables. A PowerShell generator is documented in `.env.example`.

## Connectivity conclusions

Python calls the private `POST /api/v1/stream` route with the required bearer header and validates `READY`, `stream_url`, and `stream_id`. It closes sessions through the authenticated delete route and checks health at `/health`.

The public stream URL is implemented by Go, but it is only reachable when `GO_ENGINE_PUBLIC_URL` points to a network path visible to PyTgCalls/Telegram. The Compose service name is not public, and localhost is not public to Telegram. No reverse proxy or TLS configuration was found in the repository; a VPS deployment therefore needs an external proxy/firewall/DNS setup or a deliberately exposed port.

The Go handler rejects non-HTTP(S) source URLs and DNS-resolved loopback, private, link-local, and unspecified addresses before FFmpeg is started. This is an application-level SSRF defense; a production proxy should additionally restrict egress and handle redirect/rebinding policy.

## Validation status

- Editor diagnostics: clean for all edited Go, Python, Compose, and documentation files.
- Go, Python, and source-level route tests were added, but could not be executed from this GitHub-backed virtual workspace because VS Code task execution cannot target its `vscode-vfs` URI.
- Local Windows probe: Go `1.27.3` and Python `3.15.2` are installed; FFmpeg and Docker are not installed or available on `PATH`.
- Dockerfile inspection confirms the Docker image installs FFmpeg, but container health, Go tests, Python tests, authentication, and live stream transcoding still require a checkout with executable workspace access plus Docker/FFmpeg.
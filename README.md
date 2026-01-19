# Python Socket Rate Limiter

This project demonstrates a simple rate-limited server and client using Python sockets and threading. It implements a per-user rate limiter using the token bucket algorithm.

## Features
- **Server**: Accepts multiple client connections, assigns each a unique ID, and enforces a rate limit (10 requests per minute per user).
- **Client**: Connects to the server and allows sending requests interactively, displaying server responses.
- **Rate Limiting**: Uses a token bucket algorithm for efficient and fair request limiting.

## How It Works
- Each client connection is assigned a unique user ID.
- Each user starts with 10 tokens (requests allowed).
- Tokens are refilled at a rate of 10 per 60 seconds (1 every 6 seconds).
- If a user sends a request and has tokens, the request is allowed and a token is consumed.
- If no tokens are available, the server responds with a rate limit message.

## Usage

### 1. Start the Server
```bash
python server.py
```

### 2. Start the Client (in a new terminal)
```bash
python client.py
```
Type messages and press Enter to send requests to the server. The server will respond if you are rate-limited or allowed.

## Requirements
- Python 3.x
- No external dependencies (uses only the Python standard library)

## Notes
- This project is for educational/demo purposes. 

## License
MIT License

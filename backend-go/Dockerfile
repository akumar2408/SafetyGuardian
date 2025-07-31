# Build stage
FROM golang:1.21-alpine AS builder
WORKDIR /app

# Copy Go module files and download dependencies
COPY go.mod ./
RUN go mod download

# Copy the rest of the source code
COPY . .

# Build the Go binary
RUN CGO_ENABLED=0 GOOS=linux go build -o gateway .

# Final stage: minimal runtime image
FROM alpine:latest
WORKDIR /root/
COPY --from=builder /app/gateway .
EXPOSE 8080

# Run the compiled binary
CMD ["./gateway"]

FROM golang:latest as builder
WORKDIR /app
COPY ./go.mod ./go.sum .
RUN go mod download
COPY ../.. .
RUN go build -o /tg_bot_service ./cmd/
CMD ["/tg_bot_service"]
#!/bin/sh
set -e

# Khởi động ollama serve trong nền
ollama serve &
sleep 5  # chờ server khởi động ổn định (tùy máy, có thể tăng)

# Pull model
ollama pull llama3.2 || true

# Giữ tiến trình foreground để container không thoát
wait

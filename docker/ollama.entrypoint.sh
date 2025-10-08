#!/bin/sh
set -e

if ! ollama list | grep -q "llama3.2"; then
  echo "Model llama3.2 not found. Pulling..."
  ollama pull llama3.2
fi

exec ollama serve

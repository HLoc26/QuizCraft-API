#!/bin/sh
set -e

# Start server
exec ollama serve

# Pull model: llama3.2
ollama pull llama3.2
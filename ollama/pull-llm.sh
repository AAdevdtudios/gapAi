./bin/ollama serve &
pid=$!
sleep 5

echo "Pulling mistral model"
ollama pull qwen:0.5b
echo "Done pulling"

wait $pid
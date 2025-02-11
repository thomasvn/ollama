# Ollama

Experimenting ...

## Hosting Ollama

Docker:

```sh
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

```sh
# Pull a ~1.3GB model
curl http://localhost:11434/api/pull -d '{
  "model": "llama3.2:1b"
}'

# Query
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "With a $10,000 loan at a 6% interest, how can I pay this off in 2 years?",
  "stream": false
}'
```

Kubernetes:

```sh
kubectl apply -f ollama-k8s.yaml
```

## Links

- https://ollama.com/search
- https://github.com/ollama/ollama/blob/main/docs/api.md
- https://hub.docker.com/r/ollama/ollama/tags
- https://github.com/otwld/ollama-helm

<!-- TODO
- code-explain
  - Python codebase summarizer? Recursively look at this file/directory and describe its operations?
  - Be able to chat and ask questions of the codebase?
  - Stream the results
  - How to deal with context window constraints?
- granite-code
- Code review assistant
- Documentation generator
- Natural language query interface for databases
- deepseek-r1
- llama3.2
- Modelfiles. Fine-tuning an existing Model.
- IBM Granite Models? Granite Time Series Foundation Model?
- https://github.com/otwld/ollama-helm
-->

<!-- DONE
- Serving Ollama via Docker and Kubernetes
-->
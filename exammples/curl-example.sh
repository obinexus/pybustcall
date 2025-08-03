# Bust cache via Python binding
curl -X POST http://localhost:3000/api/v1/bust \
  -H "Content-Type: application/json" \
  -d '{"target": "cdn/main.css", "binding": "python", "strategy": "dimensional"}'

# Check daemon status
curl http://localhost:3000/api/v1/status

# Get binding capabilities
curl http://localhost:3000/api/v1/capabilities

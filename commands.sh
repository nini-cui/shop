# create categories
curl -X POST http://localhost:8000/categories/ \ -H "Content-Type: application/json" \ -d '{"name": "test", "slug": "test"}'
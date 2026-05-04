# Setup Instructions

## Post-Installation Steps

### 1. Add Screenshot to README

The README.md file references a screenshot at the top. To include it:

1. Take a screenshot of the running application (http://127.0.0.1:8000)
2. Save it as `screenshot.png` in the project root directory
3. The README will automatically display it

### 2. Model Setup

The T5 model files need to be placed in `models/saved_summary_model/`

Required files:
- `config.json` - Model configuration
- `generation_config.json` - Generation settings  
- `model.safetensors` - Model weights
- `tokenizer.json` - Tokenizer vocabulary
- `tokenizer_config.json` - Tokenizer settings

These files should already be in place. If missing, they will be auto-downloaded on first run.

### 3. Environment Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your settings (optional):
   ```
   FASTAPI_ENV=development
   HOST=127.0.0.1
   PORT=8000
   ```

### 4. Verify Installation

Test the setup by running:

```bash
# Start the application
python run.py

# In another terminal, test the API
curl -X POST http://127.0.0.1:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"dialogue": "Machine learning is a subset of artificial intelligence that focuses on the development of algorithms and statistical models that enable computers to improve their performance on tasks through experience."}'
```

Expected response:
```json
{
  "summary": "Machine learning is a subset of artificial intelligence that improves through experience."
}
```

### 5. Run with Docker (Optional)

```bash
# Build and run with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f text-summarizer

# Stop the service
docker-compose down
```

### 6. Deploy to GitHub

1. Initialize git repository:
   ```bash
   git init
   ```

2. Add all files:
   ```bash
   git add .
   ```

3. Create initial commit:
   ```bash
   git commit -m "Initial commit: Text Summarizer App with T5 model"
   ```

4. Add remote repository:
   ```bash
   git remote add origin https://github.com/yourusername/text-summarizer-app.git
   ```

5. Push to GitHub:
   ```bash
   git branch -M main
   git push -u origin main
   ```

### 7. GitHub Repository Features

Add these badges to your README.md for visibility:

```markdown
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104.1-009485.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Transformers](https://img.shields.io/badge/transformers-4.35.2-FF6B6B)](https://huggingface.co/transformers)
```

### 8. Troubleshooting Setup Issues

**Issue**: ModuleNotFoundError when running
```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Issue**: Port 8000 already in use
```bash
# Solution: Use different port
uvicorn app.main:app --port 8001
```

**Issue**: Model download fails
```bash
# Solution: Pre-download model
python -c "from transformers import T5ForConditionalGeneration, T5Tokenizer; \
T5ForConditionalGeneration.from_pretrained('google/t5-base'); \
T5Tokenizer.from_pretrained('google/t5-base')"
```

## Production Deployment Checklist

- [ ] Screenshot added to README
- [ ] Environment variables configured in `.env`
- [ ] Model files verified in `models/saved_summary_model/`
- [ ] All tests passing
- [ ] README badges added
- [ ] Repository pushed to GitHub
- [ ] Docker image builds successfully
- [ ] Health endpoint responding
- [ ] API documentation accessible at `/docs`

## Next Steps

1. Customize the application further based on your needs
2. Add unit tests in a `tests/` directory
3. Add CI/CD pipeline using GitHub Actions
4. Monitor application performance
5. Collect user feedback and iterate

For more details, see [README.md](./README.md)

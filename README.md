# reqtrace

A lightweight HTTP request tracing middleware for FastAPI and Flask that outputs structured logs with correlation IDs.

---

## Installation

```bash
pip install reqtrace
```

---

## Usage

### FastAPI

```python
from fastapi import FastAPI
from reqtrace import ReqTraceMiddleware

app = FastAPI()
app.add_middleware(ReqTraceMiddleware)

@app.get("/hello")
def hello():
    return {"message": "Hello, world!"}
```

### Flask

```python
from flask import Flask
from reqtrace import ReqTraceMiddleware

app = Flask(__name__)
ReqTraceMiddleware(app)

@app.route("/hello")
def hello():
    return {"message": "Hello, world!"}
```

Each request automatically generates a correlation ID and emits structured log output:

```json
{
  "correlation_id": "4f3a1c2e-8b0d-4e6f-a123-9d7e5f2c1b0a",
  "method": "GET",
  "path": "/hello",
  "status_code": 200,
  "duration_ms": 12.4
}
```

Pass a custom correlation ID via the `X-Correlation-ID` request header to propagate existing trace contexts.

---

## Configuration

| Option | Default | Description |
|---|---|---|
| `log_level` | `INFO` | Logging level for trace output |
| `exclude_paths` | `[]` | List of paths to skip tracing |
| `header_name` | `X-Correlation-ID` | Header used to read/write correlation ID |

---

## License

MIT © reqtrace contributors
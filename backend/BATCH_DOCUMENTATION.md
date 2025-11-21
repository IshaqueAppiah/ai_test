# Batch API Documentation

This document explains how to use the backend batch endpoints (`/batch/*`) to upload JSONL files for batched requests to the OpenAI API, how the input must be formatted, and how to inspect results.

## Endpoints

- `POST /batch/upload` — Upload a JSONL file (UTF-8) where each non-empty line is a JSON object representing a single request. The server validates the file and, on success, uploads it to OpenAI Files with `purpose=batch` and creates a batch job.
- `GET /batch/status/{batch_id}` — Retrieve the OpenAI batch metadata (status, error list, timestamps).
- `GET /batch/results/{file_id}` — Download file contents (for example error files, output files) returned by OpenAI.
- `POST /batch/cancel/{batch_id}` — Request cancellation of the given batch job.
- `GET /batch/list` — List recent batch jobs.

## Input format (JSON Lines / JSONL)

The upload accepts a JSON Lines file; each line must be a JSON object. Two styles are accepted by the backend validation:

1. Simple objects that include a `custom_id` and any application-specific payload. Example:

```jsonl
{"custom_id": "batch-1", "payload": {"prompt": "What is the capital of France?"}}
```

2. Batch-request objects for the OpenAI Batch API. These must include at minimum:
- `custom_id` — unique identifier for the row
- `method` — HTTP method (backend currently supports `POST` only for batch requests)
- `url` or `path` — endpoints such as `/v1/chat/completions` (the backend accepts either `url` or `path` keys but prefers `url`)
- `body` — request body (object) to send to the endpoint

Example batch request line:

```jsonl
{"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-3.5-turbo-0125", "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello world!"}], "max_tokens": 100}}
```

Notes:
- All lines must be valid JSON. If any line fails to parse or is missing a required field (`custom_id`, and for batch-style rows: `method` and `url`/`path`), the server will return `400 Bad Request` with a message identifying the bad line number and the error.
- The server validates that `method` is a string and currently only accepts `POST` for batch requests.

## Validation rules enforced by this backend

- File must be UTF-8 decodable.
- File must contain at least one non-empty JSON line.
- Each line must parse as JSON.
- Each parsed JSON must be an object and include `custom_id`.
- If `method` or `path`/`url` are present, ensure `method` is `POST` and `path`/`url` is a non-empty string.

If any of these checks fail, the response will be `400` with a helpful description, e.g. `Invalid JSON or missing field on line 3: Missing required field 'custom_id'`.

## Sample JSONL (copy this into a file named `sample_batch.jsonl`)

Use the following sample to test the batch upload. Each line is a valid batch request to `/v1/chat/completions`.

```jsonl
{"custom_id": "batch-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-5-nano", "messages": [{"role": "user", "content": "What is the capital of France?"}], "max_tokens": 100}}
{"custom_id": "batch-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-5-nano", "messages": [{"role": "user", "content": "Explain Newton's second law in one sentence."}], "max_tokens": 150}}
{"custom_id": "batch-3", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-5-nano", "messages": [{"role": "user", "content": "List three uses of machine learning in healthcare."}], "max_tokens": 200}}
{"custom_id": "batch-4", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-5-nano", "messages": [{"role": "user", "content": "Provide a short summary (2 sentences) of the following passage: 'Artificial intelligence is transforming industries by enabling new automation and insights.'"}], "max_tokens": 200}}
```

Save that as `backend/sample_batch.jsonl` (it is included in this repo) and then run the curl command below.

## Example curl commands

- Upload the file:

```bash
curl -X POST -F "file=@backend/sample_batch.jsonl" http://localhost:8000/batch/upload
```

- Response (successful):

```json
{
  "filename": "sample_batch.jsonl",
  "result": { "file_id": "file-...", "batch_id": "batch-..." }
}
```

- Check status:

```bash
curl http://localhost:8000/batch/status/<batch_id>
```

- If a batch fails, the status response contains `errors` with per-line diagnostics. Example:

```json
{
  "batch": {
    "status": "failed",
    "errors": {
      "data": [
        {"line": 1, "code": "missing_required_parameter", "message": "Missing required parameter: 'url'.", "param": "url"},
        ...
      ]
    }
  }
}
```

## Troubleshooting

- If you see `missing_required_parameter: 'url'` or `'method'`, update your JSONL lines so each batch request includes `method` and `url` (see sample above).
- If the OpenAI SDK reports connection errors (DNS or network), ensure your environment has network access and the appropriate API keys set in `.env`.

## Next steps

- Add persistence or a UI to track jobs and show progress.
- Add automated tests that post `sample_batch.jsonl` to the upload endpoint and mock the OpenAI SDK.

from typing import Any, Dict

result: Dict[str, Any] = {
    "id": "evalrun_691f045f271c81919e18fae9dfd4604f",
    "created_at": 1763640415,
    "data_source": {
        "source": {
            "id": "file-WGnrTR8wUwWaEsXV1NcCLn",
            "type": "file_id"
        },
        "type": "responses",
        "input_messages": {
            "template": [
                {
                    "content": "You are an expert at answering factual questions. Answer concisely and accurately.",
                    "role": "system",
                    "type": "message"
                },
                {
                    "content": "{{ item.input }}",
                    "role": "user",
                    "type": "message"
                }
            ],
            "type": "template"
        },
        "model": "gpt-5-nano",
        "sampling_params": None
    },
    "error": None,
    "eval_id": "eval_691f045dd2b881919ee7fb0d0cc89a7e",
    "metadata": {},
    "model": "gpt-5-nano",
    "name": "QA Eval Run",
    "object": "eval.run",
    "per_model_usage": [
        {
            "cached_tokens": 0,
            "completion_tokens": 1722,
            "invocation_count": 10,
            "model_name": "gpt-5-nano-2025-08-07",
            "prompt_tokens": 343,
            "total_tokens": 2065
        }
    ],
    "per_testing_criteria_results": [
        {
            "failed": 6,
            "passed": 4,
            "testing_criteria": "Match output to ideal answer-02c9b2d3-bf88-4f28-9d4f-05893dd457ea",
            "testing_criteria_id": "Match output to ideal answer-02c9b2d3-bf88-4f28-9d4f-05893dd457ea"
        }
    ],
    "report_url": "https://platform.openai.com/evaluations/eval_691f045dd2b881919ee7fb0d0cc89a7e?project_id=proj_qDHGPSZUpKpdbTRuW8QbFXv4&run_id=evalrun_691f045f271c81919e18fae9dfd4604f",
    "result_counts": {
        "errored": 0,
        "failed": 6,
        "passed": 4,
        "total": 10
    },
    "status": "completed",
    "shared_with_openai": False
}
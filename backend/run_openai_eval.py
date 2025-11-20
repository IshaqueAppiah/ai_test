
from openai import OpenAI
client = OpenAI()
def run_evaluation():
    try:
        with open("eval_data.jsonl", "rb") as f:
            file = client.files.create(file=f, purpose="fine-tune")
        eval_obj = client.evals.create(
            name="QA Eval",
            data_source_config={
                "type": "custom",
                "item_schema": {
                    "type": "object",
                    "properties": {
                        "input": {"type": "string"},
                        "ideal_output": {"type": "string"},
                    },
                    "required": ["input", "ideal_output"],
                },
                "include_sample_schema": True,
            },
            testing_criteria=[
                {
                    "type": "string_check",
                    "name": "Match output to ideal answer",
                    "input": "{{ sample.output_text }}",
                    "operation": "eq",
                    "reference": "{{ item.ideal_output }}",
                }
            ],
        )
        run = client.evals.runs.create(
            eval_obj.id,
            name="QA Eval Run",
            data_source={
                "type": "responses",
                "model": "gpt-5-nano",
                "input_messages": {
                    "type": "template",
                    "template": [
                        {"role": "system", "content": "You are an expert at answering factual questions. Answer concisely and accurately."},
                        {"role": "user", "content": "{{ item.input }}"},
                    ],
                },
                "source": {"type": "file_id", "id": file.id},
            },
        )
        return run
    except Exception as e:
        # Return error details in a dict for FastAPI JSON response
        return {"error": str(e)}
    

def retrieve_result(eval_id: str, run_id: str):
    # OpenAI API expects both eval_id and run_id as keyword arguments
    try:
        run = client.evals.runs.retrieve(eval_id=eval_id, run_id=run_id)
        return run
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    result = run_evaluation()
    print("Eval run result:")
    print(result)

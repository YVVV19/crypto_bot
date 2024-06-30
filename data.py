import json

def get_answer(
    file_path: str = "data.json", answer_id: int | None = None
) -> list[dict] | dict:
    with open(file_path, "r") as fp:
        answer = json.load(fp)
        if answer_id != None and answer_id < len(answer):
            return answer[answer_id]
        return answer
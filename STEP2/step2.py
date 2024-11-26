import base64
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pororo import Pororo

# .env 파일에서 API 키 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")  # 환경변수에서 API 키 가져오기

# API 키가 잘 불러와졌는지 확인
if not api_key:
    raise ValueError("API key not found. Please check your .env file.")

client = OpenAI(
    api_key=api_key,
)
ocr = Pororo(task="ocr", lang="ko")

# 이미지 인코딩 함수 정의
def encode_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Pororo OCR
def analyze_image_pororo(image_path):
    ocr_result = ocr(image_path)
    return "\n".join(ocr_result)

# request openai by function call
def request_openai(image_base64, ocr_text):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You must return function call. if user have image, you must consider the image.",
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": ocr_text},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ],
            }
        ],
        model="gpt-4o-mini",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "format_student_id_info",
                    "description": (
                        "주어진 학번, 이름, 학과, 재학여부 정보를 포맷팅해 줘. "
                        "다음 형식으로 출력해 줘: '학번: [학번], 이름: [이름], 학과: [학과], 재학여부: [재학여부]'. "
                        "재학여부는 '재학', '휴학', '졸업' 중 하나로 출력해 줘. "
                        "알 수 없는 정보는 'None' 이라고 출력해 줘."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "student_id": {
                                "type": "string",
                                "description": "The student ID number.",
                            },
                            "name": {
                                "type": "string",
                                "description": "The name of the student.",
                            },
                            "department": {
                                "type": "string",
                                "description": "The department of the student.",
                            },
                            "university": {
                                "type": "string",
                                "description": "The university of the student.",
                            },
                            "status": {
                                "type": "string",
                                "description": "The enrollment status of the student.",
                            },
                        },
                        "required": ["student_id", "name", "department", "university", "status"],
                        "additionalProperties": False,
                    },
                }
            }
        ],
    )

    # check if the request was successful
    if not chat_completion or 'error' in chat_completion:
        raise Exception("Request failed with error: {}".format(chat_completion.get('error', 'Unknown error')))

    try:
        # TODO: 에러 핸들링 해야 해요
        function_call = chat_completion.choices[0].message.tool_calls[0]
        return json.loads(function_call.function.arguments)
    except Exception as e:
        print("Error occurred while parsing the response.")
        print(e)
        return None

# openai + pororo
def analyze_image(image_path):
    image_base64 = encode_image_base64(image_path)
    ocr_text = analyze_image_pororo(image_path)
    req = request_openai(image_base64, ocr_text)
    return req

# TODO: 병렬 처리나 배치는 나중에 생각해보셔도 될 것 같아요.

if __name__ == "__main__":
    test_img_path = r"./test_img/7.png"
    req = analyze_image(test_img_path)
    print(req)
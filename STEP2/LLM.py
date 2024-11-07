import base64
import requests
import os
import csv
from dotenv import load_dotenv

# .env 파일에서 API 키 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")  # 환경변수에서 API 키 가져오기

# API 키가 잘 불러와졌는지 확인
if not api_key:
    raise ValueError("API key not found. Please check your .env file.")
else:
    print("API Key loaded successfully.")

# 이미지 인코딩 함수 정의
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# OpenAI API 요청 함수 정의
def analyze_image(image_path):
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "주어진 이미지가 모바일 학생증 이미지인지 판단해 줘. "
                            "학번은 무조건 6자리 이상의 숫자로 인식해. 학번, 이름 정보가 없다면 모바일 학생증이 아니야. "
                            "만약 모바일 학생증 이미지라면 학번, 이름, 학과, 재학여부를 찾아 "
                            "다음 형식으로 출력해 줘: '학번: [학번], 이름: [이름], 학과: [학과], 재학여부: [재학여부]'. "
                            "재학여부는 '재학', '휴학', '졸업' 중 하나로 출력해 줘. "
                            "이미지를 통해 알 수 없는 정보는 '알 수 없음' 이라고 출력해 줘. "
                            "읽은 글자가 문맥에 맞지 않거나 잘못 읽은 걸로 판단된다면 정보를 유추하거나 '알 수 없음'으로 처리해."
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Error message:", response.text)
        return None

# CSV 파일로 저장 함수
def save_to_csv(data, csv_filename="student_data.csv"):
    # CSV 파일의 헤더 정의
    fieldnames = ["index", "university", "department", "name", "student-id", "path"]
    with open(csv_filename, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data saved to {csv_filename}")

# 메인 코드
def main(image_paths):
    data = []
    for idx, path in enumerate(image_paths):
        result = analyze_image(path)
        if result:
            # OpenAI 응답에서 필요한 정보 추출
            text_response = result['choices'][0]['message']['content']
            
            # GPT-4 응답 텍스트 그대로 출력
            print(f"GPT-4 Response for Image {idx+1}:\n{text_response}")
            print("-" * 40)

            # 데이터를 CSV 형식으로 변환
            student_info = {
                "index": idx,
                "university": "알 수 없음",  # university 정보 추출 가능 시 업데이트
                "department": "알 수 없음",  # department 정보 추출 가능 시 업데이트
                "name": "알 수 없음",
                "student-id": "알 수 없음",
                "path": path
            }
            
            # 텍스트에서 정보를 추출하여 student_info에 업데이트 (간단한 파싱)
            for line in text_response.split(", "):
                if "학번:" in line:
                    student_info["student-id"] = line.replace("학번:", "").strip()
                elif "이름:" in line:
                    student_info["name"] = line.replace("이름:", "").strip()
                elif "학과:" in line:
                    student_info["department"] = line.replace("학과:", "").strip()
                elif "재학여부:" in line:
                    student_info["university"] = line.replace("재학여부:", "").strip()
            
            # 결과를 터미널에 출력
            print(f"Processed Image {idx+1}:")
            print(f"  학번: {student_info['student-id']}")
            print(f"  이름: {student_info['name']}")
            print(f"  학과: {student_info['department']}")
            print(f"  재학여부: {student_info['university']}")
            print(f"  경로: {student_info['path']}")
            print("-" * 40)

            data.append(student_info)

    # CSV로 저장
    save_to_csv(data)

# 이미지 경로 리스트 설정
image_paths = [
    "/Users/mac/Desktop/HAI-2024/images/ajou.png",
    "/Users/mac/Desktop/HAI-2024/images/cau.png",
    "/Users/mac/Desktop/HAI-2024/images/hankuk.png",
    "/Users/mac/Desktop/HAI-2024/images/hanyang.png",
    "/Users/mac/Desktop/HAI-2024/images/kaist.png",
    "/Users/mac/Desktop/HAI-2024/images/ku.png",
    "/Users/mac/Desktop/HAI-2024/images/yonsei.png"
]


# 실행
main(image_paths)

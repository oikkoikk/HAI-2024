from easyocr.easyocr import Reader
import os
import openai


# 파일 리스트를 가져오는 함수
def get_files(path):
    file_list = []
    files = [f for f in os.listdir(path) if not f.startswith('.')]  # 숨김 파일 무시
    files.sort()
    abspath = os.path.abspath(path)
    for file in files:
        file_path = os.path.join(abspath, file)
        file_list.append(file_path)

    return file_list, len(file_list)


# GPT API로 텍스트를 전송하여 분석 결과를 받는 함수
def analyze_text_with_gpt(prompt_text, api_key):
    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # 사용할 GPT 모델 (gpt-4 또는 gpt-3.5-turbo)
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text}
            ],
            max_tokens=256,
            temperature=0.7
        )
        # GPT 응답 텍스트 반환
        return response['choices'][0]['message']['content']
    except openai.OpenAIError as e:  # 최신 OpenAI 라이브러리에서의 에러 핸들링
        print(f"GPT API 요청 오류: {e}")
        return None



if __name__ == '__main__':
    # GPU 설정 (사용 가능하면 활성화, 그렇지 않으면 비활성화)
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # GPU ID 지정
    use_gpu = True  # GPU를 사용하지 않을 경우 False로 설정

    # 사용자 정의 모델 설정
    model_storage_directory = './model'  # 모델 저장 디렉토리
    user_network_directory = './model'  # 사용자 정의 네트워크 디렉토리
    recog_network = 'custom'  # 사용자 정의 네트워크 이름

    # EasyOCR Reader 초기화
    reader = Reader(
        ['ko'],  # 언어 설정
        gpu=use_gpu,  # GPU 사용 여부
        model_storage_directory=model_storage_directory,
        user_network_directory=user_network_directory,
        recog_network=recog_network
    )

    # 이미지 파일 가져오기
    image_directory = './image'  # 이미지 디렉토리
    files, count = get_files(image_directory)

    # API 키 설정
    with open("API_KEY.txt") as f:
        API_KEY = f.read().strip()

    # 이미지 파일 처리
    for idx, file in enumerate(files):
        filename = os.path.basename(file)
        print(f"[{idx + 1}/{count}] Processing: {filename}")

        # 이미지에서 텍스트 읽기
        result = reader.readtext(file)

        # 추출된 텍스트 합치기
        extracted_texts = [string for (_, string, _) in result]
        combined_text = " ".join(extracted_texts)
        print(f"Extracted Text from '{filename}': {combined_text}")

        # GPT API 호출
        gpt_prompt = (
            f"다음은 모바일 학생증 이미지에서 추출된 텍스트입니다:\n\n"
            f"{combined_text}\n\n"
            "이 이미지가 모바일 학생증인지 판단해주세요. 만약 모바일 학생증이 아니라면 모바일 학생증이 아님이라고 출력해주세요"
            "만약 모바일 학생증이라면 학번, 이름, 학과, 재학여부를 다음 형식으로 한줄만 출력해주시고 이름은 학번 학과로 추정되는 텍스트를 제외하고 나머지 텍스트중 하나로 해주시는데 한글로 된 세글자인 텍스트가 이름일 확률이 높습니다: "
            "'학번: [학번], 이름: [이름], 학과: [학과], 재학여부: [재학여부]'. "
            "재학여부는 '재학', '휴학', '졸업' 중 하나로 출력해주세요. "
            "알 수 없는 정보는 '알 수 없음'으로 출력하세요."
        )

        api_result = analyze_text_with_gpt(gpt_prompt, API_KEY)
        if api_result:
            print(f"'{filename}': {api_result}")
        else:
            print(f"GPT API 분석 실패 for '{filename}'")

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os

import streamlit as st
from datetime import datetime

def get_APIkey():
    with open("API_KEY.txt") as f:
        API_KEY = f.read()
    return API_KEY

def send_request(image_path, API_KEY):
    PATH = os.getcwd() + '\\images'
    images = os.listdir(PATH)
    print(image_path)
    if image_path not in images:
        raise FileNotFoundError
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    now_image = genai.upload_file(path = f"images\\{image_path}", display_name = image_path)
    image_file = genai.get_file(name = now_image.name)
    response = model.generate_content(
        [image_file, "주어지는 이미지가 모바일 학생증 이미지인지 판단해 줘. 학번, 이름 정보가 없다면 모바일 학생증이 아니야. 만약 모바일 학생증 이미지라면 학교, 학번, 이름, 학과, 재학여부를 찾아 다음 형식으로 출력해 줘: \'학교: [학교], 학번: [학번], 이름: [이름], 학과: [학과], 재학여부: [재학여부]\'. 재학여부는 \'재학\', \'휴학\', \'졸업\' 중 하나로 출력해 줘. 이미지를 통해 알 수 없는 정보는 \'알 수 없음\' 이라고 출력해 줘. 읽은 글자가 문맥에 맞지 않거나 잘못 읽은 걸로 판단된다면 딘어를 유추하거나 \'알 수 없음\' 으로 처리해."],
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
    )
    print(image_path)
    try:
        return response.text
    except:
        raise Exception("알 수 없는 이유로 응답을 받지 못했습니다.")
    
img_file = st.file_uploader('전자 학생증의 캡쳐화면을 업로드하세요.', type=['png','jpg', 'jpeg'])
API_KEY = get_APIkey()

if img_file:
    tmp = st.info('처리 중 ..')
    file_name, file_type = img_file.name.split('.')
    file_name += str(datetime.now().timestamp()).replace('.', '') + '.' + file_type
    img_file.name = file_name
    img_path = os.path.join(os.getcwd(), 'images', img_file.name)
    with open(img_path, 'wb') as f:
        f.write(img_file.getbuffer())
    
    try:
        result = send_request(file_name, API_KEY)
        st.success(result)
    except FileNotFoundError:
        st.error('파일을 저장하지 못했습니다.')
    except Exception as e:
        st.error(e)
    finally:
        tmp.empty()
    
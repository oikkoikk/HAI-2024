import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
from io import BytesIO
import base64
import traceback

import streamlit as st
from datetime import datetime

def get_APIkey():
    # return os.environ.get('Gemini_KEY')
    return st.secrets['Gemini_KEY']

def send_request(image, API_KEY):
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    base64_image = base64.b64encode(image.getvalue()).decode('utf-8')
    response = model.generate_content(
        contents={
                "parts":[
                    {
                        "text":"주어지는 이미지가 모바일 학생증 이미지인지 판단해 줘. 학번, 이름 정보가 없다면 모바일 학생증이 아니야. 만약 모바일 학생증 이미지라면 학교, 학번, 이름, 학과, 재학여부를 찾아 다음 형식으로 출력해 줘: \'학교: [학교], 학번: [학번], 이름: [이름], 학과: [학과], 재학여부: [재학여부]\'. 재학여부는 \'재학\', \'휴학\', \'졸업\' 중 하나로 출력해 줘. 이미지를 통해 알 수 없는 정보는 \'알 수 없음\' 이라고 출력해 줘. 읽은 글자가 문맥에 맞지 않거나 잘못 읽은 걸로 판단된다면 딘어를 유추하거나 \'알 수 없음\' 으로 처리해.",
                    },
                    {
                        "inline_data" :{
                            "mime_type" : image.type,
                            "data":base64_image
                        }
                    }
                ]
            },
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
    )
    # print(image_path)
    try:
        return response.text
    except:
        raise RuntimeError("알 수 없는 이유로 응답을 받지 못했습니다.")
    
img_file = st.file_uploader('전자 학생증의 캡쳐화면을 업로드하세요.', type=['png','jpg', 'jpeg'])
API_KEY = get_APIkey()

if img_file:
    tmp = st.info('처리 중 ..')
    
    try:
        result = send_request(img_file, API_KEY)
        st.success(result)
        st.image(img_file)
    except FileNotFoundError:
        st.error('파일을 저장하지 못했습니다.')
    except RuntimeError as e:
        st.error(e)
    except:
        st.error('처리 과정에서 에러가 발생했습니다.')
        traceback.print_exc()
    finally:
        tmp.empty()
    
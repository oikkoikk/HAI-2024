import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os

with open("API_KEY.txt") as f:
    API_KEY = f.read()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

PATH = os.getcwd() + '\\images'
images = os.listdir(PATH)

out = ''

for image_path in images:
    now_image = genai.upload_file(path = f"images\\{image_path}", display_name = image_path)
    image_file = genai.get_file(name = now_image.name)
    response = model.generate_content(
        [image_file, "모바일 학생증 이미지에서 학번, 이름, 학과, 재학여부를 찾아 다음 형식으로 출력해 줘: \'학번: [학번], 이름: [이름], 학과: [학과], 재학여부: [재학여부]\'. 재학여부는 \'재학\', \'휴학\', \'졸업\' 중 하나로 출력해 줘. 이미지를 통해 알 수 없는 정보는 \'알 수 없음\' 이라고 출력해 줘. 읽은 글자가 문맥에 맞지않거나 잘못 읽은 걸로 판단된다면 딘어를 유추하거나 \'알 수 없음\' 으로 처리해."],
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
    )
    print(image_path)
    out += image_path + '\n'
    out += str(response) + '\n\n'
    try:
        print(response.text)
    except:
        print('실패. 왜? 모름.')

with open("output.txt", "w") as f:
    f.write(out)
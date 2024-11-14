from pororo import Pororo

path = "test_img\\7.png" # Test image path

# OCR
ocr = Pororo(task="ocr", lang="ko")
ocr_result = ocr(path)

print(ocr_result)
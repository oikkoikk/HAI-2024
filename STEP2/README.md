# 가상환경 : conda

> 파이썬 버전 = 3.6
> CUDA 버전 = 미정

# 사용 방법

처음 실행시, 가상환경을 만듭니다.
```sh
cd ./STEP2
conda env create -f environment.yml
conda activate hai-2024-proj-step-2
pip install -e ./pororo
```

그렇지 않다면, 가상환경을 실행합니다.
```sh
conda activate hai-2024-proj-step-2
```

```py
import step2
step2.analyze_image(path)
```

# 코드 설명

## `step2.py`

이미지 데이터를 Pororo OCR과 OpenAI GPT API를 활용해 학생증 정보를 추출하고 포맷팅된 결과를 반환.

### 주요 사용 함수
- `analyze_image(image_path: str) -> dict`  
  - **입력**: 이미지 파일 경로 (`image_path`)  
  - **출력**: 학번, 이름, 학과, 재학 여부가 포함된 포맷팅된 결과 (`dict`)

## `pororo_usage.py`
pororo ocr 기능의 기본적인 사용법

## `accuracy_checker.py`
`step2.py`에 있는 함수에 따른 결과에 대한 정확도를 측정하는 코드입니다.


# 참고

충돌이 많아서 꽤 걸렸어요,,

[Pororo 설치 오류 - Velog](https://velog.io/@yg-kim-korean/Pororo-%EC%84%A4%EC%B9%98-%EC%98%A4%EB%A5%98)

[Pororo ASR(Auto Speech Recognition) 설치를 위한 고군분투기 - Velog](https://velog.io/@ldc/Pororo-ASRAuto-Speech-Recognition-%EC%84%A4%EC%B9%98%EB%A5%BC-%EC%9C%84%ED%95%9C-%EA%B3%A0%EA%B5%B0%EB%B6%84%ED%88%AC%EA%B8%B0)


## conda 관련 명령어

### 가상환경 활성화 / 비활성화
다음 코드를 통해 가상환경을 활성화합니다.
```sh
conda activate hai-2024-proj-step-2
```

다음 코드를 통해 가상환경을 비활성화합니다.
```sh
conda deactivate
```

### 가상환경 저장
```sh
conda env export --name hai-2024-proj-step-2 > environment.yml
```

### 가상환경 불러오기 (주의!!)

처음 로드시 다음을 실행합니다.
```sh
conda env create -f environment.yml
```

(주의!!) 현재 폴더 안에 있는 `pororo` 모듈(오류 수정)을 설치해야 합니다
```sh
pip install -e ./pororo
```

가상환경이 이미 있을 때는 다음을 실행합니다.
```sh
conda env update --name hai-2024-proj-step-2 --file environment.yml
```

### 가상환경 삭제
```sh
conda env remove --name hai-2024-proj-step-2
```

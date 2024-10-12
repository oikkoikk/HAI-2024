# 가상환경 : conda

> 파이썬 버전 = 3.6
> CUDA 버전 = 미정

## 실행방법

### 가상환경 활성화 / 비활성화
다음 코드를 통해 가상환경을 활성화합니다.
```
conda activate hai-2024-proj-step-2
```

다음 코드를 통해 가상환경을 비활성화합니다.
```
conda deactivate
```

### 가상환경 저장
```
conda env export --name hai-2024-proj-step-2 > environment.yml
```

### 가상환경 불러오기 (주의!!)

처음 로드시 다음을 실행합니다.
```
conda env create -f environment.yml
```

(주의!!) 현재 폴더 안에 있는 `pororo` 모듈(오류 수정)을 설치해야 합니다
```
pip install -e ./pororo
```

가상환경이 이미 있을 때는 다음을 실행합니다.
```
conda env update --name hai-2024-proj-step-2 --file environment.yml
```

### 가상환경 삭제
```
conda env remove --name hai-2024-proj-step-2
```

# 참고한 링크

충돌이 많아서 꽤 걸렸어요,,

[Pororo 설치 오류 - Velog](https://velog.io/@yg-kim-korean/Pororo-%EC%84%A4%EC%B9%98-%EC%98%A4%EB%A5%98)

[Pororo ASR(Auto Speech Recognition) 설치를 위한 고군분투기 - Velog](https://velog.io/@ldc/Pororo-ASRAuto-Speech-Recognition-%EC%84%A4%EC%B9%98%EB%A5%BC-%EC%9C%84%ED%95%9C-%EA%B3%A0%EA%B5%B0%EB%B6%84%ED%88%AC%EA%B8%B0)
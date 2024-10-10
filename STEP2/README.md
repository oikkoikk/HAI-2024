# 가상환경 : conda

> 파이썬 버전 = 3.8
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

### 가상환경 불러오기

처음 로드시 다음을 실행합니다.
```
conda env create -f environment.yml
```

가상환경이 이미 있을 때는 다음을 실행합니다.
```
conda env update --name hai-2024-proj-step-2 --file environment.yml
```

### 가상환경 삭제
```
conda env remove --name hai-2024-proj-step-2
```
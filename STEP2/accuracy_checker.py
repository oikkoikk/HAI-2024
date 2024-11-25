import pandas as pd
import numpy as np

def load_and_preprocess_data(ground_truth_path, prediction_path):
    """
    두 CSV 파일을 로드하고 전처리합니다.
    """
    # CSV 파일 로드
    gt_df = pd.read_csv(ground_truth_path)
    pred_df = pd.read_csv(prediction_path)
    
    # 경로에서 파일명만 추출하여 매칭에 사용
    gt_df['image_name'] = gt_df['path'].apply(lambda x: x.split('/')[-1])
    pred_df['image_name'] = pred_df['path'].apply(lambda x: x.split('/')[-1])
    
    return gt_df, pred_df

def calculate_accuracy(gt_df, pred_df):
    """
    각 필드별 정확도를 계산합니다.
    """
    # 비교할 컬럼들
    columns = ['university', 'department', 'name', 'student-id']
    
    # 결과 저장용 딕셔너리
    accuracies = {}
    error_cases = {}
    
    for col in columns:
        correct = 0
        total = 0
        errors = []
        
        for idx in range(len(gt_df)):
            gt_value = str(gt_df.iloc[idx][col]).strip().lower()
            pred_value = str(pred_df.iloc[idx][col]).strip().lower()
            
            # 빈 값 처리
            if gt_value in ['nan', ''] and pred_value in ['알 수 없음', 'nan', '']:
                correct += 1
            elif gt_value == pred_value:
                correct += 1
            else:
                errors.append({
                    'image': gt_df.iloc[idx]['image_name'],
                    'ground_truth': gt_value,
                    'prediction': pred_value
                })
            total += 1
        
        accuracy = (correct / total) * 100
        accuracies[col] = accuracy
        error_cases[col] = errors
    
    # 전체 정확도 계산
    total_accuracy = sum(accuracies.values()) / len(accuracies)
    
    return accuracies, total_accuracy, error_cases

def print_accuracy_report(accuracies, total_accuracy, error_cases):
    """
    정확도 결과를 보기 좋게 출력합니다.
    """
    print("\n=== 정확도 분석 결과 ===")
    print(f"\n전체 정확도: {total_accuracy:.2f}%")
    print("\n각 필드별 정확도:")
    for field, accuracy in accuracies.items():
        print(f"- {field}: {accuracy:.2f}%")
    
    print("\n=== 오류 사례 분석 ===")
    for field, errors in error_cases.items():
        if errors:
            print(f"\n{field} 필드 오류 사례 (총 {len(errors)}개):")
            for error in errors[:5]:  # 처음 5개의 오류만 출력
                print(f"이미지: {error['image']}")
                print(f"정답: {error['ground_truth']}")
                print(f"예측: {error['prediction']}")
                print("-" * 40)

def main():
    # 파일 경로
    ground_truth_path = "/Users/mac/Downloads/dataset/data.csv"  # 정답 파일
    prediction_path = "student_data.csv"        # AI 모델 예측 파일
    
    try:
        # 데이터 로드 및 전처리
        gt_df, pred_df = load_and_preprocess_data(ground_truth_path, prediction_path)
        
        # 정확도 계산
        accuracies, total_accuracy, error_cases = calculate_accuracy(gt_df, pred_df)
        
        # 결과 출력
        print_accuracy_report(accuracies, total_accuracy, error_cases)
        
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
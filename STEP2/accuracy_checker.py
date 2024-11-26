import numpy as np
import pandas as pd

def evaluate_accuracy(ground_truth_path, prediction_path):
    """학생증 분석 결과의 정확도를 평가하는 함수"""
    try:
        # CSV 파일 로드
        gt_df = pd.read_csv(ground_truth_path)
        pred_df = pd.read_csv(prediction_path)
        
        # 이미지 파일명으로 매칭
        gt_df['image_name'] = gt_df['path'].apply(lambda x: x.split('/')[-1])
        pred_df['image_name'] = pred_df['path'].apply(lambda x: x.split('/')[-1])
        
        # 평가할 필드들
        fields = ['university', 'department', 'name', 'student-id']
        accuracies = {}
        error_cases = {}
        
        # 각 필드별 정확도 계산
        for field in fields:
            correct = 0
            total = 0
            errors = []
            
            for idx in range(len(gt_df)):
                gt_value = str(gt_df.iloc[idx][field]).strip().lower()
                pred_value = str(pred_df.iloc[idx][field]).strip().lower()
                
                if gt_value in ['nan', ''] and pred_value in ['none', 'nan', '']:
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
            accuracies[field] = accuracy
            error_cases[field] = errors
        
        # 전체 정확도 계산
        total_accuracy = sum(accuracies.values()) / len(accuracies)
        
        # 결과 출력
        print("\n=== 정확도 분석 결과 ===")
        print(f"전체 정확도: {total_accuracy:.2f}%\n")
        print("필드별 정확도:")
        for field, acc in accuracies.items():
            print(f"- {field}: {acc:.2f}%")
        
        print("\n=== 오류 사례 ===")
        for field, errors in error_cases.items():
            if errors:
                print(f"\n{field} 필드 오류 ({len(errors)}개):")
                for error in range(0, min(15, len(errors)), 3):  # 처음 3개의 오류만 출력
                    print(f"이미지: {error['image']}")
                    print(f"정답: {error['ground_truth']}")
                    print(f"예측: {error['prediction']}")
                    print("-" * 40)
        
        return total_accuracy, accuracies, error_cases
        
    except Exception as e:
        print(f"평가 중 오류 발생: {e}")
        return None, None, None

if __name__ == "__main__":
    
    # 정확도 평가
    ground_truth_path = "/Users/mac/Downloads/dataset/data.csv"
    prediction_path = "analyzed_results.csv"
    total_acc, field_acc, errors = evaluate_accuracy(ground_truth_path, prediction_path)
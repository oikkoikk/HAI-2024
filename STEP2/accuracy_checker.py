import pandas as pd
import numpy as np
import os


def calculate_accuracy(ground_truth_path, prediction_path):
    """
    각 필드별 정확도를 계산합니다.
    """

    gt_df = pd.read_csv(ground_truth_path)
    pred_df = pd.read_csv(prediction_path)

    # 비교할 컬럼들
    columns = ['university', 'department', 'name', 'student-id']
    
    # 결과 저장용 딕셔너리
    accuracies = {}
    error_cases = {}
    
    # gt_df에서 pred_df에 없는 index 걸러내기
    gt_df = gt_df[gt_df['index'].isin(pred_df['index'])]

    for column in columns:
        # 각 필드별 정확도 계산
        correct_predictions = ((gt_df.set_index('index')[column] == pred_df.set_index('index')[column]) | 
                       (gt_df.set_index('index')[column].isna() & pred_df.set_index('index')[column].isna())).sum()
        total_predictions = len(gt_df)
        accuracy = (correct_predictions / total_predictions) * 100
        accuracies[column] = accuracy
        
        # 오류 사례 저장
        errors = []
        for idx, row in gt_df.iterrows():
            if row[column] != pred_df.loc[pred_df['index'] == row['index'], column].values[0]:
                if pd.isna(row[column]) and pd.isna(pred_df.loc[pred_df['index'] == row['index'], column].values[0]):
                    continue
                errors.append({
                    'ground_truth': row[column],
                    'prediction': pred_df.loc[pred_df['index'] == row['index'], column].values[0]
                })
                print(pred_df.loc[pred_df['index'] == row['index'], column].values[0])
        error_cases[column] = errors

    # 전체 정확도 계산
    total_correct_predictions = sum([accuracies[col] for col in columns]) / len(columns)
    total_accuracy = total_correct_predictions

    print_accuracy_report(accuracies, total_accuracy, error_cases)
    

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
                print(f"정답: {error['ground_truth']}")
                print(f"예측: {error['prediction']}")
                print("-" * 40)

def predict_student_datas(csv_path, output_path):
    import step2 # speed issue
    df = pd.read_csv(csv_path)

    # 데이터 줄이기
    sample_number = 1
    sampled_df = df.groupby('university').apply(lambda x: x.sample(min(len(x), sample_number))).reset_index(drop=True)

    results = []

    for idx, row in sampled_df.iterrows():
        index = row['index']
        student_id = row['student-id']
        name = row['name']
        department = row['department']
        university = row['university']
        path = row['path']

        # 학과 예측
        predict = step2.analyze_image(path)

        # 결과 저장
        result = {
            'index': index,
            'student-id': student_id,
            'name': name,
            'department': department,
            'university': university,
            'status': '재학'
        }
        results.append(result)

    # 결과를 DataFrame으로 변환
    results_df = pd.DataFrame(results)
    
    # CSV 파일로 저장
    results_df.to_csv(output_path, index=False)
        
    

def main():
    # 파일 경로
    ground_truth_path = r"./dataset/data.csv"  # 정답 파일
    prediction_path = r"./student_data.csv" # AI 모델 예측 파일
    
    try:
        calculate_accuracy(ground_truth_path, prediction_path)
        
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        raise e

if __name__ == "__main__":
    ground_truth_path = r"./dataset/data.csv"  # 정답 파일
    prediction_path = r"./student_data.csv" # AI 모델 예측 파일
    if not os.path.exists(prediction_path):
        predict_student_datas(ground_truth_path, prediction_path)
    main()
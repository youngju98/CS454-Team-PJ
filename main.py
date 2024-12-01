import os
import json
from file_reader import read_input_files
from perplexity_api import generate_feedback
from feedback_writer import write_feedback

def main():
    # 입력 데이터 읽기
    base_dir = 'data'
    output_dir = 'feedback'
    problems = read_input_files(base_dir)

    # 각 문제에 대해 피드백 생성
    for problem_name, problem_data in problems.items():
        for i, solution in enumerate(problem_data['solutions'], 1):
            # 첫 번째 피드백 생성 (커버리지 데이터 없이)
            feedback1 = generate_feedback(
                problem_data['description'],
                problem_data['skeleton'],
                solution
            )

            # 두 번째 피드백 생성 (커버리지 데이터 포함)
            feedback2 = generate_feedback(
                problem_data['description'],
                problem_data['skeleton'],
                solution,
                problem_data['coverage'][i-1]
            )

            # 피드백 저장
            write_feedback(os.path.join(output_dir, f"{problem_name}_solution_{i}_feedback1.txt"), feedback1)
            write_feedback(os.path.join(output_dir, f"{problem_name}_solution_{i}_feedback2.txt"), feedback2)
            
            # 진행 상황 출력
            print(f"문제 '{problem_name}'의 솔루션 {i}에 대한 피드백 생성 완료")

        # 각 문제가 끝날 때마다 구분선 출력
        print(f"--- 문제 '{problem_name}'에 대한 모든 솔루션 피드백 생성 완료 ---")

if __name__ == "__main__":
    main()
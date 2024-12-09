import os
import json
import concurrent.futures
from collections import defaultdict
from file_reader import read_input_files
from perplexity_api import generate_feedback
from feedback_writer import write_feedback

def process_solution(problem_name, i, solution, problem_data, output_dir):
    try:
        # 첫 번째 피드백 생성 (커버리지 데이터 없이)
        feedback1 = generate_feedback(
            problem_data['description'],
            problem_data['skeleton'],
            problem_data['feedback_example'],
            solution
        )

        # 두 번째 피드백 생성 (커버리지 데이터 포함)
        feedback2 = generate_feedback(
            problem_data['description'],
            problem_data['skeleton'],
            problem_data['feedback_example'],
            solution,
            problem_data['coverage'][i-1]
        )

        # 피드백 저장
        feedback1_filename = os.path.join(output_dir, f"{problem_name}_solution_{i}_feedback1.txt")
        write_feedback(feedback1_filename, feedback1)

        feedback2_filename = os.path.join(output_dir, f"{problem_name}_solution_{i}_feedback2.txt")
        write_feedback(feedback2_filename, feedback2)

        return f"문제 '{problem_name}'의 솔루션 {i}에 대한 피드백 생성 완료"
    except Exception as e:
        return f"에러 발생: 문제 '{problem_name}'의 솔루션 {i} 처리 중 {type(e).__name__} 발생\n에러 메시지: {str(e)}"

def main():
    # 입력 데이터 읽기
    base_dir = 'data'
    output_dir = 'feedback'
    problems = read_input_files(base_dir)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = {}
        solution_counts = {problem_name: len(problem_data['solutions']) for problem_name, problem_data in problems.items()}
        completed_solutions = defaultdict(int)

        for problem_name, problem_data in problems.items():
            for i, solution in enumerate(problem_data['solutions'], 1):
                future = executor.submit(process_solution, problem_name, i, solution, problem_data, output_dir)
                futures[future] = problem_name
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            print(result)
            
            problem_name = futures[future]
            completed_solutions[problem_name] += 1
            
            if completed_solutions[problem_name] == solution_counts[problem_name]:
                print(f"--- 문제 '{problem_name}'에 대한 모든 솔루션 피드백 생성 완료 ---")

if __name__ == "__main__":
    main()
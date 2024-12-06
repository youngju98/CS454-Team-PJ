import os
import concurrent.futures
from collections import defaultdict
from file_reader import read_feedback_files
from perplexity_api import generate_feedback_compare
from feedback_writer import write_feedback

def process_feedback_comparison(problem_name, solution_num, feedbacks, output_dir):
    try:
        feedback1 = feedbacks[problem_name][solution_num]['1']
        feedback2 = feedbacks[problem_name][solution_num]['2']
        
        comparison = generate_feedback_compare(feedback1, feedback2)
        
        comparison_filename = os.path.join(output_dir, f"{problem_name}_solution_{solution_num}_feedback_compare.txt")
        write_feedback(comparison_filename, comparison)
        
        return f"문제 '{problem_name}'의 솔루션 {solution_num}에 대한 피드백 비교 완료"
    except Exception as e:
        return f"에러 발생: 문제 '{problem_name}'의 솔루션 {solution_num} 처리 중 {type(e).__name__} 발생\n에러 메시지: {str(e)}"

def main():
    feedback_dir = 'feedback'
    output_dir = 'feedback_compare'
    feedbacks = read_feedback_files(feedback_dir)
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = {}
        solution_counts = {problem_name: len(problem_data) for problem_name, problem_data in feedbacks.items()}
        completed_solutions = defaultdict(int)
        
        for problem_name, problem_data in feedbacks.items():
            for solution_num in problem_data:
                future = executor.submit(process_feedback_comparison, problem_name, solution_num, feedbacks, output_dir)
                futures[future] = problem_name
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            print(result)
            problem_name = futures[future]
            completed_solutions[problem_name] += 1
            
            if completed_solutions[problem_name] == solution_counts[problem_name]:
                print(f"--- 문제 '{problem_name}'에 대한 모든 솔루션 피드백 비교 완료 ---")

if __name__ == "__main__":
    main()
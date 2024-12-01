import os

def read_input_files(base_dir):
    problems = {}
    for problem_folder in os.listdir(base_dir):
        problem_path = os.path.join(base_dir, problem_folder)
        if os.path.isdir(problem_path):
            problems[problem_folder] = {
                'description': None,
                'skeleton': None,
                'solutions': [],
                'coverage': []
            }
            
            # 설명 파일 읽기
            with open(os.path.join(problem_path, 'description.txt'), 'r') as f:
                problems[problem_folder]['description'] = f.read()
            
            # 스켈레톤 코드 읽기
            with open(os.path.join(problem_path, 'skeleton.py'), 'r') as f:
                problems[problem_folder]['skeleton'] = f.read()
            
            # 솔루션 파일들 읽기
            solution_dir = os.path.join(problem_path, 'solution')
            for solution_file in sorted(os.listdir(solution_dir)):
                with open(os.path.join(solution_dir, solution_file), 'r') as f:
                    problems[problem_folder]['solutions'].append(f.read())
            
            # 커버리지 파일들 읽기
            coverage_dir = os.path.join(problem_path, 'coverage')
            for coverage_file in sorted(os.listdir(coverage_dir)):
                with open(os.path.join(coverage_dir, coverage_file), 'r') as f:
                    problems[problem_folder]['coverage'].append(f.read())
    
    return problems
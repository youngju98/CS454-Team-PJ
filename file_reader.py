import os
import chardet

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
            
            # 인코딩 디버깅
            solution_dir = os.path.join(problem_path, 'solution')
            for solution_file in sorted(os.listdir(solution_dir)):
                file_path = os.path.join(solution_dir, solution_file)
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as rawdata:
                        result = chardet.detect(rawdata.read(10000))
                    print(f"파일 '{solution_file}'의 인코딩: {result['encoding']}")
            coverage_dir = os.path.join(problem_path, 'coverage')
            for coverage_file in sorted(os.listdir(coverage_dir)):
                file_path = os.path.join(coverage_dir, coverage_file)
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as rawdata:
                        result = chardet.detect(rawdata.read(10000))
                    print(f"파일 '{coverage_file}'의 인코딩: {result['encoding']}")
            
            # 솔루션 파일들 읽기
            solution_dir = os.path.join(problem_path, 'solution')
            for solution_file in sorted(os.listdir(solution_dir)):
                file_path = os.path.join(solution_dir, solution_file)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            problems[problem_folder]['solutions'].append(f.read())
                    except UnicodeDecodeError:
                        # UTF-8로 읽기 실패시 ASCII로 시도
                        try:
                            with open(file_path, 'r', encoding='ascii') as f:
                                problems[problem_folder]['solutions'].append(f.read())
                        except UnicodeDecodeError:
                            print(f"파일 '{solution_file}'를 UTF-8, ASCII으로 읽을 수 없음")
            
            # 커버리지 파일들 읽기
            coverage_dir = os.path.join(problem_path, 'coverage')
            for coverage_file in sorted(os.listdir(coverage_dir)):
                file_path = os.path.join(coverage_dir, coverage_file)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            problems[problem_folder]['coverage'].append(f.read())
                    except UnicodeDecodeError:
                        # UTF-8로 읽기 실패시 ASCII로 시도
                        try:
                            with open(file_path, 'r', encoding='ascii') as f:
                                problems[problem_folder]['coverage'].append(f.read())
                        except UnicodeDecodeError:
                            print(f"파일 '{coverage_file}'를 UTF-8, ASCII으로 읽을 수 없음")
    
    return problems

def read_feedback_files(feedback_dir):
    feedbacks = {}
    for feedback_file in os.listdir(feedback_dir):
        if feedback_file.endswith('.txt'):
            file_path = os.path.join(feedback_dir, feedback_file)
            problem_name = feedback_file.split('_solution_')[0]
            solution_num = feedback_file.split('_solution_')[1].split('_')[0]
            feedback_type = feedback_file.split('_feedback')[1].split('.')[0]
            
            if problem_name not in feedbacks:
                feedbacks[problem_name] = {}
            if solution_num not in feedbacks[problem_name]:
                feedbacks[problem_name][solution_num] = {}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                feedbacks[problem_name][solution_num][feedback_type] = f.read()
    
    return feedbacks
import os

def write_feedback(filename, feedback):
    # 파일이 위치할 디렉토리가 없으면 생성
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(feedback)
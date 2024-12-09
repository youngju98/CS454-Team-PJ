import requests
from config import API_KEY

def generate_feedback(description, skeleton, solution, feedback_example, coverage=None):
    # Perplexity API 엔드포인트 및 API 키 설정
    API_ENDPOINT = "https://api.perplexity.ai/chat/completions"

    # API 요청 헤더
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

#     # System 메시지 준비
#     system_message = """당신은 프로그래밍 코드 리뷰어입니다. 주어진 알고리즘 문제, 스켈레톤 코드, 코드 커버리지 데이터(있는 경우에만), 그리고 제출된 솔루션을 분석하여 상세한 피드백을 제공해야 합니다. 피드백은 다음 6가지 카테고리로 구성되어야 합니다:

# 1. 코드 구현 정확도 : 실제 문제를 정확하게 풀고 예외나 에러를 모두 잘 처리하여 제대로 실행되는 코드 구현인지 피드백 
# 2. 코드 스타일 : 변수명 설정, 띄어쓰기, 괄호 처리, 주석 처리 등 코드 스타일이 표준 규격에 맞게끔 적용되었는지 피드백
# 3. 불필요 코드 : 실행되지 않는 코드, 불필요한 코드가 있는지에 대한 검토와 함께 개선 방안 피드백 
# 4. 코드 효율성 : 자주 쓰이는 코드는 함수로 모듈화 하여 구현했는지, 표준 라이브러리로 코드를 줄이거나, 효율화 할 수 있는 부분이 있는지 피드백 
# 5. 고려하지 못한 케이스 : 알고리즘에 대해 제대로 작동하기는 하지만, 알고리즘의 특정한 케이스를 고려하지 못한 부분이 있는 코드 구현인지 피드백 
# 6. 종합 피드백 : 결론으로서, 전체 피드백에 대해 요약해서 설명

# 각 카테고리에 대해 구체적이고 정확한 피드백을 제공하세요. 각 카테고리 별 피드백은 필요한 경우 최대 6문장까지로 작성하세요. 피드백 외의 다른 텍스트는 포함하지 마세요."""

#     # System 메시지 준비
#     system_message = """You are a programming code reviewer. You should analyze the given algorithm problem, skeleton code, code coverage data (if available), and submitted solution to provide detailed feedback. The feedback should be structured into the following 6 categories:
    
# 1. Code Implementation Accuracy: Feedback on whether the code accurately solves the actual problem, handles all exceptions and errors, and executes properly.
# 2. Code Style: Feedback on whether variable naming, spacing, bracket handling, commenting, etc. are applied according to standard conventions.
# 3. Unnecessary Code: Review and provide improvement suggestions for any code that is not executed or unnecessary.
# 4. Code Efficiency: Feedback on whether frequently used code is modularized into functions, if standard libraries could be used to reduce code, or if there are areas that could be optimized.
# 5. Unconsidered Cases: Feedback on whether the code implementation, while functioning properly for the algorithm, fails to consider specific cases of the algorithm.
# 6. Overall Feedback: As a conclusion, summarize the overall feedback.

# Provide specific and accurate feedback for each category. Write up to a maximum of 6 sentences for each category's feedback if necessary. Do not include any text other than the feedback.
# """

    # System 메시지 준비
    system_message = """You are a programming code reviewer. Your task is to analyze the given algorithm problem, skeleton code, feedback example, code coverage data (if available), and submitted solution to provide detailed feedback. 
For each category, you should provide feedback in the following format:
"line number": {
    "reason": "Detailed explanation",
    "reason_num": [reason numbers],
    "improved_code": "Suggested improvement"
}

Using this format, feedback should be given on a specific line of the solution, explaining why and how it needs to be improved. Additionally, it should clearly list which of the six reasons fall under the three categories below.

6 reasons : {
Unnecessary code:
reason_number 1: Duplicated code that is inefficient due to repetition.
reason_number 2: Unused code, such as variables or functions that are declared but never used.
Bad coding style:
reason_number 3: Poor variable or function names, e.g., using 'a', 'b' instead of descriptive names.
reason_number 4: Overuse of global variables, making the code's intention unclear.
Logical fault:
reason_number 5: Logical errors where the code doesn't execute as intended.
reason_number 6: Failure to handle edge cases or extreme input values.
}
"line number" should contain only one number indicating which line is being referenced for feedback. "Detailed explanation" should provide a detailed reason for the need for improvement in a maximum of two sentences. The reason numbers should be presented as an array of numbers corresponding to the six reasons mentioned above. "Suggested improvement" should propose how to modify the code on that line based on the reasons provided.
"""

    # User 메시지 준비
    user_message = f"""
problem description:
{description}

skeleton code:
{skeleton}

feedback example:
{feedback_example}

submitted solution:
{solution}

{"code coverage data:" if coverage else ""}
{coverage if coverage else ""}

Based on the information above, generate feedback according to the format explained in the system message. Your answer must only contain data in the format form. And the output should be in the form of a json file, with no other sentences."""

    # API 요청 데이터 준비
    data = {
        "model": "llama-3.1-sonar-huge-128k-online",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    }

    # API 요청 보내기
    response = requests.post(API_ENDPOINT, headers=headers, json=data)

    # 응답 처리
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"

def generate_feedback_compare(feedback1, feedback2):
    API_ENDPOINT = "https://api.perplexity.ai/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_message = """당신은 각기 다른 사람이 작성한 프로그래밍 코드 리뷰에 대한 피드백을 비교 분석하는 전문가입니다. 두 개의 피드백을 비교하여 다음 항목들에 대해 분석해주세요:

1. 피드백 일치도: 두 피드백이 얼마나 일치하는지 백분율로 표현해
2. 주요 차이점: 두 피드백 간의 주요한 차이점을 설명
3. 추가 인사이트: 각 피드백에서 추가로 제공된 인사이트가 있다면 어떤 피드백에서 어떤 인사이트가 있었는지 설명
4. 코드 커버리지 데이터 유용성 : 두 피백은 알고리즘 문제의 설명, 스켈레톤 코드, 제출된 솔루션을 분석해서 생성된 피드백이야. 단, 두번째 피드백은 첫번째 피드백과 달리 코드 커버리지 데이터를 추가로 받아 어떤 함수에서 어떤 코드가 실행되지 않았는지도 분석했어. 두 피드백을 분석했을 때 두번째 피드백에서 코드 커버리지 데이터가 개선된 피드백을 생성하는데 유용했는지 분석해줘. 
5. 종합 분석: 두 피드백을 종합적으로 분석하여 각 피드백 중 어떤 것이 더 나은지, 구체적인 정보를 표현했는지 설명

각 항목에 대해 구체적이고 정확한 분석을 제공하세요. 각 카테고리 별 설명은 필요한 경우 최대 6문장까지로 작성하세요. 분석 외의 다른 텍스트는 포함하지 마세요."""

    user_message = f"""
첫 번째 피드백:
{feedback1}

두 번째 피드백:
{feedback2}

위의 두 피드백을 비교 분석하여 앞서 설명한 4가지 항목에 맞춰 분석 결과를 생성해주세요."""

    data = {
        "model": "llama-3.1-sonar-huge-128k-online",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    }
    
    response = requests.post(API_ENDPOINT, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"
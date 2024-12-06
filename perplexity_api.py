import requests
from config import API_KEY

def generate_feedback(description, skeleton, solution, coverage=None):
    # Perplexity API 엔드포인트 및 API 키 설정
    API_ENDPOINT = "https://api.perplexity.ai/chat/completions"

    # API 요청 헤더
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # System 메시지 준비
    system_message = """당신은 프로그래밍 코드 리뷰어입니다. 주어진 알고리즘 문제, 스켈레톤 코드 (있는 경우에만), 그리고 제출된 솔루션을 분석하여 상세한 피드백을 제공해야 합니다. 피드백은 다음 6가지 카테고리로 구성되어야 합니다:

1. 코드 구현 정확도 : 실제 문제를 정확하게 풀고 예외나 에러를 모두 잘 처리하여 제대로 실행되는 코드 구현인지 피드백 
2. 코드 스타일 : 변수명 설정, 띄어쓰기, 괄호 처리, 주석 처리 등 코드 스타일이 표준 규격에 맞게끔 적용되었는지 피드백
3. 불필요 코드 : 실행되지 않는 코드, 불필요한 코드가 있는지에 대한 검토와 함께 개선 방안 피드백 
4. 코드 효율성 : 자주 쓰이는 코드는 함수로 모듈화 하여 구현했는지, 표준 라이브러리로 코드를 줄이거나, 효율화 할 수 있는 부분이 있는지 피드백 
5. 고려하지 못한 케이스 : 알고리즘에 대해 제대로 작동하기는 하지만, 알고리즘의 특정한 케이스를 고려하지 못한 부분이 있는 코드 구현인지 피드백 
6. 종합 피드백 : 결론으로서, 전체 피드백에 대해 요약해서 설명

각 카테고리에 대해 구체적이고 정확한 피드백을 제공하세요. 각 카테고리 별 피드백은 필요한 경우 최대 6문장까지로 작성하세요. 피드백 외의 다른 텍스트는 포함하지 마세요."""

    # User 메시지 준비
    user_message = f"""
문제 설명:
{description}

스켈레톤 코드:
{skeleton}

제출된 솔루션:
{solution}

{"커버리지 데이터:" if coverage else ""}
{coverage if coverage else ""}

위의 정보를 바탕으로 앞서 설명한 6가지 카테고리에 맞춰 피드백을 생성해주세요."""

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
4. 종합 분석: 두 피드백을 종합적으로 분석하여 각 피드백 중 어떤 것이 더 나은지, 구체적인 정보를 표현했는지 설명

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
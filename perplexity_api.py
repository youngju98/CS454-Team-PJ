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
    system_message = """당신은 프로그래밍 코드 리뷰어입니다. 주어진 알고리즘 문제, 스켈레톤 코드, 그리고 제출된 솔루션을 분석하여 상세한 피드백을 제공해야 합니다. 피드백은 다음 6가지 카테고리로 구성되어야 합니다:

1. 코드 구현 정확도
2. 코드 스타일
3. 불필요 코드
4. 코드 효율성
5. 고려하지 못한 케이스
6. 종합 피드백

각 카테고리에 대해 구체적이고 건설적인 피드백을 제공하세요. 피드백 외의 다른 텍스트는 포함하지 마세요."""

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
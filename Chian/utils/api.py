import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests
from config import GEMINI_KEY, UPSTAGE_KEY

# OAuth 토큰 생성
def get_google_oauth_token():
    try:
        # JSON 파일의 상대 경로
        base_dir = os.path.dirname(os.path.dirname(__file__))  # chian 디렉토리 경로
        file_path = os.path.join(base_dir, "credentials", "gen-lang-client-0597667452-3507693b9eee.json")
        
        # 파일 경로 확인
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Service account file not found: {file_path}")

        # OAuth 인증 범위
        scopes = ["https://www.googleapis.com/auth/cloud-platform", "https://www.googleapis.com/auth/generative-language"]

        # OAuth 토큰 생성
        credentials = service_account.Credentials.from_service_account_file(
            file_path,
            scopes=scopes
        )
        auth_request = Request()
        credentials.refresh(auth_request)
        return credentials.token
    except Exception as e:
        print(f"Error while generating OAuth token: {e}")
        return None

# Gemini 키워드 추출
def extract_keyword_with_gemini(question):
    try:
        # gemini-1.5-pro 모델 URL
        url = "https://generativelanguage.googleapis.com/v1beta2/models/gemini-1.5-pro:generate"

        # OAuth 토큰 가져오기
        access_token = get_google_oauth_token()
        if not access_token:
            return "OAuth 인증 실패: 토큰을 가져올 수 없습니다."

        # 요청 헤더
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        # 요청 본문 수정
        payload = {
            "input": f"Extract a keyword from the question: '{question}'",
            "parameters": {
                "temperature": 0.7,
                "maxOutputTokens": 64,
                "topP": 0.8,
                "topK": 40
            }
        }

        # API 호출
        response = requests.post(url, headers=headers, json=payload)
        print(f"Gemini Response Status Code: {response.status_code}")
        print(f"Gemini Response Text: {response.text}")

        if response.status_code == 200:
            response_data = response.json()
            return response_data.get("candidates", [{}])[0].get("output", "키워드를 추출할 수 없습니다.")
        else:
            return f"키워드를 추출할 수 없습니다. Status Code: {response.status_code}"
    except Exception as e:
        print(f"Error in Gemini API call: {e}")
        return "키워드를 추출할 수 없습니다."
    
    
# Upstage 질문 분석
def analyze_question_with_upstage(question):
    try:
        url = "https://api.upstage.ai/v1/solar/analyze"
        headers = {
            "Authorization": f"Bearer {UPSTAGE_KEY}",
            "Content-Type": "application/json",
        }
        payload = {"text": question}
        response = requests.post(url, headers=headers, json=payload)
        print(f"Upstage Response Status Code: {response.status_code}")
        print(f"Upstage Response Text: {response.text}")

        if response.status_code == 200:
            return response.json()
        return {"error": "Upstage API 분석 실패"}
    except Exception as e:
        print(f"Error in Upstage API call: {e}")
        return {"error": "Upstage API 호출 중 오류 발생"}

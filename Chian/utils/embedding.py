from transformers import AutoTokenizer, AutoModel
from utils.retriever import data
from utils.api import extract_keyword_with_gemini
import pandas as pd
import numpy as np
import torch


from utils.retriever import retrieve_data

def process_question_with_gemini(question):
    keyword = extract_keyword_with_gemini(question)
    if keyword is None:
        return "키워드를 추출할 수 없습니다."
    return keyword


# 사전 학습된 모델 로드
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

def generate_embedding(text):
    if not isinstance(text, str):  # 문자열이 아닌 경우 처리
        return np.zeros(768)  # 기본값 (768차원 벡터)
    tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        embeddings = model(**tokens).last_hidden_state.mean(dim=1).squeeze().numpy()
    return embeddings


data['review'] = data['review'].fillna("").astype(str)  # NaN 값을 빈 문자열로 대체하고 문자열로 변환

# 'review' 열을 기반으로 'embedding' 열 추가
data['embedding'] = data['review'].apply(lambda x: generate_embedding(x) if pd.notna(x) else np.zeros(768))


def generate_embedding(text):
    if not isinstance(text, str):
        return np.zeros(768)
    tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        embeddings = model(**tokens).last_hidden_state.mean(dim=1).squeeze().numpy()
    return embeddings

# 'review' 컬럼 기반으로 'embedding' 생성
if 'review' in data.columns:
    data['embedding'] = data['review'].fillna("").apply(lambda x: generate_embedding(x))
else:
    print("Error: 'review' column not found in data.")


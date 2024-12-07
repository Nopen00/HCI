from flask import Flask, request, jsonify, render_template
from utils.retriever import retrieve_data
from utils.parser import parse_uploaded_file
from utils.embedding import process_question_with_gemini 
import numpy as np


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    question = request.json.get('question', '')
    print(f"Received question: {question}")

    # Gemini API 호출
    keyword = process_question_with_gemini(question)
    print(f"Extracted keyword: {keyword}")  # 추출된 키워드 로그 출력
    if not keyword:
        return jsonify({"error": "Gemini API에서 키워드를 추출할 수 없습니다."}), 400

    # 로컬 데이터 검색
    result = retrieve_data(keyword)
    return jsonify(result)





@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    parse_uploaded_file(file)  # 업로드된 파일 파싱 및 데이터 처리
    return jsonify({'message': 'File processed successfully'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

#http://172.30.1.98:5000
#http://172.24.48.1:5000

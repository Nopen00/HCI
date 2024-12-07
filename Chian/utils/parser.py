import pandas as pd

def parse_uploaded_file(file):
    # 엑셀 파일을 읽어 데이터베이스나 CSV 파일에 저장
    data = pd.read_excel(file)
    processed_data = data.fillna('정보 없음')
    processed_data.to_csv('data/processed_data.csv', index=False)
    return True

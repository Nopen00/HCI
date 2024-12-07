import pandas as pd
import os

# 파일 경로
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "../data/HCI_data.xlsx")

try:
    data = pd.read_excel(file_path)
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    data = pd.DataFrame(columns=['Title', 'review', 'perform', 'safety'])

# 키워드로 데이터 검색
def retrieve_data(keyword):
    if not isinstance(keyword, str):
        return {"error": "The keyword must be a string."}

    filtered_data = data[data['Title'].str.contains(keyword, na=False, case=False)]

    if filtered_data.empty:
        return {"message": f"No relevant data found for '{keyword}'"}

    return filtered_data[['Title', 'review', 'perform', 'safety']].to_dict(orient='records')

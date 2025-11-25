import requests
import xmltodict
import pandas as pd
import sqlite3
import time

# -----------------------------------------------------------
# 1. 설정 및 장르 코드 정의
# -----------------------------------------------------------
# 🚨 본인의 실제 서비스 키로 교체하세요
SERVICE_KEY = "######" 

# 수집 기간: 2024년 전체
START_DATE = "20240101"
END_DATE = "20241231"

# KOPIS 장르 코드 목록 (공통 코드표 참조)
GENRE_CODES = {
    "AAAA": "연극",
    "GGGA": "뮤지컬",
    "CCCA": "서양음악(클래식)",
    "CCCC": "한국음악(국악)",
    "CCCD": "대중음악",
    "BBBC": "무용(서양/한국무용)",
    "BBBR": "대중무용",
    "EEEB": "서커스/마술",
    "EEEA": "복합"
}

def fetch_all_performances_2024(service_key):
    """
    모든 장르의 2024년 공연 데이터를 수집하여 DataFrame으로 반환합니다.
    """
    base_url = "http://www.kopis.or.kr/openApi/restful/pblprfr"
    all_data = []

    print(f"🚀 2024년 전체 공연 데이터 수집을 시작합니다...")

    for code, name in GENRE_CODES.items():
        page = 1
        print(f"\n>> 장르 수집 시작: {name} ({code})")
        
        while True:
            params = {
                'service': service_key,
                'stdate': START_DATE,
                'eddate': END_DATE,
                'cpage': page,
                'rows': 100,     # 한 페이지당 최대 100건 (API 권장)
                'shcate': code,  # 장르 코드
            }

            try:
                response = requests.get(base_url, params=params)
                response.raise_for_status()
                
                # XML 파싱
                data_dict = xmltodict.parse(response.text)
                
                # 'dbs' > 'db' 구조 확인
                items = data_dict.get('dbs', {}).get('db')

                # 데이터가 없으면 해당 장르 수집 종료
                if not items:
                    print(f"   - 페이지 {page}: 데이터 없음. 다음 장르로 이동.")
                    break
                
                # 단일 항목일 경우 리스트로 변환
                if not isinstance(items, list):
                    items = [items]
                
                # 데이터 전처리 및 추가
                for item in items:
                    # 편의를 위해 장르명 컬럼을 명시적으로 추가
                    item['genre_name'] = name 
                    all_data.append(item)
                
                print(f"   - 페이지 {page}: {len(items)}건 수집 완료 (누적 {len(all_data)}건)")
                
                page += 1
                time.sleep(0.2) # API 서버 부하 방지

            except Exception as e:
                print(f"❌ 에러 발생 (페이지 {page}): {e}")
                break
    
    print(f"\n🎉 수집 완료! 총 {len(all_data)}개의 공연 정보를 가져왔습니다.")
    return pd.DataFrame(all_data)

def save_to_sqlite(df, db_name="kopis_2024.db", table_name="performances"):
    """
    DataFrame을 SQLite 데이터베이스 파일로 저장합니다.
    """
    try:
        # DB 연결 (파일이 없으면 자동 생성됨)
        conn = sqlite3.connect(db_name)
        
        # DataFrame을 SQL 테이블로 저장 (이미 존재하면 덮어쓰기)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        conn.close()
        print(f"💾 DB 저장 완료: '{db_name}' 파일 내 '{table_name}' 테이블")
    except Exception as e:
        print(f"❌ DB 저장 실패: {e}")




def save_to_sqlite(df, db_name="kopis_2024.db", table_name="performances"):
    """
    DataFrame을 SQLite 데이터베이스 파일로 저장합니다.
    """
    try:
        # DB 연결 (파일이 없으면 자동 생성됨)
        conn = sqlite3.connect(db_name)
        
        # DataFrame을 SQL 테이블로 저장 (이미 존재하면 덮어쓰기)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        conn.close()
        print(f"💾 DB 저장 완료: '{db_name}' 파일 내 '{table_name}' 테이블")
    except Exception as e:
        print(f"❌ DB 저장 실패: {e}")


          
if __name__ == "__main__":
    # 1. 데이터 수집
    df_result = fetch_all_performances_2024(SERVICE_KEY)
    
    # 2. 결과 확인 및 DB 저장
    if not df_result.empty:
        print(df_result.head()) # 상위 5개 데이터 미리보기
        print(df_result.info()) # 데이터 구조 확인
        
        # DB로 내보내기
        save_to_sqlite(df_result)
    else:
        print("수집된 데이터가 없습니다. 서비스 키나 기간을 확인해주세요.")
  

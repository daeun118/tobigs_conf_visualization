from matplotlib import rc
from utils.db_manager import DBManager
from utils.filter import FilterManager

# matplotlib 한글깨짐 방지
rc('font', family='Malgun Gothic')  # Windows: 'Malgun Gothic' (Mac의 경우 'AppleGothic')
rc('axes', unicode_minus=False)  # 마이너스 기호 깨짐 방지

if __name__ == '__main__':
    # 데이터베이스 연결 정보
    db_config = {
        'host': 'localhost',
        'database': 'example_db',
        'user': 'postgres',
        'password': '0118',
        'port': 5432
        }

    # DBManager 초기화
    db_manager = DBManager(db_config)
    # FilterManager 초기화
    filter_manager = FilterManager()

    # 조건 정의
    conditions = {
    "depart_country": "대한민국",
    "arrival_country": "대한민국",
    "depart_airport": ["김포국제공항", "인천국제공항"],
    "arrival_airport": "제주국제공항",
    "airline": ["제주항공", "대한항공"],
    "depart_time(dep)": {
        "date": "1월 둘째주",
        "day": ["토요일", "일요일"],
        "time": "오후"
    },
    "arrival_time(arr)": {
        "time": {
            "start": "18:00",
            "end": "22:00"
        }
    },
    "fare": "50000",
    "visualization": {
        "type": "calendar_heatmap",
    }
}

    # SQL 쿼리 생성
    query = filter_manager.generate_query_from_conditions(conditions)
    print(f"Generated Query: {query}")

    # SQL 쿼리를 실행하여 데이터프레임 가져오기
    grouped_data = db_manager.execute_query(query)

    # 쿼리에서 시각화 타입 추출
    visualization_type = conditions.get("visualization", {}).get("type")

    # 적절한 시각화 함수 호출
    if visualization_type in VISUALIZATION_FUNCTIONS:
        visualization_function = VISUALIZATION_FUNCTIONS[visualization_type]
        # 시각화 함수 호출 (grouped_data 전달)
        visualization_function(grouped_data) 
    else:
        print(f"Unsupported visualization type: {visualization_type}")
from matplotlib import rc
from utils.db_manager import DBManager
from utils.filter import FilterManager
from visualizations.visualization_mapper import VISUALIZATION_FUNCTIONS
import time # 실행시간 측정

# matplotlib 한글깨짐 방지
rc('font', family='Malgun Gothic')  
rc('axes', unicode_minus=False)  # 마이너스 기호 깨짐 방지

if __name__ == '__main__':
    # 시작 시간 기록
    overall_start_time = time.time()

    # 데이터베이스 연결 정보
    db_config = {
        'host': 'localhost',
        'database': 'flight',
        'user': 'postgres',
        'password': '0118',
        'port': 5432
        }

    # DBManager 초기화
    db_manager = DBManager(db_config)
    # FilterManager 초기화
    filter_manager = FilterManager()

    # SQL 쿼리 생성 시작 시간
    query_start_time = time.time()

    # 조건 정의
    conditions = {
        "depart_country": "대한민국",
        "arrival_country": "대한민국",
        "depart_airport": ["김포국제공항", "인천국제공항"],
        "arrival_airport": "제주국제공항",
        "seat_class": "비즈니스석",
        "depart_time(dep)": {
            "date": "1월 둘째주",
        },
        "arrival_time(arr)": {
            "time": {
                "start": "18:00",
                "end": "22:00"
            }
        },
        "fare": "1000000",
        "visualization": {
            "type": "line_graph",
        }
    }

    # SQL 쿼리 생성
    query = filter_manager.generate_query_from_conditions(conditions)
    query_elapsed_time = time.time() - query_start_time
    print(f"SQL 쿼리 생성 시간: {query_elapsed_time:.2f}초")
    print(f"Generated Query: {query}")

    # SQL 실행 시작 시간
    query_execution_start_time = time.time()

    # SQL 쿼리를 실행하여 데이터프레임 가져오기
    grouped_data = db_manager.execute_query(query)
    query_execution_elapsed_time = time.time() - query_execution_start_time
    print(f"SQL 실행 및 데이터 가져오기 시간: {query_execution_elapsed_time:.2f}초")

    # 쿼리에서 시각화 타입 추출
    visualization_type = conditions.get("visualization", {}).get("type")

    # 적절한 시각화 함수 호출
    if visualization_type in VISUALIZATION_FUNCTIONS:
        visualization_function = VISUALIZATION_FUNCTIONS[visualization_type]
        visualization_start_time = time.time()

        # 시각화 함수 호출 (grouped_data 전달)
        visualization_function(grouped_data)
        visualization_elapsed_time = time.time() - visualization_start_time
        overall_elapsed_time = time.time() - overall_start_time
        print(f"{visualization_type} 시각화 출력 시간: {visualization_elapsed_time:.2f}초")
        print(f"전체 실행 시간: {overall_elapsed_time:.2f}초")
    else:
        print(f"Unsupported visualization type: {visualization_type}")
from datetime import datetime

def generate_query_from_conditions(conditions):
    """
    조건에 맞는 SQL 쿼리를 동적으로 생성.
    :param conditions: dict - 필터링 조건
    :return: str - SQL 쿼리
    """
    base_query = "SELECT * FROM flight_data WHERE 1=1"

    # air_id 필터링
    if "air_id" in conditions:
        base_query += f" AND air_id = '{conditions['air_id']}'"

    # is_layover 필터링
    if "is_layover" in conditions:
        base_query += f" AND is_layover = {conditions['is_layover']}"

    # 출발 공항 코드 필터링
    if "airport_code_dep" in conditions:
        base_query += f" AND airport_code_dep = '{conditions['airport_code_dep']}'"

    # 출발 공항 이름 필터링
    if "departure_airport" in conditions:
        base_query += f" AND departure_airport = '{conditions['departure_airport']}'"

    # 출발 국가 필터링
    if "departure_country" in conditions:
        base_query += f" AND departure_country = '{conditions['departure_country']}'"

    # 도착 공항 코드 필터링
    if "airport_code_arr" in conditions:
        base_query += f" AND airport_code_arr = '{conditions['airport_code_arr']}'"

    # 도착 공항 이름 필터링
    if "arrival_airport" in conditions:
        base_query += f" AND arrival_airport = '{conditions['arrival_airport']}'"

    # 도착 국가 필터링
    if "arrival_country" in conditions:
        base_query += f" AND arrival_country = '{conditions['arrival_country']}'"

    # 항공사 필터링
    if "airline" in conditions:
        base_query += f" AND airline = '{conditions['airline']}'"

    # 출발 UTC 시간 필터링
    if "depart_timestamp_utc" in conditions:
        base_query += f" AND depart_timestamp_utc = '{conditions['depart_timestamp_utc']}'"

    # 도착 UTC 시간 필터링
    if "arrival_timestamp_utc" in conditions:
        base_query += f" AND arrival_timestamp_utc = '{conditions['arrival_timestamp_utc']}'"

    # 출발 시간 (현지) 필터링
    if "departure_time_in_dep" in conditions:
        departure_time = conditions["departure_time_in_dep"]
    
    try:
        # 시간이 포함된 경우 (TIMESTAMP)
        datetime.strptime(departure_time, "%Y-%m-%d %H:%M:%S")
        base_query += f" AND departure_time_in_dep = '{departure_time}'"
    except ValueError:
        # 날짜만 포함된 경우 (DATE)
        base_query += f" AND DATE(departure_time_in_dep) = '{departure_time}'"


    # 도착 시간 (현지) 필터링
    if "arrival_time_in_dep" in conditions:
        base_query += f" AND arrival_time_in_dep = '{conditions['arrival_time_in_dep']}'"

    # 출발 시간 (도착지 시간대) 필터링
    if "departure_time_in_arr" in conditions:
        base_query += f" AND departure_time_in_arr = '{conditions['departure_time_in_arr']}'"

    # 도착 시간 (도착지 시간대) 필터링
    if "arrival_time_in_arr" in conditions:
        base_query += f" AND arrival_time_in_arr = '{conditions['arrival_time_in_arr']}'"

    # 좌석 등급 필터링
    if "seat_class" in conditions:
        base_query += f" AND seat_class = '{conditions['seat_class']}'"

    # AGT 코드 필터링
    if "agt_code" in conditions:
        base_query += f" AND agt_code = '{conditions['agt_code']}'"

    # 운임 필터링
    if "fare" in conditions:
        base_query += f" AND fare = {conditions['fare']}"

    # 여정 시간 필터링
    if "journey_time" in conditions:
        base_query += f" AND journey_time = {conditions['journey_time']}"

    # 데이터 수집 날짜 필터링
    if "fetched_date" in conditions:
        base_query += f" AND fetched_date = '{conditions['fetched_date']}'"

    return base_query

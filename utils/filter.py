
from utils.date_utils import DateUtils
from utils.day_utils import DayUtils
from utils.time_utils import TimeUtils

class FilterManager:
    def __init__(self):
        self.date_utils = DateUtils()
        self.day_utils = DayUtils()
        self.time_utils = TimeUtils()

    # 출발 시간과 도착 시간 필터링하는 공통 함수
    def handle_time_filters(self, time_conditions, prefix, base_query):

        # 날짜 필터링
        if "date" in time_conditions:
            base_query += self.date_utils.build_date_conditions(time_conditions["date"], prefix)

        # 요일 필터링
        if "day" in time_conditions:
            base_query += self.day_utils.build_weekday_condition(time_conditions["day"], prefix)

        # 시간 필터링
        if "time" in time_conditions:
            base_query += self.time_utils.build_time_conditions(time_conditions["time"], prefix)

        return base_query

    # 조건이 두 개 이상일 경우 더하는 함수  
    def _add_condition(self, base_query, column, value, is_list=False):
        if value != "all":
            if is_list:
                values = "', '".join(value)
                base_query += f" AND {column} IN ('{values}')\n"
            else:
                base_query += f" AND {column} = '{value}'\n"
        return base_query

    # 조건에 맞는 SQL 쿼리문 작성 함수
    def generate_query_from_conditions(self, conditions):
        base_query = "SELECT * FROM flight_data WHERE 1=1\n"

        # LCC, FSC, 국내 항공사 분류
        lcc_airlines = ["제주항공", "진에어", "티웨이항공", "에어부산", "에어서울", "이스타항공", "피치항공"]
        fsc_airlines = ["대한항공", "아시아나항공", "전일본공수", "일본 항공"]
        domestic_airlines = ["대한항공", "아시아나항공", "에어부산", "에어서울", "이스타항공", "제주항공", "진에어", "티웨이항공"]

        # 항공사 필터링 (airline)
        if "airline" in conditions and conditions["airline"] != "all":
            airline = conditions["airline"]
            if airline == "lcc":
                base_query = self._add_condition(base_query, "airline", lcc_airlines, is_list=True)
            elif airline == "fsc":
                base_query = self._add_condition(base_query, "airline", fsc_airlines, is_list=True)
            elif airline == "국내 항공사":
                base_query = self._add_condition(base_query, "airline", domestic_airlines, is_list=True)
            elif isinstance(airline, list):  # 사용자가 직접 리스트를 넘긴 경우
                base_query = self._add_condition(base_query, "airline", airline, is_list=True)
            else:  # 단일 항공사 문자열인 경우
                base_query = self._add_condition(base_query, "airline", airline)

        # 출발 국가 필터링 (depart_country)
        if "depart_country" in conditions:
            base_query = self._add_condition(base_query, "depart_country",conditions["depart_country"], is_list=isinstance(conditions["depart_country"], list))
        
        # 도착 국가 필터링 (arrival_country)
        if "arrival_country" in conditions:
            base_query = self._add_condition(base_query, "arrival_country", conditions["arrival_country"], is_list=isinstance(conditions["arrival_country"], list))
        
        # 출발 공항 필터링 (depart_ariport)
        if "depart_airport" in conditions:
            base_query = self._add_condition(base_query, "depart_airport", conditions["depart_airport"], is_list=isinstance(conditions["depart_airport"], list))
        
        # 도착 공항 필터링 (arrival_airport)
        if "arrival_airport" in conditions:
            base_query = self._add_condition(base_query, "arrival_airport", conditions["arrival_airport"], is_list=isinstance(conditions["arrival_airport"], list))

        # 출발 시간 필터링 (depart_time(dep))
        if "depart_time(dep)" in conditions:
            depart_conditions = conditions["depart_time(dep)"]
            base_query = self.handle_time_filters(depart_conditions, "depart_time_dep", base_query)

        # 도착 시간 필터링 (arrival_time(arr))
        if "arrival_time(arr)" in conditions:
            arrival_conditions = conditions["arrival_time(arr)"]
            base_query = self.handle_time_filters(arrival_conditions, "arrival_time_arr", base_query)

        # 요금 조건 필터링 (fare)
        if "fare" in conditions:
            base_query += " AND fare <= {}\n".format(float(conditions["fare"]))
            
        return base_query
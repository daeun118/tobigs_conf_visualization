class TimeUtils:
    # 시간 조건을 처리하여 SQL 구문을 생성하는 함수
    def build_time_condition(self, time, prefix):
        time_ranges = {
            "아침": (6, 9),
            "낮": (10, 17),
            "저녁": (18, 20),
            "밤": (21, 5),
            "오전": (0, 11),
            "오후": (12, 23),
        }
        if time in time_ranges:
            start_hour, end_hour = time_ranges[time]
            if start_hour <= end_hour:
                return f" AND EXTRACT(HOUR FROM {prefix}::time) BETWEEN {start_hour} AND {end_hour}\n"
            else:
                return f" AND EXTRACT(HOUR FROM {prefix}::time) >= {start_hour} OR EXTRACT(HOUR FROM {prefix}::time) <= {end_hour}\n"
        return ""

    # 시간 범위 처리 함수
    def build_time_range_condition(self, time_range, prefix):
        if "start" in time_range and "end" in time_range:
            start_time = time_range["start"]
            end_time = time_range["end"]
            return f" AND EXTRACT(HOUR FROM {prefix}::time) BETWEEN {start_time.split(':')[0]} AND {end_time.split(':')[0]}\n"
        return ""
    
    # 시간 조건 종류에 따라 SQL 구문을 생성하는 함수
    def build_time_conditions(self, time_condition, prefix):
        # 시간 조건이 여러 개일 경우 각각 처리하고, OR 조건을 이용하여 결합
        if isinstance(time_condition, list):  
            time_conditions = [self.build_time_condition(time, prefix) for time in time_condition]
            if time_conditions:
                return " AND (" + " OR ".join(time_conditions) + ")\n"
        # 사용자가 시간 범위를 입력했을 경우
        elif isinstance(time_condition, dict):  
            return self.build_time_range_condition(time_condition, prefix)
        # 시간 조건이 하나일 경우
        elif isinstance(time_condition, str):  
            return self.build_time_condition(time_condition, prefix)

        return ""




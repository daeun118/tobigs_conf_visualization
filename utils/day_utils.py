class DayUtils:
    # 요일 조건에 맞는 SQL 구문을 생성하는 함수
    def build_weekday_condition(self, weekdays, prefix):
        weekdays_map = {"일요일": 0, "월요일": 1, "화요일": 2, "수요일": 3, 
                        "목요일": 4, "금요일": 5, "토요일": 6}
        selected_days = [str(weekdays_map[day]) for day in weekdays if day in weekdays_map]
        if selected_days:
            return f" AND EXTRACT(DOW FROM {prefix}) IN ({', '.join(selected_days)})\n"
        return ""
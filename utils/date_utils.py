import re
import datetime

class DateUtils:
    # 월 이름을 숫자로 변환하는 함수
    def convert_month_to_number(self, month_name):
        month_numbers = {f"{i}월": i for i in range(1, 13)} 
        return month_numbers.get(month_name, None)

    # 주 이름을 숫자로 변환하는 함수
    def convert_week_to_number(self, week):
        week_numbers = {"첫째주": 1, "둘째주": 2, "셋째주": 3, "넷째주": 4}
        return week_numbers.get(week, None)

    # 해당 월의 첫 번째 월요일을 구하는 함수
    def get_first_weekday_of_month(self, year, month, weekday):
        # 해당 월의 첫 번째 날을 구한 후, 주어진 요일에 맞춰 첫 번째 월요일을 계산
        first_day_of_month = datetime.date(year, month, 1)
        days_to_add = (weekday - first_day_of_month.weekday()) % 7
        return first_day_of_month + datetime.timedelta(days=days_to_add)

    # 주의 시작일과 끝일을 계산하는 함수
    def get_week_date_range(self, year, month, week_number):
        # 해당 월의 첫 번째 월요일을 구하고, 주 번호에 맞는 날짜 범위 계산
        first_weekday_of_month = self.get_first_weekday_of_month(year, month, 0)  # 월요일: 0
        start_date = first_weekday_of_month + datetime.timedelta(weeks=week_number - 1)
        end_date = start_date + datetime.timedelta(days=6)
        return start_date, end_date
    
    # 월 조건을 처리하여 SQL 구문을 생성하는 함수
    def build_month_condition(self, month_condition, prefix):
        month_numbers = {f"{i}월": i for i in range(1, 13)}  # 1월 ~ 12월 매핑
        selected_months = [str(month_numbers[month]) for month in month_condition if month in month_numbers]
        if selected_months:
            return f" AND EXTRACT(MONTH FROM {prefix}) IN ({', '.join(selected_months)})\n"
        return ""
    
    # 주, 월, 날짜 조건에 맞는 SQL 구문을 생성하는 함수    
    def build_date_condition(self, date, prefix):
        if "주" in date:
            month_name, week = date.split(" ")[0], date.split(" ")[1]
            month = self.convert_month_to_number(month_name)
            week_number = self.convert_week_to_number(week)
            if month and week_number:
                start_date, end_date = self.get_week_date_range(2025, month, week_number)
                return f"{prefix} BETWEEN '{start_date}' AND '{end_date}'"
        # 월 형식: 예) '1월', '3월'
        elif "월" in date:
            return self.build_month_condition([date], prefix)
        # 날짜 형식: 예) '2024-03-15'
        elif re.match(r'\d{4}-\d{2}-\d{2}', date):  
            return f"DATE({prefix} = '{date}'"
        return ""

    # 날짜 조건의 리스트 유무에 따라 SQL 구문을 생성하는 함수
    def build_date_conditions(self, date_condition, prefix):
        if isinstance(date_condition, list):
            date_conditions = [self.build_date_condition(date, prefix) for date in date_condition]
        else:
            date_conditions = [self.build_date_condition(date_condition, prefix)]

        if date_conditions:
            return " AND (" + " OR ".join(date_conditions) + ")\n"
        return ""
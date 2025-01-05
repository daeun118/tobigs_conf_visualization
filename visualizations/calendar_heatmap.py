import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import os
from datetime import datetime

def calendar_heatmap(data):
    """
    달력형 히트맵을 생성하여 출발 날짜(depart_time_dep)별 중앙값 요금을 시각화
    """
    # 1. 날짜 정보 변환
    data['depart_time_dep'] = pd.to_datetime(data['depart_time_dep'])
    data['year'] = data['depart_time_dep'].dt.year
    data['month'] = data['depart_time_dep'].dt.month
    data['day'] = data['depart_time_dep'].dt.day
    data['weekday'] = data['depart_time_dep'].dt.weekday  # 요일 정보 추가 (월=0, 일=6)

    # 2. 대상 연도 및 월 추출
    year = data['year'].iloc[0]
    months = data['month'].unique()

    for month in sorted(months):
        # 해당 월 데이터만 필터링
        month_data = data[data['month'] == month]

        # 3. 월별 달력 데이터 생성
        month_calendar = calendar.monthcalendar(year, month)

        # 4. 요금 데이터를 달력에 매핑 (중앙값 기준)
        fare_values = np.full_like(month_calendar, np.nan, dtype=float)  # 중앙값 요금을 저장할 배열
        fare_annotations = np.full_like(month_calendar, '', dtype=object)  # 날짜와 요금, 요일 표시용

        for week_idx, week in enumerate(month_calendar):
            for day_idx, day in enumerate(week):
                if day > 0:  # 유효한 날짜만 처리
                    # 해당 날짜 데이터 필터링
                    day_data = month_data[month_data['day'] == day]
                    if not day_data.empty:  # 필터링된 데이터가 비어 있는지 확인
                        fare = day_data['fare'].median()  # 중앙값 요금 계산
                        weekday_idx = day_data['weekday'].iloc[0]  # 요일 인덱스
                        weekday = calendar.day_abbr[weekday_idx]  # 요일 인덱스를 요일 약자로 변환
                        fare_values[week_idx][day_idx] = fare  # 중앙값 요금 저장
                        fare_annotations[week_idx][day_idx] = f"{day}\n{weekday}\n{int(fare):,}"

        # 5. 히트맵 생성 (중앙값 요금 기준)
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(
            fare_values, 
            annot=fare_annotations, 
            fmt='', 
            cmap='YlGnBu', 
            linewidths=0.7, 
            linecolor='white', 
            cbar=True, 
            ax=ax, 
            annot_kws={"size": 15, "color": "black"}
        )

        # 6. 축 및 레이블 설정
        ax.set_xticks(np.arange(7) + 0.5)
        ax.set_xticklabels(['월', '화', '수', '목', '금', '토', '일'], fontsize=12, fontweight='bold')
        ax.set_yticks(np.arange(len(month_calendar)) + 0.5)
        ax.set_yticklabels(range(1, len(month_calendar) + 1), fontsize=12, fontweight='bold')

        ax.set_title(f'{year}년 {month}월 항공권 중앙값 요금', fontsize=16, fontweight='bold')
        ax.axis('off')

        plt.tight_layout()

        # 이미지 저장 (고정 경로로 저장)
        save_path = "D:/Tobigs/output"
        os.makedirs(save_path, exist_ok=True)  # 폴더가 없으면 생성
        today = datetime.today()
        file_name = f"{today.strftime('%Y-%m-%d_%H-%M-%S')}_calender_heatmap.png"
        plt.savefig(f"{save_path}/{file_name}", dpi=300, bbox_inches='tight')
        print(f"이미지가 '{save_path}/{file_name}'에 저장되었습니다.")

        plt.show()

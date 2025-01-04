import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from matplotlib.ticker import StrMethodFormatter
import os

'''
들어가는 data는 air_ID와 fetched_date로 groupby 후 
각 그룹에서 fare가 가장 낮은 행만 남긴 것
'''
# 가격변동 시각화 그래프(꺾은선그래프)

def line_graph(data):
    X = 'fetched_date'
    y = 'fare'

    # 현재 날짜와 한 달 전 날짜 계산
    today = datetime.today()
    one_month_ago = today - timedelta(days=74) # 현재 10월 데이터밖에 없어서 시험용! days 30으로 바꿔줘야 함

    # fetched_date 열을 datetime 형식으로 변환
    data[X] = pd.to_datetime(data[X])

    # 최근 한 달치 데이터 필터링
    filtered_data = data[(data[X] >= one_month_ago) & (data[X] <= today)]

    # X축 값별로 Y값의 평균 및 중앙값 계산
    data_grouped = filtered_data.groupby(X, as_index=False).agg(
        avg_fare=(y, 'mean'),
        median_fare=(y, 'median')
    )

    # 꺾은선 그래프 생성
    plt.figure(figsize=(10, 6))
    plt.plot(data_grouped[X], data_grouped['avg_fare'], color='blue', marker='o', linestyle='-', label='Average Fare')
    plt.plot(data_grouped[X], data_grouped['median_fare'], color='red', marker='s', linestyle='-', label='Median Fare')

    # 그래프 설정
    plt.title("Line Graph(최근 30일)")
    plt.xlabel("Fetched Date")
    plt.ylabel("Fare")
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # y축 3자리마다 ',' 추가
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()

    # 이미지 저장 (고정 경로로 저장)
    save_path = "D:/Tobigs/output"
    os.makedirs(save_path, exist_ok=True)  # 폴더가 없으면 생성
    file_name = f"{today.strftime('%Y-%m-%d_%H-%M-%S')}_line_graph.png"
    plt.savefig(f"{save_path}/{file_name}", dpi=300, bbox_inches='tight')
    print(f"이미지가 '{save_path}/{file_name}'에 저장되었습니다.")

    plt.show()

    
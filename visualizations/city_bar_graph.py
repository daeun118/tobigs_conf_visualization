import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

def city_airport_mapping(data):
    # 1. 도시별 공항 매핑 정의
    city_airports = {
        "김포": ["GMP"],
        "인천": ["ICN"],
        "제주": ["CJU"],
        "도쿄": ["NRT", "HND"],
        "오사카": ["KIX", "ITM"],
        "고베": ["UKB"],
        "나고야": ["NKB", "NGO"],
        "오키나와": ["OKA"],
        "삿포로": ["CTS"],
        "후쿠오카": ["FUK"]
    }

    # 2. 도착 공항에 따라 도시 이름으로 매핑 
    def map_city(airport):
        for city, airports in city_airports.items():
            if airport in airports:
                return city
        return None  # 매핑되지 않는 공항은 None 처리

    data['city'] = data['airport_code_arr'].apply(map_city)
    
    return data

def city_bar_graph(data):
    # 1. 도시별 평균 및 중앙값 계산
    data = city_airport_mapping(data)
    grouped_data = data.groupby('city', as_index=False).agg(
        avg_fare=('fare', 'mean'),
        median_fare=('fare', 'median')
    )

    # 2. 각각의 데이터 정렬
    avg_sorted = grouped_data.sort_values(by='avg_fare', ascending=True).reset_index(drop=True)
    median_sorted = grouped_data.sort_values(by='median_fare', ascending=True).reset_index(drop=True)

    # 3. 캔버스 생성 및 서브플롯 설정
    fig, axes = plt.subplots(2, 1, figsize=(16, 16), sharex=False)
    fig.suptitle("도시별 평균 및 중앙값 요금", fontsize=16, fontweight='bold')

    # 4. 평균 요금 그래프 생성 (첫 번째 서브플롯)
    sns.barplot(
        x='city', y='avg_fare', data=avg_sorted,
        palette="Blues_d", edgecolor='black', ax=axes[0], width=0.6
    )
    axes[0].set_title("도시별 평균 요금", fontsize=14)
    axes[0].set_ylabel("평균 요금 (₩)", fontsize=12)
    axes[0].set_ylim(0, avg_sorted['avg_fare'].max() * 1.2) # y축 범위 조정, 최대값의 120%로 설정
    axes[0].grid(axis='y', linestyle='--', alpha=0.6)

    # 평균 요금 값 표시
    for index, row in avg_sorted.iterrows():
        axes[0].text(index, row['avg_fare'] + 500, f"{int(row['avg_fare']):,}", ha='center', fontsize=10, fontweight='bold')

    # 5. 중앙값 요금 그래프 생성 (두 번째 서브플롯)
    sns.barplot(
        x='city', y='median_fare', data=median_sorted,
        palette="Oranges_d", edgecolor='black', ax=axes[1], width=0.6
    )
    axes[1].set_title("도시별 중앙값 요금", fontsize=14)
    axes[1].set_ylabel("중앙값 요금 (₩)", fontsize=12)
    axes[1].set_ylim(0, median_sorted['median_fare'].max() * 1.2) # y축 범위 조정, 최대값의 120%로 설정
    axes[1].grid(axis='y', linestyle='--', alpha=0.6)

    # 중앙값 요금 값 표시
    for index, row in median_sorted.iterrows():
        axes[1].text(index, row['median_fare'] + 500, f"{int(row['median_fare']):,}", ha='center', fontsize=10, fontweight='bold')

    # 6. X축 설정 (각각 독립)
    axes[0].set_xticks(range(len(avg_sorted['city'])))  # 고정된 눈금 설정
    axes[0].set_xticklabels(avg_sorted['city'], rotation=45, fontsize=10)
    axes[1].set_xticks(range(len(median_sorted['city'])))  # 고정된 눈금 설정
    axes[1].set_xticklabels(median_sorted['city'], rotation=45, fontsize=10)

    # 7. 그래프 레이아웃 조정 및 표시
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # 제목과 그래프 간격 조정

    # 이미지 저장 (고정 경로로 저장)
    save_path = "D:/Tobigs/output"
    os.makedirs(save_path, exist_ok=True)  # 폴더가 없으면 생성
    today = datetime.today()
    file_name = f"{today.strftime('%Y-%m-%d_%H-%M-%S')}_city_bar_graph.png"
    plt.savefig(f"{save_path}/{file_name}", dpi=300, bbox_inches='tight')
    print(f"이미지가 '{save_path}/{file_name}'에 저장되었습니다.")
    
    plt.show()
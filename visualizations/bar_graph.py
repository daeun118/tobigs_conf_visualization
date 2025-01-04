import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def bar_graph(data):
    # 1. 평균 및 중앙값 계산
    grouped_data = data.groupby('airline', as_index=False).agg(
        avg_fare=('fare', 'mean'),
        median_fare=('fare', 'median')
    )

    # 2. 각각의 데이터 정렬
    avg_sorted = grouped_data.sort_values(by='avg_fare', ascending=True).reset_index(drop=True)
    median_sorted = grouped_data.sort_values(by='median_fare', ascending=True).reset_index(drop=True)

    # 3. 캔버스 생성 및 서브플롯 설정
    fig, axes = plt.subplots(2, 1, figsize=(16, 20), sharex=False)
    fig.suptitle("항공사별 평균 및 중앙값 요금", fontsize=16, fontweight='bold')

    # 4. 평균 요금 그래프 생성 (첫 번째 서브플롯)
    sns.barplot(
        x='airline', y='avg_fare', data=avg_sorted,
        palette="Blues_d", edgecolor='black', ax=axes[0]
    )
    axes[0].set_title("항공사별 평균 요금", fontsize=14)
    axes[0].set_ylabel("평균 요금 (₩)", fontsize=12)
    axes[0].grid(axis='y', linestyle='--', alpha=0.6)

    # 평균 요금 값 표시
    for index, row in avg_sorted.iterrows():
        axes[0].text(index, row['avg_fare'] + 2000, f"{int(row['avg_fare']):,}", ha='center', fontsize=10)

    # 5. 중앙값 요금 그래프 생성 (두 번째 서브플롯)
    sns.barplot(
        x='airline', y='median_fare', data=median_sorted,
        palette="Oranges_d", edgecolor='black', ax=axes[1]
    )
    axes[1].set_title("항공사별 중앙값 요금", fontsize=14)
    axes[1].set_ylabel("중앙값 요금 (₩)", fontsize=12)
    axes[1].grid(axis='y', linestyle='--', alpha=0.6)

    # 중앙값 요금 값 표시
    for index, row in median_sorted.iterrows():
        axes[1].text(index, row['median_fare'] + 2000, f"{int(row['median_fare']):,}", ha='center', fontsize=10)

    # 6. X축 설정 (각각 독립)
    axes[0].set_xticklabels(avg_sorted['airline'], rotation=45, fontsize=10)
    axes[1].set_xticklabels(median_sorted['airline'], rotation=45, fontsize=10)

    # 7. 그래프 레이아웃 조정 및 표시
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # 제목과 그래프 간격 조정
    plt.show()

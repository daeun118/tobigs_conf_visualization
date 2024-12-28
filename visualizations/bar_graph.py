import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def bar_graph(data):
    # 1. 평균 요금 계산 및 정렬
    grouped_data = data.groupby('airline', as_index=False)['fare'].mean()
    grouped_data = grouped_data.sort_values(by='fare', ascending=True).reset_index(drop=True)

    # 2. 막대 색상 설정
    norm = plt.Normalize(grouped_data['fare'].min(), grouped_data['fare'].max())
    sm = plt.cm.ScalarMappable(cmap="Reds", norm=norm)
    colors = [sm.to_rgba(val) for val in grouped_data['fare']]

    # 3. 막대 그래프 생성
    plt.figure(figsize=(12, 6))
    sns.barplot(
        x='airline', y='fare', data=grouped_data,
        palette=colors, edgecolor='black'
    )

    # 4. 그래프 꾸미기
    plt.title("항공사별 평균 요금", fontsize=16, fontweight='bold')
    plt.xlabel("항공사", fontsize=14)
    plt.ylabel("평균 요금 (₩)", fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    # 5. 평균 요금 값 표시
    for index, row in grouped_data.iterrows():
        plt.text(index, row['fare'] + 2000, f"{int(row['fare']):,}", ha='center', fontsize=10)

    # 6. 컬러바 추가
    cbar = plt.colorbar(sm, ax=plt.gca(), orientation='vertical')
    cbar.set_label('평균 요금 (₩)', fontsize=12)
    cbar.ax.tick_params(labelsize=10)

    # 7. 그래프 표시
    plt.tight_layout()
    plt.show()

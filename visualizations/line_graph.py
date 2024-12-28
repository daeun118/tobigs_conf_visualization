import matplotlib.pyplot as plt

'''
들어가는 data는 air_ID와 fetched_date로 groupby 후 
각 그룹에서 fare가 가장 낮은 행만 남긴 것
'''
# 가격변동 시각화 그래프(꺾은선그래프)

def line_graph(data):
    X = 'fetched_date'
    y = 'fare'

    # X축 값별로 Y값을 평균으로 집계
    data_grouped = data.groupby(X, as_index=False)[y].mean()

    # 꺾은선 그래프 생성
    plt.figure(figsize=(10, 6))
    plt.plot(data_grouped[X], data_grouped[y], marker='o', linestyle='-', label=y)

    # 그래프 설정
    plt.title("Line Graph")
    plt.xlabel("Fetched Date")
    plt.ylabel("Fare")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()

    # 그래프 표시
    plt.show()
from visualizations.line_graph import line_graph
from visualizations.airline_bar_graph import airline_bar_graph
from visualizations.calendar_heatmap import calendar_heatmap
from visualizations.calendar_heatmap_medi import calendar_heatmap_medi
from visualizations.city_bar_graph import city_bar_graph

# 시각화 타입과 해당 함수 매핑
VISUALIZATION_FUNCTIONS = {
    "line_graph": line_graph,
    "airline_bar_graph": airline_bar_graph,
    "calendar_heatmap": calendar_heatmap,
    "calendar_heatmap_medi": calendar_heatmap_medi,
    "city_bar_graph": city_bar_graph
}

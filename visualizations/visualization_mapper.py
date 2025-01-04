from visualizations.line_graph import line_graph
from visualizations.bar_graph import bar_graph
from visualizations.calendar_heatmap import calendar_heatmap
from visualizations.calendar_heatmap_medi import calendar_heatmap_medi

# 시각화 타입과 해당 함수 매핑
VISUALIZATION_FUNCTIONS = {
    "line_graph": line_graph,
    "calendar_heatmap": calendar_heatmap,
    "bar_graph": bar_graph,
    "calendar_heatmap_medi": calendar_heatmap_medi
}

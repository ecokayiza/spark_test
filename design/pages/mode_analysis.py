import streamlit as st
import folium
import pandas as pd


st.markdown("<h1 style='text-align: center;'>🤓👆模式分析</h1>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df_track=pd.read_csv(r"design/result/track/part-00000-a99a94b6-e428-49f1-b3b0-411b1034eaac-c000.csv")
    return df_track
df_track = load_data()
@st.cache_data
def load_distance_data():
    df_track=pd.read_csv(r"design/result/avg_distance/part-00000-688ae885-e7d1-43d7-b5c1-8574a0eae789-c000.csv")
    return df_track
df_distance = load_distance_data()
@st.cache_data
def load_intensity_data():
    df_intensity=pd.read_csv(r"design/result/intensity_trend/part-00000-230f148b-8c77-4f42-bc0c-4d0236d48799-c000.csv")
    return df_intensity
df_intensity = load_intensity_data()
################################################################################################################
from folium.plugins import HeatMap
@st.cache_resource
def generate_typhoon_heatmap(df_track, start_year, end_year):
# 过滤指定年份范围内的数据
    typhoon_data = df_track[(df_track['year'] >= start_year) & (df_track['year'] <= end_year)]
    # 创建 Folium 地图对象
    m = folium.Map(location=[20, 120], zoom_start=5)
    # 提取坐标数据
    heat_data = [[row['latitude'], row['longitude']] for index, row in typhoon_data.iterrows()]
    # 添加热力图层
    HeatMap(heat_data, radius=5, blur=10).add_to(m)
    
    return m
@st.cache_resource
def get_map_by_id(storm_id):
    typhoon = df_track[df_track['storm_id'] == storm_id]
    typhoon['latitude'] = typhoon['latitude'].astype(float)
    typhoon['longitude'] = typhoon['longitude'].astype(float)
    typhoon['date'] = pd.to_datetime(typhoon['date'])
    return get_map(typhoon[['latitude', 'longitude']].to_records(index=False), typhoon['date'])
@st.cache_resource
def get_map(coordinates, dates):
    m = folium.Map() #Folium 地图对象 
    m.fit_bounds(coordinates.tolist()) #调整地图视角
    folium.PolyLine(locations=coordinates, color='blue').add_to(m) #绘制一条蓝色的折线，表示台风路径
    folium.Marker(location=coordinates[0], popup="start").add_to(m) #起点标记
    for coord, date in zip(coordinates, dates):
        folium.Circle(location=coord,
                      color='yellow' if date.hour else 'orange').add_to(m)
    return m
################################################################################################################
st.markdown("### 一、时序分析")
with st.expander("热力图选项"):
    year_range = st.slider("选择年份范围", min_value=int(df_track['year'].min()), max_value=int(df_track['year'].max()), value=(1990, 2000), key="year_range")
    start_year, end_year = year_range
    radius = st.number_input("选择热力图半径", min_value=1, max_value=10, value=5, key="radius")
    blur = st.number_input("选择热力图模糊度", min_value=5, max_value=20, value=10, key="blur")
if st.button("显示热力图", key="show_heatmap"):
    heatmap = generate_typhoon_heatmap(df_track, start_year, end_year)
    st.components.v1.html(heatmap._repr_html_(), height=500)


    intensity_data = df_intensity[(df_intensity['year'] >= start_year) & (df_intensity['year'] <= end_year)]
    import plotly.express as px
    st.markdown("#### 强度趋势")
    fig = px.line(intensity_data, x='year', y='avg_central_pressure')
    st.plotly_chart(fig)

################################################################################################################
st.markdown("### 二、单台风轨迹可视化")

selected_year_for_id = st.number_input("输入年份", min_value=int(df_track['year'].min()), max_value=int(df_track['year'].max()),
                                       value=1990, key="selected_year_for_id")
filtered_df = df_track[(df_track['year'] == selected_year_for_id)]
selected_storm_id = st.selectbox("选择台风ID", filtered_df[['storm_id', 'year']].drop_duplicates()
                                 .sort_values(by='year', ascending=True).apply(lambda x: f"{x['storm_id']} ({x['year']})", axis=1), index=0)
selected_storm_id = int(selected_storm_id.split(" (")[0])

if st.button("显示地图", key="show_map"):
    typhoon_info = df_track[df_track['storm_id'] == selected_storm_id]
    avg_distance = df_distance[df_distance['storm_id'] == selected_storm_id]['avg_distance'].values[0]
    st.markdown(f"<div style='text-align: left;'><strong>台风等级:</strong> {typhoon_info['grade'].iloc[0]}<br><strong>平均移动距离:</strong> {avg_distance:.4f} km</div>", unsafe_allow_html=True)
    folium_map = get_map_by_id(selected_storm_id)
    st.components.v1.html(folium_map._repr_html_(), height=500)
    

    



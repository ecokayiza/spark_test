import streamlit as st
import pandas as pd
import folium


st.markdown("<h1 style='text-align: center;'>😎路径聚类</h1>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df_cluster2=pd.read_csv(r'design/result/clusters/cluster2/part-00000-2de41987-4dd4-4354-bb79-0d88682d2fe8-c000.csv')
    df_cluster3=pd.read_csv(r'design/result/clusters/cluster3/part-00000-44c3cb5e-cbaf-425f-bc3b-6e3dc2b8473f-c000.csv')
    df_cluster4=pd.read_csv(r'design/result/clusters/cluster4/part-00000-db54e985-6431-4359-b6e7-ff0de7c78cad-c000.csv')
    df_features=pd.read_csv(r'design/result/clusters/features/part-00000-532e7d9b-f021-41d5-b3f4-494d20e975cc-c000.csv')
    return df_cluster2,df_cluster3,df_cluster4,df_features
c2,c3,c4,features=load_data()


@st.cache_resource
def show_cluster(clusters):
    # 将聚类结果转换为 Pandas DataFrame
    clusters_pd = clusters[["prediction", "points"]]
    # 创建一个地图对象
    m = folium.Map(location=[20, 130], zoom_start=3)


    # 为每个聚类添加点
    for cluster in clusters_pd['prediction'].unique():
        if cluster == 0:
            color = 'red'
        elif cluster == 1:
            color = 'blue'
        elif cluster == 2:
            color = 'yellow'
        else:
            color = 'green'
 
        cluster_points = clusters_pd[clusters_pd['prediction'] == cluster]['points']
        for points in cluster_points:
            points=eval(points)
            folium.PolyLine(points, color=color, weight=0.2).add_to(m) 
    # 显示地图
    return m

st.markdown("### 一、提取的特征")
st.write(features.head())

st.markdown("### 二、查看聚类")
cluster_option = st.selectbox("选择聚类数", [2, 3, 4])

if cluster_option == 2:
    clusters=c2
elif cluster_option == 3:
    clusters=c3
elif cluster_option == 4:
    clusters=c4
if st.button("查看分布图"):
    folium_map = show_cluster(clusters)
    st.components.v1.html(folium_map._repr_html_(), height=500)
    st.markdown("##### 分布直方图")
    cluster_counts = clusters['prediction'].value_counts().sort_index()
    cluster_counts.index = cluster_counts.index.map({0: 'red', 1: 'blue', 2: 'yellow', 3: 'green'})
    st.bar_chart(cluster_counts)


    
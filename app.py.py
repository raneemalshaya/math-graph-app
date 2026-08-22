import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# إعداد عنوان الصفحة وتصميمها البسيط
st.title("📐 أداة تحليل وتتبع المخططات المستوية الرياضية")
st.write("هذه الأداة تحلل المخططات هندسياً، تفحص استواءها، تطبق صيغة أويلر، وتجد أقصر مسار بضغطة زر.")

# صندوق لإدخال الأضلاع من قبل المستخدم
edges_input = st.text_input("أدخل الأضلاع على شكل أزواج (مثال):", "(4, 2), (3, 1), (1, 4), (4, 3), (3, 2), (2, 1)")

col1, col2 = st.columns(2)
with col1:
    start_node = st.number_input("نقطة البداية للمسار:", min_value=1, value=1, step=1)
with col2:
    end_node = st.number_input("نقطة النهاية للمسار:", min_value=1, value=4, step=1)

if st.button("تشغيل التحليل الشامل"):
    try:
        # تحويل النص المدخل إلى قائمة أضلاع برمجية بأمان
        edges_list = eval(f"[{edges_input}]")
        
        # بناء المخطط
        G = nx.Graph()
        G.add_edges_from(edges_list)
        
        # فحص الاستواء
        is_planar, embedding = nx.check_planarity(G)
        
        # حساب خصائص أويلر
        V = G.number_of_nodes()
        E = G.number_of_edges()
        F = 2 - V + E if is_planar else "غير متاح (يوجد تقاطعات هندسية)"
        
        # إيجاد أقصر مسار
        try:
            shortest_path = nx.shortest_path(G, source=int(start_node), target=int(end_node))
        except:
            shortest_path = "لا يوجد مسار يربط بين هاتين النقطتين"
            
        # عرض النتائج في واجهة الموقع بمرتبة جميلة
        st.subheader("📊 نتائج التقرير الرياضي:")
        st.success(f"هل المخطط مستوٍ (Planar)؟ ➔ {is_planar}")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("عدد الرؤوس (V)", V)
        m2.metric("عدد الأضلاع (E)", E)
        m3.metric("عدد الأوجه (F)", F)
        
        st.info(f"📍 أقصر مسار من ({start_node}) إلى ({end_node}): **{shortest_path}**")
        
        # رسم المخطط وعرضه في الواجهة
        fig, ax = plt.subplots(figsize=(6, 4))
        pos = nx.planar_layout(G) if is_planar else nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, font_weight='bold', ax=ax)
        
        if isinstance(shortest_path, list) and len(shortest_path) > 1:
            path_edges = list(zip(shortest_path, shortest_path[1:]))
            nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color='red', node_size=700, ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, ax=ax)
            
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"حدث خطأ في صياغة الإدخال، تأكد من كتابة الأضلاع بالطريقة الصحيحة. التفاصيل: {e}")
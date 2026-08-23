import ast
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt


# ==========================================
# إعداد الصفحة
# ==========================================
st.set_page_config(
    page_title="محلل المخططات الرياضية",
    page_icon="📐",
    layout="wide"
)


# ==========================================
# تنسيق الواجهة والخط العربي
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');

html, body, [class*="css"], [data-testid="stAppViewContainer"] {
    font-family: 'Tajawal', sans-serif !important;
    direction: rtl;
    text-align: right;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f8fbff 0%, #eef5ff 100%);
}

[data-testid="stSidebar"] {
    direction: rtl;
    text-align: right;
}

h1, h2, h3 {
    font-family: 'Tajawal', sans-serif !important;
    color: #17365d;
    font-weight: 800 !important;
}

p, label, span, div, button, input {
    font-family: 'Tajawal', sans-serif !important;
}

.stTextInput input,
.stNumberInput input {
    direction: ltr;
    text-align: left;
    border-radius: 10px;
}

.stSelectbox div[data-baseweb="select"] {
    direction: rtl;
}

.stButton > button {
    width: 100%;
    min-height: 48px;
    color: white;
    background: linear-gradient(90deg, #1d4e89, #2878c7);
    border: none;
    border-radius: 12px;
    font-size: 17px;
    font-weight: 700;
    transition: 0.2s;
}

.stButton > button:hover {
    color: white;
    background: linear-gradient(90deg, #163d6c, #1f66ad);
    border: none;
    transform: translateY(-1px);
}

[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #dce8f5;
    border-radius: 14px;
    padding: 15px;
    box-shadow: 0 4px 12px rgba(23, 54, 93, 0.06);
}

[data-testid="stMetricLabel"],
[data-testid="stMetricValue"] {
    direction: rtl;
    text-align: center;
}

.app-description {
    background-color: white;
    padding: 16px 20px;
    border-right: 5px solid #2878c7;
    border-radius: 12px;
    color: #334155;
    line-height: 1.9;
    margin-bottom: 22px;
    box-shadow: 0 4px 12px rgba(23, 54, 93, 0.05);
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# دوال مساعدة
# ==========================================
def parse_edges(edges_text):
    """تحويل الإدخال النصي إلى قائمة أضلاع والتحقق منه."""
    if not edges_text.strip():
        raise ValueError("لم يتم إدخال أي أضلاع.")

    try:
        edges = ast.literal_eval(f"[{edges_text}]")
    except (ValueError, SyntaxError):
        raise ValueError(
            "صيغة الأضلاع غير صحيحة. استخدمي مثلًا: (1,2), (2,3), (3,1)"
        )

    if not isinstance(edges, list) or len(edges) == 0:
        raise ValueError("يجب إدخال ضلع واحد على الأقل.")

    cleaned_edges = []

    for edge in edges:
        if not isinstance(edge, (tuple, list)) or len(edge) != 2:
            raise ValueError("كل ضلع يجب أن يحتوي على رأسين فقط، مثل: (1,2)")

        node1, node2 = edge

        if not isinstance(node1, int) or not isinstance(node2, int):
            raise ValueError("يجب أن تكون أسماء الرؤوس أرقامًا صحيحة.")

        if node1 == node2:
            raise ValueError(
                f"الحلقة ({node1},{node2}) غير مسموحة في هذا الإصدار."
            )

        cleaned_edges.append((node1, node2))

    # حذف الأضلاع المكررة
    return list(dict.fromkeys(cleaned_edges))


def get_layout(graph, layout_name, is_planar):
    """اختيار طريقة توزيع الرؤوس."""
    if layout_name == "تلقائي":
        if is_planar:
            return nx.planar_layout(graph)

        if nx.is_bipartite(graph):
            colors = nx.bipartite.color(graph)
            first_group = [
                node for node, color in colors.items() if color == 0
            ]
            return nx.bipartite_layout(
                graph,
                nodes=first_group,
                align="vertical"
            )

        return nx.kamada_kawai_layout(graph)

    if layout_name == "مستوٍ Planar":
        if not is_planar:
            raise ValueError(
                "لا يمكن استخدام التخطيط المستوي لأن المخطط غير مستوٍ."
            )
        return nx.planar_layout(graph)

    if layout_name == "ثنائي الأجزاء Bipartite":
        if not nx.is_bipartite(graph):
            raise ValueError(
                "هذا التخطيط متاح فقط للمخططات ثنائية الأجزاء."
            )

        colors = nx.bipartite.color(graph)
        first_group = [
            node for node, color in colors.items() if color == 0
        ]

        return nx.bipartite_layout(
            graph,
            nodes=first_group,
            align="vertical"
        )

    if layout_name == "نابضي Spring":
        return nx.spring_layout(graph, seed=42)

    if layout_name == "كاماتا–كاواي":
        return nx.kamada_kawai_layout(graph)

    if layout_name == "طيفي Spectral":
        return nx.spectral_layout(graph)

    if layout_name == "صدفي Shell":
        return nx.shell_layout(graph)

    if layout_name == "دائري Circular":
        return nx.circular_layout(graph)

    return nx.spring_layout(graph, seed=42)


# ==========================================
# عنوان التطبيق
# ==========================================
st.title("📐 أداة تحليل ورسم المخططات الرياضية")

st.markdown("""
<div class="app-description">
أداة تفاعلية لبناء المخططات الرياضية وتحليل خصائصها، وفحص استوائها،
وتطبيق صيغة أويلر، وإيجاد أقصر مسار بين رأسين مع توفير عدة طرق للرسم.
</div>
""", unsafe_allow_html=True)


# ==========================================
# إدخال البيانات
# ==========================================
st.subheader("✏️ بيانات المخطط")

edges_input = st.text_input(
    "أدخلي الأضلاع على شكل أزواج:",
    value="(1,4), (1,5), (1,6), (2,4), (2,5), (2,6), (3,4), (3,5), (3,6)",
    help="مثال: (1,2), (2,3), (3,1)"
)

input_col1, input_col2, input_col3 = st.columns(3)

with input_col1:
    start_node = st.number_input(
        "رأس بداية المسار:",
        min_value=0,
        value=1,
        step=1
    )

with input_col2:
    end_node = st.number_input(
        "رأس نهاية المسار:",
        min_value=0,
        value=6,
        step=1
    )

with input_col3:
    layout_name = st.selectbox(
        "طريقة الرسم:",
        [
            "تلقائي",
            "مستوٍ Planar",
            "ثنائي الأجزاء Bipartite",
            "نابضي Spring",
            "كاماتا–كاواي",
            "طيفي Spectral",
            "صدفي Shell",
            "دائري Circular"
        ]
    )


# ==========================================
# تشغيل التحليل
# ==========================================
if st.button("🔍 تشغيل التحليل الشامل", use_container_width=True):
    try:
        edges_list = parse_edges(edges_input)

        graph = nx.Graph()
        graph.add_edges_from(edges_list)

        # الخصائص الأساسية
        vertices_count = graph.number_of_nodes()
        edges_count = graph.number_of_edges()
        components_count = nx.number_connected_components(graph)

        is_connected = nx.is_connected(graph)
        is_planar, embedding = nx.check_planarity(graph)
        is_bipartite = nx.is_bipartite(graph)
        is_tree = nx.is_tree(graph)

        # صيغة أويلر للمخططات المستوية
        if is_planar:
            faces_count = (
                edges_count
                - vertices_count
                + components_count
                + 1
            )

            euler_left_side = (
                vertices_count
                - edges_count
                + faces_count
            )

            euler_right_side = components_count + 1
        else:
            faces_count = "غير متاح"
            euler_left_side = None
            euler_right_side = None

        # أقصر مسار
        shortest_path = None
        path_message = None

        try:
            shortest_path = nx.shortest_path(
                graph,
                source=int(start_node),
                target=int(end_node)
            )

            path_length = len(shortest_path) - 1

        except nx.NodeNotFound:
            path_message = "إحدى النقطتين غير موجودة في المخطط."

        except nx.NetworkXNoPath:
            path_message = "لا يوجد مسار يربط بين النقطتين."

        # طريقة توزيع الرسم
        positions = get_layout(
            graph,
            layout_name,
            is_planar
        )

        # ==========================================
        # عرض النتائج
        # ==========================================
        st.divider()
        st.subheader("📊 نتائج التحليل")

        if is_planar:
            st.success(
                "✅ المخطط مستوٍ ويمكن رسمه في المستوى دون تقاطع الأضلاع."
            )
        else:
            st.error(
                "❌ المخطط غير مستوٍ، ولا يمكن رسمه في المستوى دون تقاطع الأضلاع."
            )

        metric1, metric2, metric3, metric4 = st.columns(4)

        metric1.metric("عدد الرؤوس V", vertices_count)
        metric2.metric("عدد الأضلاع E", edges_count)
        metric3.metric("عدد الأوجه F", faces_count)
        metric4.metric("المكونات المتصلة", components_count)

        st.subheader("🧮 صيغة أويلر")

        if is_planar:
            if is_connected:
                st.info(
                    f"V − E + F = "
                    f"{vertices_count} − {edges_count} + {faces_count} "
                    f"= {euler_left_side} = 2"
                )
            else:
                st.info(
                    f"V − E + F = "
                    f"{vertices_count} − {edges_count} + {faces_count} "
                    f"= {euler_left_side} = C + 1 "
                    f"= {euler_right_side}"
                )
        else:
            st.warning(
                "لا تُطبّق صيغة أويلر الخاصة بالمخططات المستوية "
                "لأن المخطط غير مستوٍ."
            )

        # خصائص إضافية
        st.subheader("🧩 خصائص المخطط")

        property_col1, property_col2 = st.columns(2)

        with property_col1:
            st.write(
                f"**متصل:** {'نعم ✅' if is_connected else 'لا ❌'}"
            )
            st.write(
                f"**ثنائي الأجزاء:** {'نعم ✅' if is_bipartite else 'لا ❌'}"
            )

        with property_col2:
            st.write(
                f"**شجرة:** {'نعم ✅' if is_tree else 'لا ❌'}"
            )
            st.write(
                f"**مستوٍ:** {'نعم ✅' if is_planar else 'لا ❌'}"
            )

        # درجات الرؤوس
        degrees = dict(graph.degree())
        degrees_text = "، ".join(
            [f"{node}: {degree}" for node, degree in sorted(degrees.items())]
        )

        st.write(f"**درجات الرؤوس:** {degrees_text}")

        # أقصر مسار
        st.subheader("📍 أقصر مسار")

        if shortest_path is not None:
            path_text = " ← ".join(
                map(str, reversed(shortest_path))
            )

            st.info(
                f"أقصر مسار من {int(start_node)} إلى {int(end_node)}: "
                f"**{path_text}**\n\n"
                f"طول المسار: **{path_length}**"
            )
        else:
            st.warning(path_message)

        # ==========================================
        # رسم المخطط
        # ==========================================
        st.subheader("🎨 الرسم البياني")

        figure, axis = plt.subplots(figsize=(10, 6))

        figure.patch.set_facecolor("#f8fbff")
        axis.set_facecolor("#f8fbff")

        nx.draw_networkx_nodes(
            graph,
            positions,
            node_color="#80c5ed",
            edgecolors="#17365d",
            linewidths=1.8,
            node_size=1100,
            ax=axis
        )

        nx.draw_networkx_edges(
            graph,
            positions,
            edge_color="#64748b",
            width=2,
            alpha=0.85,
            ax=axis
        )

        nx.draw_networkx_labels(
            graph,
            positions,
            font_size=12,
            font_weight="bold",
            font_color="#102a43",
            ax=axis
        )

        # تمييز أقصر مسار
        if shortest_path is not None and len(shortest_path) > 1:
            path_edges = list(
                zip(shortest_path, shortest_path[1:])
            )

            nx.draw_networkx_nodes(
                graph,
                positions,
                nodelist=shortest_path,
                node_color="#ff6b6b",
                edgecolors="#9b1c1c",
                linewidths=2,
                node_size=1100,
                ax=axis
            )

            nx.draw_networkx_edges(
                graph,
                positions,
                edgelist=path_edges,
                edge_color="#d62828",
                width=4,
                ax=axis
            )

            nx.draw_networkx_labels(
                graph,
                positions,
                font_size=12,
                font_weight="bold",
                font_color="white",
                ax=axis
            )

        axis.set_title(
            f"طريقة الرسم: {layout_name}",
            fontsize=14,
            fontweight="bold",
            color="#17365d",
            pad=18
        )

        axis.axis("off")
        plt.tight_layout()

        st.pyplot(figure, use_container_width=True)
        plt.close(figure)

    except ValueError as error:
        st.error(f"⚠️ {error}")

    except Exception as error:
        st.error(
            "حدث خطأ غير متوقع أثناء تحليل المخطط."
        )
        st.code(str(error))

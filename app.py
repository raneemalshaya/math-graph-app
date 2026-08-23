import ast

import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st


# ==========================================
# إعداد الصفحة
# ==========================================
st.set_page_config(
    page_title="محلل المخططات الرياضية",
    page_icon="📐",
    layout="wide"
)


# ==========================================
# تصميم الواجهة والخط العربي
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');

/* الخط العام واتجاه الصفحة */
html,
body,
.stApp {
    font-family: 'Tajawal', sans-serif !important;
    direction: rtl;
    color-scheme: light !important;
}

/* خلفية التطبيق */
.stApp,
[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        135deg,
        #f8fbff 0%,
        #eaf3fb 100%
    ) !important;
    color: #1e293b !important;
}

/* أعلى الصفحة */
[data-testid="stHeader"] {
    background-color: transparent !important;
}

/* النصوص العامة */
p,
label,
.stMarkdown,
[data-testid="stWidgetLabel"],
[data-testid="stCaptionContainer"] {
    font-family: 'Tajawal', sans-serif !important;
    color: #26384d !important;
}

/* العناوين */
h1 {
    font-family: 'Tajawal', sans-serif !important;
    color: #123a63 !important;
    font-weight: 800 !important;
}

h2,
h3 {
    font-family: 'Tajawal', sans-serif !important;
    color: #1d4e79 !important;
    font-weight: 700 !important;
}

/* حقول الإدخال */
.stTextInput input,
.stNumberInput input {
    font-family: 'Tajawal', sans-serif !important;
    background-color: #ffffff !important;
    color: #172033 !important;
    border: 1px solid #b9cfe3 !important;
    border-radius: 10px !important;
    direction: ltr;
    text-align: left;
}

/* القائمة المنسدلة */
div[data-baseweb="select"] > div {
    font-family: 'Tajawal', sans-serif !important;
    background-color: #ffffff !important;
    color: #172033 !important;
    border-color: #b9cfe3 !important;
    border-radius: 10px !important;
}

/* زر التشغيل */
.stButton > button {
    width: 100%;
    min-height: 48px;
    font-family: 'Tajawal', sans-serif !important;
    color: #ffffff !important;
    background: linear-gradient(
        90deg,
        #174873,
        #2878b8
    ) !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    transition: 0.2s;
}

.stButton > button:hover {
    color: #ffffff !important;
    background: linear-gradient(
        90deg,
        #103553,
        #1f659d
    ) !important;
    transform: translateY(-1px);
}

/* بطاقات الإحصائيات */
[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border: 1px solid #cbdcea !important;
    border-radius: 14px !important;
    padding: 15px !important;
    box-shadow: 0 4px 12px rgba(23, 54, 93, 0.08);
}

[data-testid="stMetricLabel"] p {
    color: #50677d !important;
}

[data-testid="stMetricValue"] {
    color: #173f67 !important;
}

/* وصف التطبيق */
.app-description {
    background-color: #ffffff !important;
    color: #334155 !important;
    padding: 16px 20px;
    border-right: 5px solid #2878b8;
    border-radius: 12px;
    line-height: 1.9;
    margin-bottom: 22px;
    box-shadow: 0 4px 12px rgba(23, 54, 93, 0.06);
}

/* اتجاه العناصر العربية */
.stMarkdown,
[data-testid="stWidgetLabel"],
[data-testid="stAlert"] {
    direction: rtl;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# دالة قراءة الأضلاع
# ==========================================
def parse_edges(edges_text):
    """تحويل النص المدخل إلى قائمة أضلاع والتحقق من صحته."""

    if not edges_text.strip():
        raise ValueError("لم يتم إدخال أي أضلاع.")

    try:
        edges = ast.literal_eval(f"[{edges_text}]")
    except (ValueError, SyntaxError):
        raise ValueError(
            "صيغة الأضلاع غير صحيحة. "
            "استخدمي مثلًا: (1,2), (2,3), (3,1)"
        )

    if not isinstance(edges, list) or len(edges) == 0:
        raise ValueError("يجب إدخال ضلع واحد على الأقل.")

    cleaned_edges = []

    for edge in edges:
        if not isinstance(edge, (tuple, list)) or len(edge) != 2:
            raise ValueError(
                "كل ضلع يجب أن يحتوي على رأسين فقط، مثل: (1,2)"
            )

        node1, node2 = edge

        if not isinstance(node1, int) or not isinstance(node2, int):
            raise ValueError(
                "يجب أن تكون أسماء الرؤوس أرقامًا صحيحة."
            )

        if node1 == node2:
            raise ValueError(
                f"الحلقة ({node1},{node2}) غير مسموحة في هذا الإصدار."
            )

        cleaned_edges.append((node1, node2))

    # حذف الأضلاع المكررة
    unique_edges = []

    for node1, node2 in cleaned_edges:
        edge = tuple(sorted((node1, node2)))

        if edge not in unique_edges:
            unique_edges.append(edge)

    return unique_edges


# ==========================================
# دالة اختيار طريقة الرسم
# ==========================================
def get_layout(graph, layout_name, is_planar):
    """اختيار توزيع الرؤوس المناسب."""

    if layout_name == "تلقائي":
        if is_planar:
            return nx.planar_layout(graph)

        if nx.is_bipartite(graph):
            colors = nx.bipartite.color(graph)

            first_group = [
                node
                for node, color in colors.items()
                if color == 0
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
                "لا يمكن استخدام التخطيط المستوي؛ "
                "لأن المخطط غير مستوٍ."
            )

        return nx.planar_layout(graph)

    if layout_name == "ثنائي الأجزاء Bipartite":
        if not nx.is_bipartite(graph):
            raise ValueError(
                "هذا التخطيط متاح فقط للمخططات ثنائية الأجزاء."
            )

        colors = nx.bipartite.color(graph)

        first_group = [
            node
            for node, color in colors.items()
            if color == 0
        ]

        return nx.bipartite_layout(
            graph,
            nodes=first_group,
            align="vertical"
        )

    if layout_name == "نابضي Spring":
        return nx.spring_layout(
            graph,
            seed=42
        )

    if layout_name == "كاماتا–كاواي":
        return nx.kamada_kawai_layout(graph)

    if layout_name == "طيفي Spectral":
        return nx.spectral_layout(graph)

    if layout_name == "صدفي Shell":
        return nx.shell_layout(graph)

    if layout_name == "دائري Circular":
        return nx.circular_layout(graph)

    return nx.spring_layout(
        graph,
        seed=42
    )


# ==========================================
# عنوان التطبيق
# ==========================================
st.title("📐 أداة تحليل ورسم المخططات الرياضية")

st.markdown("""
<div class="app-description">
أداة تفاعلية لبناء المخططات الرياضية وتحليل خصائصها،
وفحص استوائها، وتطبيق صيغة أويلر، وإيجاد أقصر مسار
بين رأسين، مع توفير عدة طرق مختلفة للرسم.
</div>
""", unsafe_allow_html=True)


# ==========================================
# إدخال بيانات المخطط
# ==========================================
st.subheader("✏️ بيانات المخطط")

edges_input = st.text_input(
    "أدخلي الأضلاع على شكل أزواج:",
    value=(
        "(1,4), (1,5), (1,6), "
        "(2,4), (2,5), (2,6), "
        "(3,4), (3,5), (3,6)"
    ),
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
if st.button(
    "🔍 تشغيل التحليل الشامل",
    use_container_width=True
):
    try:
        # إنشاء المخطط
        edges_list = parse_edges(edges_input)

        graph = nx.Graph()
        graph.add_edges_from(edges_list)

        # حساب الخصائص الأساسية
        vertices_count = graph.number_of_nodes()
        edges_count = graph.number_of_edges()
        components_count = nx.number_connected_components(graph)

        is_connected = nx.is_connected(graph)
        is_planar, embedding = nx.check_planarity(graph)
        is_bipartite = nx.is_bipartite(graph)
        is_tree = nx.is_tree(graph)

        # حساب عدد الأوجه وصيغة أويلر
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

        # إيجاد أقصر مسار
        shortest_path = None
        path_message = None
        path_length = None

        try:
            shortest_path = nx.shortest_path(
                graph,
                source=int(start_node),
                target=int(end_node)
            )

            path_length = len(shortest_path) - 1

        except nx.NodeNotFound:
            path_message = (
                "إحدى النقطتين غير موجودة في المخطط."
            )

        except nx.NetworkXNoPath:
            path_message = (
                "لا يوجد مسار يربط بين النقطتين."
            )

        # اختيار شكل الرسم
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
                "✅ المخطط مستوٍ ويمكن رسمه في المستوى "
                "دون تقاطع الأضلاع."
            )
        else:
            st.error(
                "❌ المخطط غير مستوٍ، ولا يمكن رسمه "
                "في المستوى دون تقاطع الأضلاع."
            )

        metric1, metric2, metric3, metric4 = st.columns(4)

        metric1.metric(
            "عدد الرؤوس V",
            vertices_count
        )

        metric2.metric(
            "عدد الأضلاع E",
            edges_count
        )

        metric3.metric(
            "عدد الأوجه F",
            faces_count
        )

        metric4.metric(
            "المكونات المتصلة",
            components_count
        )

        # ==========================================
        # صيغة أويلر
        # ==========================================
        st.subheader("🧮 صيغة أويلر")

        if is_planar:
            if is_connected:
                st.info(
                    f"V − E + F = "
                    f"{vertices_count} − {edges_count} "
                    f"+ {faces_count} = "
                    f"{euler_left_side} = 2"
                )
            else:
                st.info(
                    f"V − E + F = "
                    f"{vertices_count} − {edges_count} "
                    f"+ {faces_count} = "
                    f"{euler_left_side} = C + 1 = "
                    f"{euler_right_side}"
                )
        else:
            st.warning(
                "لا تُطبّق صيغة أويلر الخاصة بالمخططات "
                "المستوية؛ لأن المخطط غير مستوٍ."
            )

        # ==========================================
        # خصائص إضافية
        # ==========================================
        st.subheader("🧩 خصائص المخطط")

        property_col1, property_col2 = st.columns(2)

        with property_col1:
            if is_connected:
                st.write("**متصل:** نعم ✅")
            else:
                st.write("**متصل:** لا ❌")

            if is_bipartite:
                st.write("**ثنائي الأجزاء:** نعم ✅")
            else:
                st.write("**ثنائي الأجزاء:** لا ❌")

        with property_col2:
            if is_tree:
                st.write("**شجرة:** نعم ✅")
            else:
                st.write("**شجرة:** لا ❌")

            if is_planar:
                st.write("**مستوٍ:** نعم ✅")
            else:
                st.write("**مستوٍ:** لا ❌")

        # درجات الرؤوس
        degrees = dict(graph.degree())

        degrees_text = "، ".join(
            [
                f"{node}: {degree}"
                for node, degree in sorted(degrees.items())
            ]
        )

        st.write(
            f"**درجات الرؤوس:** {degrees_text}"
        )

        # ==========================================
        # أقصر مسار
        # ==========================================
        st.subheader("📍 أقصر مسار")

        if shortest_path is not None:
            path_text = " ← ".join(
                map(str, reversed(shortest_path))
            )

            st.info(
                f"أقصر مسار من {int(start_node)} "
                f"إلى {int(end_node)}: "
                f"**{path_text}**  \n"
                f"طول المسار: **{path_length}**"
            )
        else:
            st.warning(path_message)

        # ==========================================
        # رسم المخطط
        # ==========================================
        st.subheader("🎨 الرسم البياني")

        figure, axis = plt.subplots(
            figsize=(10, 6)
        )

        figure.patch.set_facecolor("#f8fbff")
        axis.set_facecolor("#f8fbff")

        # رسم جميع الرؤوس
        nx.draw_networkx_nodes(
            graph,
            positions,
            node_color="#80c5ed",
            edgecolors="#17365d",
            linewidths=1.8,
            node_size=1100,
            ax=axis
        )

        # رسم جميع الأضلاع
        nx.draw_networkx_edges(
            graph,
            positions,
            edge_color="#64748b",
            width=2,
            alpha=0.85,
            ax=axis
        )

        # كتابة أرقام الرؤوس
        nx.draw_networkx_labels(
            graph,
            positions,
            font_size=12,
            font_weight="bold",
            font_color="#102a43",
            ax=axis
        )

        # تمييز أقصر مسار باللون الأحمر
        if (
            shortest_path is not None
            and len(shortest_path) > 1
        ):
            path_edges = list(
                zip(
                    shortest_path,
                    shortest_path[1:]
                )
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
                font_color="#ffffff",
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

        st.pyplot(
            figure,
            use_container_width=True
        )

        plt.close(figure)

    except ValueError as error:
        st.error(f"⚠️ {error}")

    except Exception as error:
        st.error(
            "حدث خطأ غير متوقع أثناء تحليل المخطط."
        )
        st.code(str(error))

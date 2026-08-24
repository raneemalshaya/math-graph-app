import ast

import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st


# ==========================================
# إعداد الصفحة
# ==========================================
st.set_page_config(
    page_title="محلل المخططات الرياضية",
    layout="wide"
)


# ==========================================
# تصميم التطبيق
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;600;700;800&display=swap');

html,
body,
.stApp,
.stApp * {
    font-family: 'Tajawal', sans-serif !important;
}

/* الخلفية تتبع وضع Streamlit:
   أبيض في اللايت وأسود في الدارك */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: var(--background-color) !important;
    color: var(--text-color) !important;
}

[data-testid="stHeader"] {
    background-color: var(--background-color) !important;
}

/* مساحة المحتوى */
[data-testid="stMainBlockContainer"] {
    background-color: transparent !important;
    padding-top: 2.5rem !important;
    padding-bottom: 3rem !important;
}

/* اتجاه الصفحة */
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"] {
    direction: rtl !important;
}

/* النصوص */
.stMarkdown,
.stMarkdown p,
.stMarkdown li,
.stMarkdown div,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
[data-testid="stAlert"],
[data-testid="stAlert"] p {
    direction: rtl !important;
    text-align: right !important;
    color: var(--text-color) !important;
}

/* العنوان الرئيسي */
.main-title {
    direction: rtl;
    text-align: center !important;
    color: var(--text-color) !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    line-height: 1.5;
    margin: 0 0 20px 0;
}

/* العناوين الفرعية */
h2,
h3 {
    direction: rtl !important;
    text-align: right !important;
    color: var(--text-color) !important;
    font-weight: 700 !important;
}

h2 {
    font-size: 1.45rem !important;
}

h3 {
    font-size: 1.25rem !important;
}

/* وصف التطبيق */
.app-description {
    direction: rtl;
    text-align: right;
    background-color: var(--secondary-background-color) !important;
    color: var(--text-color) !important;
    padding: 17px 20px;
    border: 1px solid #2998df;
    border-right: 6px solid #2998df;
    border-radius: 13px;
    line-height: 1.9;
    margin-bottom: 23px;
    box-shadow: 0 4px 14px rgba(41, 152, 223, 0.18);
}

/* وصف المثال */
.example-description {
    direction: rtl;
    text-align: right;
    background-color: var(--secondary-background-color) !important;
    color: var(--text-color) !important;
    padding: 14px 18px;
    border: 1px solid #2998df;
    border-right: 5px solid #2998df;
    border-radius: 11px;
    line-height: 1.8;
    margin: 8px 0 18px 0;
    box-shadow: 0 3px 12px rgba(41, 152, 223, 0.14);
}

/* عناوين الحقول */
[data-testid="stWidgetLabel"] {
    width: 100% !important;
}

[data-testid="stWidgetLabel"] p {
    width: 100% !important;
    text-align: right !important;
    color: var(--text-color) !important;
    font-weight: 600 !important;
}

/* حقول الإدخال */
.stTextInput,
.stNumberInput,
.stSelectbox {
    direction: rtl !important;
}

.stTextInput input {
    direction: ltr !important;
    text-align: left !important;
}

.stNumberInput input {
    direction: ltr !important;
    text-align: center !important;
}

.stTextInput input,
.stNumberInput input,
div[data-baseweb="select"] > div {
    background-color: var(--secondary-background-color) !important;
    color: var(--text-color) !important;
    border: 1.5px solid #2998df !important;
    border-radius: 10px !important;
}

/* القائمة المنسدلة */
div[data-baseweb="select"],
div[data-baseweb="select"] > div,
div[data-baseweb="select"] span {
    direction: rtl !important;
    text-align: right !important;
    color: var(--text-color) !important;
}

div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[role="listbox"] {
    direction: rtl !important;
    text-align: right !important;
    background-color: var(--secondary-background-color) !important;
    color: var(--text-color) !important;
}

li[role="option"] {
    direction: rtl !important;
    text-align: right !important;
    color: var(--text-color) !important;
}

/* زر تشغيل التحليل */
.stButton > button {
    width: 100% !important;
    min-height: 52px !important;
    background: linear-gradient(
        90deg,
        #075d9c,
        #1594e3,
        #075d9c
    ) !important;
    color: #ffffff !important;
    border: 2px solid #75caff !important;
    border-radius: 12px !important;
    font-size: 18px !important;
    font-weight: 800 !important;
    box-shadow: 0 5px 17px rgba(21, 148, 227, 0.38);
}

.stButton > button p,
.stButton > button span,
.stButton > button div {
    color: #ffffff !important;
    fill: #ffffff !important;
    text-align: center !important;
    font-size: 18px !important;
    font-weight: 800 !important;
}

.stButton > button:hover {
    background: linear-gradient(
        90deg,
        #054b7d,
        #0879be,
        #054b7d
    ) !important;
    color: #ffffff !important;
    border-color: #c2ebff !important;
}

/* بطاقات النتائج الأصلية */
[data-testid="stMetric"] {
    direction: rtl !important;
    text-align: center !important;
    background-color: var(--secondary-background-color) !important;
    color: var(--text-color) !important;
    border: 2px solid #2998df !important;
    border-top: 5px solid #1594e3 !important;
    border-radius: 14px !important;
    padding: 14px 10px !important;
    min-height: 105px !important;
    height: auto !important;
    box-shadow: 0 5px 15px rgba(21, 148, 227, 0.20);
}

/* منع البطاقات من التمدد */
[data-testid="stMetric"] > div {
    height: auto !important;
    min-height: 0 !important;
}

/* عنوان ورقم البطاقة */
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p,
[data-testid="stMetricValue"] {
    direction: rtl !important;
    text-align: center !important;
    color: var(--text-color) !important;
}

[data-testid="stMetricLabel"] p {
    font-size: 1rem !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    font-size: 2.15rem !important;
    font-weight: 800 !important;
}

/* صندوق صيغة أويلر */
.formula-box {
    direction: ltr;
    text-align: center !important;
    background-color: var(--secondary-background-color) !important;
    color: var(--text-color) !important;
    border: 2px solid #2998df;
    border-radius: 12px;
    padding: 17px 10px;
    margin: 8px 0 22px 0;
    font-family: Arial, sans-serif !important;
    font-size: clamp(16px, 4vw, 22px);
    font-weight: 700;
    line-height: 1.7;
    overflow-x: auto;
    white-space: nowrap;
    box-shadow: 0 4px 14px rgba(21, 148, 227, 0.18);
}

/* رسائل النتائج */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-width: 1px !important;
}

/* الخط الفاصل */
hr {
    border-color: #2998df !important;
    opacity: 0.55;
}

/* تنسيق الجوال */
@media (max-width: 700px) {
    [data-testid="stMainBlockContainer"] {
        padding-top: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    .main-title {
        font-size: 1.55rem !important;
    }

    [data-testid="stMetric"] {
        min-height: 95px !important;
        padding: 11px 8px !important;
        margin-bottom: 7px !important;
    }

    [data-testid="stMetricLabel"] p {
        font-size: 0.92rem !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.85rem !important;
    }

    .formula-box {
        font-size: 16px;
        padding: 14px 8px;
    }

    .app-description,
    .example-description {
        padding: 13px 15px;
    }
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# الأمثلة الجاهزة
# ==========================================
EXAMPLES = {
    "مخطط مستوٍ": {
        "edges": "(1,2), (2,3), (3,4), (4,1), (1,3)",
        "start": 1,
        "end": 4,
        "layout": "تلقائي",
        "description": (
            "مثال لمخطط مستوٍ يمكن رسمه دون تقاطع الأضلاع، "
            "ويُستخدم لتجربة صيغة أويلر وحساب عدد الأوجه."
        )
    },

    "شجرة": {
        "edges": "(1,2), (1,3), (2,4), (2,5)",
        "start": 4,
        "end": 3,
        "layout": "تلقائي",
        "description": (
            "مثال لمخطط متصل لا يحتوي على دورات مغلقة. "
            "يحتوي على خمسة رؤوس وأربعة أضلاع."
        )
    },

    "K3,3 غير مستوٍ": {
        "edges": (
            "(1,4), (1,5), (1,6), "
            "(2,4), (2,5), (2,6), "
            "(3,4), (3,5), (3,6)"
        ),
        "start": 1,
        "end": 6,
        "layout": "ثنائي الأجزاء Bipartite",
        "description": (
            "مثال مشهور لمخطط ثنائي الأجزاء وغير مستوٍ. "
            "يتكون من مجموعتين، وفي كل مجموعة ثلاثة رؤوس."
        )
    },

    "إدخال مخصص": {
        "edges": "",
        "start": 1,
        "end": 2,
        "layout": "تلقائي",
        "description": (
            "اكتبي أضلاع مخططك الخاص، ثم حددي نقطة البداية "
            "ونقطة النهاية وطريقة الرسم."
        )
    }
}


# ==========================================
# طرق الرسم
# ==========================================
LAYOUT_OPTIONS = [
    "تلقائي",
    "مستوٍ Planar",
    "ثنائي الأجزاء Bipartite",
    "نابضي Spring",
    "دائري Circular"
]


# ==========================================
# القيم الأولية
# ==========================================
if "selected_example" not in st.session_state:
    st.session_state.selected_example = "مخطط مستوٍ"

if "edges_input" not in st.session_state:
    st.session_state.edges_input = EXAMPLES["مخطط مستوٍ"]["edges"]

if "start_node" not in st.session_state:
    st.session_state.start_node = EXAMPLES["مخطط مستوٍ"]["start"]

if "end_node" not in st.session_state:
    st.session_state.end_node = EXAMPLES["مخطط مستوٍ"]["end"]

if "layout_name" not in st.session_state:
    st.session_state.layout_name = EXAMPLES["مخطط مستوٍ"]["layout"]


# ==========================================
# تحميل المثال المحدد
# ==========================================
def load_selected_example():
    example = EXAMPLES[st.session_state.selected_example]

    st.session_state.edges_input = example["edges"]
    st.session_state.start_node = example["start"]
    st.session_state.end_node = example["end"]
    st.session_state.layout_name = example["layout"]


# ==========================================
# قراءة الأضلاع
# ==========================================
def parse_edges(edges_text):
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
        if (
            not isinstance(edge, (tuple, list))
            or len(edge) != 2
        ):
            raise ValueError(
                "كل ضلع يجب أن يحتوي على رأسين فقط، مثل: (1,2)"
            )

        node1, node2 = edge

        if (
            not isinstance(node1, int)
            or not isinstance(node2, int)
        ):
            raise ValueError(
                "يجب أن تكون أسماء الرؤوس أرقامًا صحيحة."
            )

        if node1 == node2:
            raise ValueError(
                f"الحلقة ({node1},{node2}) غير مسموحة."
            )

        normalized_edge = tuple(sorted((node1, node2)))

        if normalized_edge not in cleaned_edges:
            cleaned_edges.append(normalized_edge)

    return cleaned_edges


# ==========================================
# طريقة الرسم
# ==========================================
def get_layout(graph, layout_name, is_planar):

    # الرسم التلقائي
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

        # إذا لم يكن مستويًا ولا ثنائي الأجزاء
        # يستخدم الرسم النابضي
        return nx.spring_layout(graph, seed=42)

    # الرسم المستوي
    if layout_name == "مستوٍ Planar":
        if not is_planar:
            raise ValueError(
                "لا يمكن استخدام التخطيط المستوي؛ "
                "لأن المخطط غير مستوٍ."
            )

        return nx.planar_layout(graph)

    # الرسم ثنائي الأجزاء
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

    # الرسم النابضي
    if layout_name == "نابضي Spring":
        return nx.spring_layout(graph, seed=42)

    # الرسم الدائري
    if layout_name == "دائري Circular":
        return nx.circular_layout(graph)

    return nx.spring_layout(graph, seed=42)


# ==========================================
# واجهة التطبيق
# ==========================================
st.markdown(
    '<h1 class="main-title"> أداة تحليل ورسم المخططات الرياضية</h1>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="app-description">
أداة تعليمية تفاعلية لبناء المخططات الرياضية وتحليل
خصائصها، وفحص استوائها، وتطبيق صيغة أويلر،
وإيجاد أقصر مسار بين رأسين، مع توفير عدة طرق للرسم.
</div>
""", unsafe_allow_html=True)


# الأمثلة
st.subheader("📐 أمثلة جاهزة للتجربة")

st.selectbox(
    "اختاري مثالًا جاهزًا أو أدخلي مخططك الخاص:",
    list(EXAMPLES.keys()),
    key="selected_example",
    on_change=load_selected_example
)

current_example = EXAMPLES[
    st.session_state.selected_example
]

st.markdown(
    f"""
    <div class="example-description">
        <strong>عن المثال:</strong>
        {current_example["description"]}
    </div>
    """,
    unsafe_allow_html=True
)


# بيانات المخطط
st.subheader("✏️ بيانات المخطط")

edges_input = st.text_input(
    "أدخلي الأضلاع على شكل أزواج:",
    key="edges_input",
    help="مثال: (1,2), (2,3), (3,1)"
)

input_col1, input_col2, input_col3 = st.columns(3)

with input_col1:
    start_node = st.number_input(
        "رأس بداية المسار:",
        min_value=0,
        step=1,
        key="start_node"
    )

with input_col2:
    end_node = st.number_input(
        "رأس نهاية المسار:",
        min_value=0,
        step=1,
        key="end_node"
    )

with input_col3:
    layout_name = st.selectbox(
        "طريقة الرسم:",
        LAYOUT_OPTIONS,
        key="layout_name"
    )


# ==========================================
# تشغيل التحليل
# ==========================================
if st.button(
    "▶ تشغيل التحليل الشامل",
    use_container_width=True
):
    try:
        edges_list = parse_edges(edges_input)

        graph = nx.Graph()
        graph.add_edges_from(edges_list)

        vertices_count = graph.number_of_nodes()
        edges_count = graph.number_of_edges()
        components_count = nx.number_connected_components(graph)

        is_connected = nx.is_connected(graph)
        is_planar, embedding = nx.check_planarity(graph)
        is_bipartite = nx.is_bipartite(graph)
        is_tree = nx.is_tree(graph)

        # صيغة أويلر
        if is_planar:
            faces_count = (
                edges_count
                - vertices_count
                + components_count
                + 1
            )

            euler_result = (
                vertices_count
                - edges_count
                + faces_count
            )

        else:
            faces_count = "غير متاح"
            euler_result = None

        # أقصر مسار
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

        positions = get_layout(
            graph,
            layout_name,
            is_planar
        )

        # النتائج
        st.divider()
        st.subheader("📊 نتائج التحليل")

        if is_planar:
            st.success(
                "✅ المخطط مستوٍ ويمكن رسمه "
                "في المستوى دون تقاطع الأضلاع."
            )
        else:
            st.error(
                "❌ المخطط غير مستوٍ، ولا يمكن رسمه "
                "في المستوى دون تقاطع الأضلاع."
            )

        # بطاقات Streamlit الأصلية
        metric1, metric2, metric3, metric4 = st.columns(4)

        metric1.metric(
            "عدد الرؤوس (V)",
            vertices_count
        )

        metric2.metric(
            "عدد الأضلاع (E)",
            edges_count
        )

        metric3.metric(
            "عدد الأوجه (F)",
            faces_count
        )

        metric4.metric(
            "المكونات المتصلة",
            components_count
        )

        # صيغة أويلر
        st.subheader("🧮 صيغة أويلر")

        if is_planar:
            if is_connected:
                formula_text = (
                    f"V − E + F = "
                    f"{vertices_count} − {edges_count} "
                    f"+ {faces_count} = {euler_result}"
                )
            else:
                formula_text = (
                    f"V − E + F = "
                    f"{vertices_count} − {edges_count} "
                    f"+ {faces_count} = {euler_result} = C + 1"
                )

            st.markdown(
                f'<div class="formula-box">{formula_text}</div>',
                unsafe_allow_html=True
            )

        else:
            st.warning(
                "لا تُطبّق صيغة أويلر الخاصة بالمخططات "
                "المستوية؛ لأن المخطط غير مستوٍ."
            )

        # خصائص المخطط
        st.subheader("🧩 خصائص المخطط")

        property_col1, property_col2 = st.columns(2)

        with property_col1:
            st.write(
                f"**متصل:** {'نعم ✅' if is_connected else 'لا ❌'}"
            )

            st.write(
                f"**ثنائي الأجزاء:** "
                f"{'نعم ✅' if is_bipartite else 'لا ❌'}"
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
            [
                f"{node}: {degree}"
                for node, degree in sorted(degrees.items())
            ]
        )

        st.write(
            f"**درجات الرؤوس:** {degrees_text}"
        )

        # أقصر مسار
        st.subheader("📍 أقصر مسار")

        if shortest_path is not None:
            path_text = " ← ".join(
                map(str, reversed(shortest_path))
            )

            st.info(
                f"أقصر مسار من {int(start_node)} "
                f"إلى {int(end_node)}: **{path_text}**  \n"
                f"طول المسار: **{path_length}**"
            )

        else:
            st.warning(path_message)

        # الرسم البياني
        st.subheader("🎨 الرسم البياني")

        figure, axis = plt.subplots(figsize=(10, 6))

        figure.patch.set_facecolor("#EEF5FA")
        axis.set_facecolor("#EEF5FA")

        nx.draw_networkx_nodes(
            graph,
            positions,
            node_color="#65B9EC",
            edgecolors="#174A6B",
            linewidths=1.8,
            node_size=1100,
            ax=axis
        )

        nx.draw_networkx_edges(
            graph,
            positions,
            edge_color="#52758D",
            width=2,
            alpha=0.9,
            ax=axis
        )

        nx.draw_networkx_labels(
            graph,
            positions,
            font_size=12,
            font_weight="bold",
            font_color="#102F47",
            ax=axis
        )

        # تمييز أقصر مسار
        if (
            shortest_path is not None
            and len(shortest_path) > 1
        ):
            path_edges = list(
                zip(shortest_path, shortest_path[1:])
            )

            nx.draw_networkx_nodes(
                graph,
                positions,
                nodelist=shortest_path,
                node_color="#F05D68",
                edgecolors="#9B1C28",
                linewidths=2,
                node_size=1100,
                ax=axis
            )

            nx.draw_networkx_edges(
                graph,
                positions,
                edgelist=path_edges,
                edge_color="#D62838",
                width=4,
                ax=axis
            )

            nx.draw_networkx_labels(
                graph,
                positions,
                font_size=12,
                font_weight="bold",
                font_color="#FFFFFF",
                ax=axis
            )

        axis.set_title(
            f"طريقة الرسم: {layout_name}",
            fontsize=14,
            fontweight="bold",
            color="#17365D",
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

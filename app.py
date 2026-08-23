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
# تحديد الوضع الحالي
# ==========================================
try:
    theme_type = st.context.theme.type
except Exception:
    theme_type = "light"


if theme_type == "dark":
    COLORS = {
        "background": "#0B1724",
        "surface": "#152A3D",
        "surface_alt": "#1D3B53",
        "text": "#F4F8FC",
        "muted": "#C5D8E8",
        "border": "#438FC1",
        "primary": "#168DE0",
        "primary_dark": "#0862A4",
        "formula": "#173C59",
        "formula_text": "#F2FAFF",
        "graph": "#12283A",
        "graph_text": "#F4F8FC",
        "edge": "#91B5CE"
    }
else:
    COLORS = {
        "background": "#F2F7FC",
        "surface": "#FFFFFF",
        "surface_alt": "#E4F1FB",
        "text": "#17324A",
        "muted": "#506A7E",
        "border": "#80BDE5",
        "primary": "#147FC5",
        "primary_dark": "#075B97",
        "formula": "#DCEFFF",
        "formula_text": "#124C75",
        "graph": "#EEF6FC",
        "graph_text": "#102F47",
        "edge": "#52758D"
    }


# متغيرات الألوان
st.markdown(
    f"""
    <style>
    :root {{
        --app-background: {COLORS["background"]};
        --app-surface: {COLORS["surface"]};
        --app-surface-alt: {COLORS["surface_alt"]};
        --app-text: {COLORS["text"]};
        --app-muted: {COLORS["muted"]};
        --app-border: {COLORS["border"]};
        --app-primary: {COLORS["primary"]};
        --app-primary-dark: {COLORS["primary_dark"]};
        --formula-background: {COLORS["formula"]};
        --formula-text: {COLORS["formula_text"]};
    }}
    </style>
    """,
    unsafe_allow_html=True
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

/* الخلفية */
.stApp,
[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        145deg,
        var(--app-background) 0%,
        var(--app-surface-alt) 160%
    ) !important;
    color: var(--app-text) !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

/* مساحة المحتوى */
[data-testid="stMainBlockContainer"] {
    padding-top: 2.5rem !important;
    padding-bottom: 3rem !important;
}

/* الاتجاه العربي */
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"] {
    direction: rtl !important;
}

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
    color: var(--app-text) !important;
}

/* العنوان */
.main-title {
    direction: rtl;
    text-align: center !important;
    color: var(--app-text) !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    line-height: 1.5;
    margin: 0 0 20px 0;
}

h2,
h3 {
    direction: rtl !important;
    text-align: right !important;
    color: var(--app-text) !important;
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
    background: var(--app-surface) !important;
    color: var(--app-text) !important;
    padding: 17px 20px;
    border: 1px solid var(--app-border);
    border-right: 5px solid var(--app-primary);
    border-radius: 13px;
    line-height: 1.9;
    margin-bottom: 23px;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.14);
}

/* وصف المثال */
.example-description {
    direction: rtl;
    text-align: right;
    background: var(--app-surface-alt) !important;
    color: var(--app-text) !important;
    padding: 14px 18px;
    border: 1px solid var(--app-border);
    border-right: 4px solid var(--app-primary);
    border-radius: 11px;
    line-height: 1.8;
    margin: 8px 0 18px 0;
}

/* عناوين الحقول */
[data-testid="stWidgetLabel"] {
    width: 100% !important;
}

[data-testid="stWidgetLabel"] p {
    width: 100% !important;
    text-align: right !important;
    color: var(--app-text) !important;
    font-weight: 600 !important;
}

/* الحقول */
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
    background: var(--app-surface) !important;
    color: var(--app-text) !important;
    border: 1px solid var(--app-border) !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"],
div[data-baseweb="select"] > div,
div[data-baseweb="select"] span {
    direction: rtl !important;
    text-align: right !important;
    color: var(--app-text) !important;
}

/* القائمة المفتوحة */
div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[role="listbox"] {
    direction: rtl !important;
    text-align: right !important;
    background: var(--app-surface) !important;
    color: var(--app-text) !important;
}

li[role="option"] {
    direction: rtl !important;
    text-align: right !important;
    color: var(--app-text) !important;
}

/* زر التشغيل */
.stButton > button {
    width: 100% !important;
    min-height: 54px !important;
    background: linear-gradient(
        90deg,
        var(--app-primary-dark),
        var(--app-primary),
        var(--app-primary-dark)
    ) !important;
    color: #FFFFFF !important;
    border: 2px solid #67C1FF !important;
    border-radius: 13px !important;
    font-size: 18px !important;
    font-weight: 800 !important;
    box-shadow: 0 6px 18px rgba(0, 112, 190, 0.40);
    transition: 0.2s;
}

.stButton > button p,
.stButton > button span,
.stButton > button div {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
    text-align: center !important;
    font-size: 18px !important;
    font-weight: 800 !important;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.50);
}

.stButton > button:hover {
    color: #FFFFFF !important;
    border-color: #B7E5FF !important;
    filter: brightness(1.1);
    transform: translateY(-1px);
}

/* شبكة بطاقات النتائج */
.metrics-grid {
    direction: rtl;
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
    width: 100%;
    margin: 15px 0 28px 0;
}

/* بطاقة النتيجة */
.metric-card {
    background: linear-gradient(
        145deg,
        var(--app-surface-alt),
        var(--app-surface)
    ) !important;
    border: 1.5px solid var(--app-border);
    border-top: 4px solid var(--app-primary);
    border-radius: 14px;
    min-height: 115px;
    padding: 14px 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: 0 5px 16px rgba(0, 0, 0, 0.16);
}

/* عنوان البطاقة */
.metric-title {
    direction: rtl;
    text-align: center !important;
    color: var(--app-muted) !important;
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 7px;
    line-height: 1.5;
}

/* رقم البطاقة */
.metric-value {
    direction: ltr;
    text-align: center !important;
    color: var(--app-text) !important;
    font-size: 2.25rem;
    font-weight: 800;
    line-height: 1.2;
}

/* صندوق صيغة أويلر */
.formula-card {
    direction: ltr;
    text-align: center !important;
    background: var(--formula-background) !important;
    color: var(--formula-text) !important;
    border: 1.5px solid var(--app-border);
    border-radius: 13px;
    padding: 18px 12px;
    margin: 10px 0 24px 0;
    font-family: Arial, sans-serif !important;
    font-size: clamp(17px, 4vw, 23px);
    font-weight: 700;
    line-height: 1.7;
    overflow-x: auto;
    white-space: nowrap;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.13);
}

/* رسائل Streamlit */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-width: 1px !important;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.10);
}

/* الخط الفاصل */
hr {
    border-color: var(--app-border) !important;
    opacity: 0.5;
}

/* الجوال */
@media (max-width: 700px) {
    [data-testid="stMainBlockContainer"] {
        padding-top: 2rem !important;
        padding-left: 0.9rem !important;
        padding-right: 0.9rem !important;
    }

    .main-title {
        font-size: 1.55rem !important;
        line-height: 1.55;
    }

    .metrics-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px;
    }

    .metric-card {
        min-height: 105px;
        padding: 11px 7px;
    }

    .metric-title {
        font-size: 0.88rem;
    }

    .metric-value {
        font-size: 1.9rem;
    }

    .formula-card {
        font-size: 16px;
        padding: 15px 8px;
    }

    .app-description,
    .example-description {
        padding: 13px 15px;
    }
}

/* الشاشات الصغيرة جدًا */
@media (max-width: 360px) {
    .metric-title {
        font-size: 0.8rem;
    }

    .metric-value {
        font-size: 1.7rem;
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


LAYOUT_OPTIONS = [
    "تلقائي",
    "مستوٍ Planar",
    "ثنائي الأجزاء Bipartite",
    "نابضي Spring",
    "كاماتا–كاواي",
    "طيفي Spectral",
    "صدفي Shell",
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
# تحميل المثال
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
# اختيار طريقة الرسم
# ==========================================
def get_layout(graph, layout_name, is_planar):
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
# واجهة التطبيق
# ==========================================
st.markdown(
    '<h1 class="main-title">📐 أداة تحليل ورسم المخططات الرياضية</h1>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="app-description">
أداة تعليمية تفاعلية لبناء المخططات الرياضية وتحليل
خصائصها، وفحص استوائها، وتطبيق صيغة أويلر،
وإيجاد أقصر مسار بين رأسين، مع توفير عدة طرق للرسم.
</div>
""", unsafe_allow_html=True)


# اختيار مثال
st.subheader("🧪 أمثلة جاهزة للتجربة")

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

        # ==========================================
        # النتائج
        # ==========================================
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

        # بطاقات النتائج المخصصة
        st.markdown(
            f"""
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-title">عدد الرؤوس (V)</div>
                    <div class="metric-value">{vertices_count}</div>
                </div>

                <div class="metric-card">
                    <div class="metric-title">عدد الأضلاع (E)</div>
                    <div class="metric-value">{edges_count}</div>
                </div>

                <div class="metric-card">
                    <div class="metric-title">عدد الأوجه (F)</div>
                    <div class="metric-value">{faces_count}</div>
                </div>

                <div class="metric-card">
                    <div class="metric-title">المكونات المتصلة</div>
                    <div class="metric-value">{components_count}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # صيغة أويلر
        st.subheader("🧮 صيغة أويلر")

        if is_planar:
            if is_connected:
                formula_text = (
                    f"{vertices_count} − {edges_count} "
                    f"+ {faces_count} = {euler_result}"
                )
            else:
                formula_text = (
                    f"{vertices_count} − {edges_count} "
                    f"+ {faces_count} = {euler_result} "
                    f"= C + 1"
                )

            st.markdown(
                f"""
                <div class="formula-card">
                    V − E + F = {formula_text}
                </div>
                """,
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

        # الرسم
        st.subheader("🎨 الرسم البياني")

        figure, axis = plt.subplots(figsize=(10, 6))

        figure.patch.set_facecolor(COLORS["graph"])
        axis.set_facecolor(COLORS["graph"])

        nx.draw_networkx_nodes(
            graph,
            positions,
            node_color="#50AEE8",
            edgecolors="#D3EEFF",
            linewidths=1.8,
            node_size=1100,
            ax=axis
        )

        nx.draw_networkx_edges(
            graph,
            positions,
            edge_color=COLORS["edge"],
            width=2,
            alpha=0.9,
            ax=axis
        )

        nx.draw_networkx_labels(
            graph,
            positions,
            font_size=12,
            font_weight="bold",
            font_color=COLORS["graph_text"],
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
                edgecolors="#FFD6D9",
                linewidths=2,
                node_size=1100,
                ax=axis
            )

            nx.draw_networkx_edges(
                graph,
                positions,
                edgelist=path_edges,
                edge_color="#FF4B55",
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
            color=COLORS["graph_text"],
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

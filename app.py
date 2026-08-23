import ast

import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st


# إعداد الصفحة
st.set_page_config(
    page_title="محلل المخططات الرياضية",
    
    layout="wide"
)


# تصميم التطبيق
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;600;700;800&display=swap');

html,
body,
.stApp,
.stApp * {
    font-family: 'Tajawal', sans-serif !important;
}

/* خلفية التطبيق المتغيرة مع الوضع */
.stApp,
[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        145deg,
        var(--background-color) 0%,
        color-mix(
            in srgb,
            var(--background-color) 82%,
            var(--primary-color) 18%
        ) 100%
    ) !important;
    color: var(--text-color) !important;
}

/* مساحة المحتوى */
[data-testid="stMainBlockContainer"] {
    background: color-mix(
        in srgb,
        var(--background-color) 92%,
        white 8%
    ) !important;
    border-radius: 18px;
    padding: 2rem 2.5rem !important;
    margin-top: 20px;
    margin-bottom: 30px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

/* أعلى الصفحة */
[data-testid="stHeader"] {
    background-color: transparent !important;
}

/* اتجاه الصفحة */
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"] {
    direction: rtl !important;
}

/* النصوص العربية */
.stMarkdown,
.stMarkdown p,
.stMarkdown li,
.stMarkdown div,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
[data-testid="stCaptionContainer"],
[data-testid="stAlert"],
[data-testid="stAlert"] p {
    direction: rtl !important;
    text-align: right !important;
    color: var(--text-color) !important;
}

/* العنوان الرئيسي */
h1 {
    direction: rtl !important;
    text-align: center !important;
    color: var(--text-color) !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    line-height: 1.4 !important;
    margin-bottom: 18px !important;
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
    font-size: 1.5rem !important;
}

h3 {
    font-size: 1.28rem !important;
}

/* وصف التطبيق */
.app-description {
    direction: rtl !important;
    text-align: right !important;
    background: color-mix(
        in srgb,
        var(--secondary-background-color) 82%,
        white 18%
    ) !important;
    color: var(--text-color) !important;
    padding: 17px 21px;
    border-right: 5px solid #3b9be5;
    border-radius: 13px;
    line-height: 1.9;
    margin-bottom: 22px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.14);
}

/* وصف المثال */
.example-description {
    direction: rtl !important;
    text-align: right !important;
    background: color-mix(
        in srgb,
        var(--secondary-background-color) 80%,
        #5ba8e6 20%
    ) !important;
    color: var(--text-color) !important;
    padding: 14px 18px;
    border-right: 4px solid #46a7ee;
    border-radius: 11px;
    line-height: 1.8;
    margin: 8px 0 18px 0;
    box-shadow: 0 3px 13px rgba(0, 0, 0, 0.13);
}

/* عناوين الحقول */
[data-testid="stWidgetLabel"] {
    width: 100% !important;
    display: flex !important;
    justify-content: flex-start !important;
}

[data-testid="stWidgetLabel"] p {
    width: 100% !important;
    text-align: right !important;
    font-weight: 600 !important;
}

/* خانة الأضلاع */
.stTextInput {
    direction: rtl !important;
}

.stTextInput input {
    direction: ltr !important;
    text-align: left !important;
    background: color-mix(
        in srgb,
        var(--secondary-background-color) 85%,
        white 15%
    ) !important;
    color: var(--text-color) !important;
    border: 1px solid color-mix(
        in srgb,
        var(--text-color) 35%,
        transparent
    ) !important;
    border-radius: 10px !important;
}

/* خانات الأرقام */
.stNumberInput {
    direction: rtl !important;
}

.stNumberInput input {
    direction: ltr !important;
    text-align: center !important;
    background: color-mix(
        in srgb,
        var(--secondary-background-color) 85%,
        white 15%
    ) !important;
    color: var(--text-color) !important;
}

/* القوائم المنسدلة */
.stSelectbox {
    direction: rtl !important;
    text-align: right !important;
}

div[data-baseweb="select"] > div {
    direction: rtl !important;
    text-align: right !important;
    background: color-mix(
        in srgb,
        var(--secondary-background-color) 85%,
        white 15%
    ) !important;
    color: var(--text-color) !important;
    border-color: color-mix(
        in srgb,
        var(--text-color) 35%,
        transparent
    ) !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] span {
    direction: rtl !important;
    text-align: right !important;
    color: var(--text-color) !important;
}

/* القائمة عند فتحها */
div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[role="listbox"] {
    direction: rtl !important;
    text-align: right !important;
    background: color-mix(
        in srgb,
        var(--secondary-background-color) 82%,
        white 18%
    ) !important;
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
    min-height: 54px !important;
    background: linear-gradient(
        90deg,
        #075ea8 0%,
        #1387dc 50%,
        #075ea8 100%
    ) !important;
    color: #ffffff !important;
    border: 2px solid #55b8ff !important;
    border-radius: 13px !important;
    font-size: 18px !important;
    font-weight: 800 !important;
    box-shadow: 0 6px 18px rgba(0, 119, 204, 0.35) !important;
    transition: 0.2s ease-in-out;
}

.stButton > button p,
.stButton > button span,
.stButton > button div {
    color: #ffffff !important;
    fill: #ffffff !important;
    text-align: center !important;
    font-size: 18px !important;
    font-weight: 800 !important;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.45);
}

.stButton > button:hover {
    color: #ffffff !important;
    background: linear-gradient(
        90deg,
        #064c88 0%,
        #0878c7 50%,
        #064c88 100%
    ) !important;
    border-color: #9ad8ff !important;
    box-shadow: 0 8px 22px rgba(0, 119, 204, 0.48) !important;
    transform: translateY(-2px);
}

/* بطاقات النتائج */
[data-testid="stMetric"] {
    direction: rtl !important;
    text-align: center !important;
    background: color-mix(
        in srgb,
        var(--secondary-background-color) 78%,
        white 22%
    ) !important;
    color: var(--text-color) !important;
    border: 1px solid color-mix(
        in srgb,
        var(--primary-color) 45%,
        transparent
    ) !important;
    border-radius: 14px !important;
    padding: 16px !important;
    box-shadow: 0 5px 16px rgba(0, 0, 0, 0.14);
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p,
[data-testid="stMetricValue"] {
    direction: rtl !important;
    text-align: center !important;
    color: var(--text-color) !important;
}

[data-testid="stMetricValue"] {
    font-weight: 800 !important;
}

/* رسائل النتائج */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-width: 1px !important;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.10);
}

/* الخط الفاصل */
hr {
    border-color: color-mix(
        in srgb,
        var(--text-color) 25%,
        transparent
    ) !important;
}

/* شريط التمرير */
::-webkit-scrollbar {
    width: 9px;
}

::-webkit-scrollbar-track {
    background: var(--background-color);
}

::-webkit-scrollbar-thumb {
    background: #268bd2;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# الأمثلة الجاهزة
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


# القيم الأولية
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


# تحميل المثال المحدد
def load_selected_example():
    example = EXAMPLES[st.session_state.selected_example]

    st.session_state.edges_input = example["edges"]
    st.session_state.start_node = example["start"]
    st.session_state.end_node = example["end"]
    st.session_state.layout_name = example["layout"]


# قراءة الأضلاع والتحقق منها
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
                "كل ضلع يجب أن يحتوي على رأسين فقط، "
                "مثل: (1,2)"
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
                f"الحلقة ({node1},{node2}) "
                "غير مسموحة في هذا الإصدار."
            )

        normalized_edge = tuple(sorted((node1, node2)))

        if normalized_edge not in cleaned_edges:
            cleaned_edges.append(normalized_edge)

    return cleaned_edges


# اختيار طريقة الرسم
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
                "هذا التخطيط متاح فقط "
                "للمخططات ثنائية الأجزاء."
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


# عنوان التطبيق
st.title(" أداة تحليل ورسم المخططات الرياضية")

st.markdown("""
<div class="app-description">
أداة تعليمية تفاعلية لبناء المخططات الرياضية وتحليل
خصائصها، وفحص استوائها، وتطبيق صيغة أويلر،
وإيجاد أقصر مسار بين رأسين، مع توفير عدة طرق للرسم.
</div>
""", unsafe_allow_html=True)


# اختيار المثال
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


# إدخال بيانات المخطط
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


# تشغيل التحليل
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

        # تطبيق صيغة أويلر
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

        positions = get_layout(
            graph,
            layout_name,
            is_planar
        )

        # نتائج التحليل
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
                st.info(
                    f"V − E + F = "
                    f"{vertices_count} − "
                    f"{edges_count} + "
                    f"{faces_count} = "
                    f"{euler_left_side} = 2"
                )

            else:
                st.info(
                    f"V − E + F = "
                    f"{vertices_count} − "
                    f"{edges_count} + "
                    f"{faces_count} = "
                    f"{euler_left_side} = "
                    f"C + 1 = {euler_right_side}"
                )

        else:
            st.warning(
                "لا تُطبّق صيغة أويلر الخاصة "
                "بالمخططات المستوية؛ "
                "لأن المخطط غير مستوٍ."
            )

        # خصائص المخطط
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
                for node, degree
                in sorted(degrees.items())
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
                f"أقصر مسار من "
                f"{int(start_node)} إلى "
                f"{int(end_node)}: "
                f"**{path_text}**  \n"
                f"طول المسار: "
                f"**{path_length}**"
            )

        else:
            st.warning(path_message)

        # رسم المخطط
        st.subheader("🎨 الرسم البياني")

        figure, axis = plt.subplots(figsize=(10, 6))

        figure.patch.set_facecolor("#eef5fb")
        axis.set_facecolor("#eef5fb")

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
            edge_color="#52697d",
            width=2,
            alpha=0.9,
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

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import re

# =========================================================
# إعداد الصفحة
# =========================================================

st.set_page_config(
    page_title="أداة تحليل المخططات المستوية",
    
    layout="wide"
)

# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: "Arial", sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    h1 {
        text-align: center !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem !important;
    }

    h2, h3 {
        text-align: right !important;
    }

    .subtitle {
        text-align: center;
        opacity: 0.8;
        margin-bottom: 2rem;
        font-size: 1rem;
    }

    div[data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,0.35);
        border-radius: 14px;
        padding: 12px;
    }

    div[data-testid="stMetricLabel"] {
        text-align: center;
    }

    div[data-testid="stMetricValue"] {
        text-align: center;
    }

    .info-box {
        border: 1px solid rgba(128,128,128,0.35);
        border-radius: 14px;
        padding: 15px 18px;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .success-box {
        border: 1px solid #2e7d32;
        border-radius: 14px;
        padding: 14px 18px;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .error-box {
        border: 1px solid #c62828;
        border-radius: 14px;
        padding: 14px 18px;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 700;
        padding: 0.7rem 1rem;
    }

    div[data-baseweb="select"] {
        direction: rtl;
        text-align: right;
    }

    textarea {
        direction: ltr !important;
        text-align: left !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# العنوان
# =========================================================

st.title( "أداة تحليل وتتبع المخططات المستوية الرياضية")

st.markdown(
    """
    <div class="subtitle">
    تحليل المخططات، فحص الاستواء، تطبيق صيغة أويلر،
    والتحقق من الاتصال والمسارات وعرض المخطط بطرق مختلفة.
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# دالة قراءة الأضلاع
# =========================================================

def parse_edges(text):
    """
    تقرأ مدخلات بالشكل:
    (1,2), (2,3), (3,1)
    """

    pairs = re.findall(r"\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)", text)

    edges = []

    for u, v in pairs:
        edges.append((int(u), int(v)))

    return edges


# =========================================================
# دالة الرسم
# =========================================================

def get_layout(G, layout_name):

    if layout_name == "Planar - مستوٍ":

        if nx.is_planar(G):
            return nx.planar_layout(G), None

        return (
            nx.spring_layout(G, seed=42),
            "❌ المخطط غير مستوٍ، لذلك لا يمكن عرضه بطريقة Planar. تم عرضه بطريقة Spring بدلًا منها."
        )


    elif layout_name == "Circular - دائري":

        return nx.circular_layout(G), None


    elif layout_name == "Bipartite - ثنائي التقسيم":

        if nx.is_bipartite(G):

            # تحديد أحد القسمين
            color = nx.bipartite.color(G)

            first_set = [
                node
                for node, group in color.items()
                if group == 0
            ]

            return (
                nx.bipartite_layout(
                    G,
                    nodes=first_set,
                    align="vertical"
                ),
                None
            )

        return (
            nx.spring_layout(G, seed=42),
            "⚠️ المخطط ليس ثنائي التقسيم، لذلك تم عرضه بطريقة Spring."
        )


    elif layout_name == "Spring - نابضي":

        return nx.spring_layout(G, seed=42), None


    return nx.spring_layout(G, seed=42), None


# =========================================================
# الإدخال
# =========================================================

st.subheader("✍️ إدخال المخطط")

st.write(
    "أدخلي الأضلاع على هيئة أزواج مرتبة، مثل:"
)

st.code(
    "(1,2), (2,3), (3,1)",
    language=None
)

edges_input = st.text_area(
    "الأضلاع:",
    placeholder="مثال: (1,2), (2,3), (3,4), (4,1)",
    height=110
)

# =========================================================
# طريقة الرسم
# =========================================================

layout_option = st.selectbox(
    "🎨 طريقة الرسم:",
    [
        "Planar - مستوٍ",
        "Circular - دائري",
        "Bipartite - ثنائي التقسيم",
        "Spring - نابضي"
    ]
)

# =========================================================
# تشغيل التحليل
# =========================================================

analyze = st.button(
    "▶ تشغيل التحليل الشامل",
    use_container_width=True
)

if analyze:

    # -----------------------------------------------------
    # التحقق من الإدخال
    # -----------------------------------------------------

    edges = parse_edges(edges_input)

    if not edges:

        st.error(
            "❌ لم يتم العثور على أضلاع صحيحة. استخدمي الصيغة مثل: (1,2), (2,3)"
        )

        st.stop()

    # -----------------------------------------------------
    # إنشاء Graph
    # -----------------------------------------------------

    G = nx.Graph()

    G.add_edges_from(edges)

    # -----------------------------------------------------
    # معلومات أساسية
    # -----------------------------------------------------

    num_vertices = G.number_of_nodes()
    num_edges = G.number_of_edges()
    num_components = nx.number_connected_components(G)

    is_connected = nx.is_connected(G)

    is_planar, embedding = nx.check_planarity(G)

    is_bipartite = nx.is_bipartite(G)

    # -----------------------------------------------------
    # الإحصائيات
    # -----------------------------------------------------

    st.divider()

    st.subheader("📊 معلومات المخطط")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "عدد الرؤوس (V)",
            num_vertices
        )

    with col2:
        st.metric(
            "عدد الأضلاع (E)",
            num_edges
        )

    with col3:
        st.metric(
            "المكونات المتصلة",
            num_components
        )

    with col4:
        st.metric(
            "ثنائي التقسيم",
            "نعم" if is_bipartite else "لا"
        )

    # -----------------------------------------------------
    # الاتصال
    # -----------------------------------------------------

    st.subheader("🔗 الاتصال")

    if is_connected:

        st.success(
            "✅ المخطط متصل؛ أي يمكن الوصول من أي رأس إلى أي رأس آخر عبر مسار."
        )

    else:

        st.warning(
            f"⚠️ المخطط غير متصل، ويتكون من {num_components} مكونات متصلة."
        )

    # -----------------------------------------------------
    # فحص الاستواء
    # -----------------------------------------------------

    st.subheader("📐 فحص الاستواء")

    if is_planar:

        st.success(
            "✅ المخطط مستوٍ (Planar Graph)، ويمكن رسمه في المستوى دون تقاطع الأضلاع."
        )

    else:

        st.error(
            "❌ المخطط غير مستوٍ (Non-Planar Graph)، ولا يمكن رسمه في المستوى دون تقاطع بعض الأضلاع."
        )

    # -----------------------------------------------------
    # صيغة أويلر
    # -----------------------------------------------------

    st.subheader("🧮 صيغة أويلر")

    if is_planar and is_connected:

        # للمخطط المستوي المتصل:
        # V - E + F = 2

        faces = 2 - num_vertices + num_edges

        st.markdown(
            f"""
            <div class="info-box">

            للمخطط المستوي المتصل نستخدم:

            <b>V − E + F = 2</b>

            <br><br>

            حيث:

            V = {num_vertices}<br>
            E = {num_edges}<br>
            F = {faces}

            <br><br>

            بالتعويض:

            <b>{num_vertices} − {num_edges} + {faces} = 2</b>

            </div>
            """,
            unsafe_allow_html=True
        )

    elif is_planar and not is_connected:

        # الصيغة العامة:
        # V - E + F = 1 + C

        faces = (
            1
            + num_components
            - num_vertices
            + num_edges
        )

        st.markdown(
            f"""
            <div class="info-box">

            لأن المخطط غير متصل نستخدم الصيغة العامة:

            <b>V − E + F = 1 + C</b>

            <br><br>

            حيث:

            V = {num_vertices}<br>
            E = {num_edges}<br>
            F = {faces}<br>
            C = {num_components}

            <br><br>

            بالتعويض:

            <b>{num_vertices} − {num_edges} + {faces}
            = {1 + num_components}</b>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "ℹ️ لا يتم حساب عدد الأوجه باستخدام صيغة أويلر هنا لأن المخطط غير مستوٍ."
        )

    # -----------------------------------------------------
    # درجات الرؤوس
    # -----------------------------------------------------

    st.subheader("🔢 درجات الرؤوس")

    degrees = dict(G.degree())

    degree_text = " | ".join(
        [
            f"{node}: {degree}"
            for node, degree in sorted(degrees.items())
        ]
    )

    st.write(degree_text)

    # -----------------------------------------------------
    # اختبار المصافحة
    # -----------------------------------------------------

    degree_sum = sum(degrees.values())

    st.markdown(
        f"""
        <div class="info-box">

        <b>نظرية المصافحة:</b>

        مجموع درجات الرؤوس = {degree_sum}

        <br>

        2 × عدد الأضلاع = {2 * num_edges}

        <br><br>

        {
            "✅ متساويان، وبالتالي تتحقق نظرية المصافحة."
            if degree_sum == 2 * num_edges
            else "❌ لا يوجد تطابق."
        }

        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # رسم المخطط
    # -----------------------------------------------------

    st.subheader("🖼️ رسم المخطط")

    pos, layout_message = get_layout(
        G,
        layout_option
    )

    if layout_message:

        if layout_option == "Planar - مستوٍ":
            st.error(layout_message)

        else:
            st.warning(layout_message)

    fig, ax = plt.subplots(
        figsize=(9, 6)
    )

    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax,
        node_size=1500
    )

    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax,
        width=2
    )

    nx.draw_networkx_labels(
        G,
        pos,
        ax=ax,
        font_size=12,
        font_weight="bold"
    )

    ax.set_title(
        layout_option,
        fontsize=13
    )

    ax.axis("off")

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)

    # -----------------------------------------------------
    # أقصر مسار
    # -----------------------------------------------------

    st.divider()

    st.subheader("🛣️ أقصر مسار")

    nodes = sorted(G.nodes())

    if len(nodes) >= 2:

        col_start, col_end = st.columns(2)

        with col_start:

            start_node = st.selectbox(
                "رأس البداية:",
                nodes,
                key="start_node"
            )

        with col_end:

            end_node = st.selectbox(
                "رأس النهاية:",
                nodes,
                index=1 if len(nodes) > 1 else 0,
                key="end_node"
            )

        if start_node == end_node:

            st.info(
                "اختاري رأسين مختلفين لحساب أقصر مسار."
            )

        else:

            try:

                shortest_path = nx.shortest_path(
                    G,
                    source=start_node,
                    target=end_node
                )

                shortest_distance = nx.shortest_path_length(
                    G,
                    source=start_node,
                    target=end_node
                )

                path_string = " → ".join(
                    map(str, shortest_path)
                )

                st.success(
                    f"✅ أقصر مسار: {path_string}"
                )

                st.write(
                    f"عدد الأضلاع في أقصر مسار: **{shortest_distance}**"
                )

            except nx.NetworkXNoPath:

                st.error(
                    f"❌ لا يوجد مسار بين الرأس {start_node} والرأس {end_node}."
                )

    # -----------------------------------------------------
    # معلومات طريقة الرسم
    # -----------------------------------------------------

    st.divider()

    st.subheader("🎨 ماذا تعني طريقة الرسم المختارة؟")

    layout_descriptions = {

        "Planar - مستوٍ":
            """
            **Planar Layout:** يرتب المخطط المستوي بحيث يمكن عرضه
            بدون تقاطع الأضلاع قدر الإمكان. وهو الأنسب لفحص
            المخططات المستوية بصريًا.
            """,

        "Circular - دائري":
            """
            **Circular Layout:** يضع جميع الرؤوس حول دائرة.
            يفيد في عرض الرؤوس بترتيب منتظم وواضح، لكنه لا يضمن
            عدم تقاطع الأضلاع.
            """,

        "Bipartite - ثنائي التقسيم":
            """
            **Bipartite Layout:** يستخدم عندما يمكن تقسيم الرؤوس
            إلى مجموعتين بحيث تكون الأضلاع بين المجموعتين فقط.
            وهو مناسب جدًا لمخططات مثل K₃,₃.
            """,

        "Spring - نابضي":
            """
            **Spring Layout:** يتعامل مع الأضلاع كأنها نوابض
            والرؤوس كأن بينها قوى، ثم يرتبها تلقائيًا للوصول
            إلى شكل متوازن بصريًا.
            """
    }

    st.info(
        layout_descriptions[
            layout_option
        ]
    )

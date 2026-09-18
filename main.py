import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# 기본 설정
# ============================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")

st.write(
    "1년간 박스오피스 10위권에 든 영화 가운데 "
    "이 기간에 개봉한 216편의 데이터를 다양한 그래프로 살펴봅니다."
)


# ============================================================
# 데이터 불러오기
# ============================================================

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_movies.csv"
)


@st.cache_data
def load_data():

    df = pd.read_csv(DATA_URL)

    # --------------------------------------------------------
    # 개봉일
    # --------------------------------------------------------

    df["openDt"] = (
        df["openDt"]
        .astype(str)
        .str.zfill(8)
    )

    # --------------------------------------------------------
    # 장르
    # 여러 장르가 "|"로 연결되어 있으면 첫 번째 장르만 사용
    # 예: 액션|범죄 → 액션
    # --------------------------------------------------------

    df["genre"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    # --------------------------------------------------------
    # 숫자 데이터 변환
    # --------------------------------------------------------

    numeric_columns = [
        "first_scrn",
        "first_show",
        "first_week_audi",
        "total_audi",
        "days_in_top10"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # 총 관객 수
    df["total_audi"] = df["total_audi"].fillna(0)

    # --------------------------------------------------------
    # 영화명
    # --------------------------------------------------------

    df["movieNm"] = (
        df["movieNm"]
        .fillna("영화명 없음")
        .astype(str)
    )

    return df


# ============================================================
# 데이터 불러오기 오류 처리
# ============================================================

try:
    df = load_data()

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.error(f"오류 내용: {e}")
    st.stop()


# ============================================================
# 데이터 요약
# ============================================================

st.subheader("📋 데이터 요약")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "전체 영화 수",
        f"{len(df):,}편"
    )

with col2:
    st.metric(
        "장르 수",
        f"{df['genre'].nunique():,}개"
    )


# ============================================================
# 그래프 1
# 장르별 영화 편수 - 도넛 그래프
# ============================================================

st.divider()

st.header("📊 그래프 1. 장르별 영화 편수")

st.write(
    "각 장르에 영화가 몇 편씩 있는지 도넛 그래프로 나타냈습니다."
)


genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = [
    "genre",
    "count"
]


fig1 = px.pie(
    genre_count,
    names="genre",
    values="count",
    hole=0.45,
    title="장르별 영화 편수"
)


fig1.update_traces(
    textposition="inside",
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)


fig1.update_layout(
    height=550,
    legend_title_text="장르"
)


st.plotly_chart(
    fig1,
    use_container_width=True
)


with st.container(border=True):

    st.markdown("### 💡 이 그래프로 알 수 있는 것")

    st.write(
        "장르별로 영화가 몇 편씩 분포되어 있는지 한눈에 비교할 수 있다."
    )


# ============================================================
# 그래프 2
# 장르 → 영화 트리맵
# 크기 = 총 관객 수
# ============================================================

st.divider()

st.header("📊 그래프 2. 장르별 영화와 총 관객 트리맵")

st.write(
    "장르 안에 각각의 영화를 표시하고, "
    "영화 칸의 크기를 총 관객 수에 따라 나타냈습니다."
)


fig2 = px.treemap(
    df,
    path=[
        "genre",
        "movieNm"
    ],
    values="total_audi",
    title="장르 안의 영화별 총 관객"
)


fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)


fig2.update_layout(
    height=700,
    margin=dict(
        t=60,
        l=10,
        r=10,
        b=10
    )
)


st.plotly_chart(
    fig2,
    use_container_width=True
)


with st.container(border=True):

    st.markdown("### 💡 이 그래프로 알 수 있는 것")

    st.write(
        "장르별로 어떤 영화가 많은 관객을 모았는지와 "
        "영화별 총 관객 규모의 차이를 알 수 있다."
    )


# ============================================================
# 그래프 3
# 총 관객 수 히스토그램
# ============================================================

st.divider()

st.header("📊 그래프 3. 총 관객 수 분포")

st.write(
    "영화들의 총 관객 수가 어느 구간에 많이 모여 있는지 "
    "히스토그램으로 확인합니다."
)


fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 수 분포",
    labels={
        "total_audi": "총 관객 수",
        "count": "영화 편수"
    }
)


fig3.update_traces(
    hovertemplate=(
        "총 관객 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)


fig3.update_layout(
    height=550,
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수"
)


st.plotly_chart(
    fig3,
    use_container_width=True
)


# ------------------------------------------------------------
# 대부분의 영화가 몰려 있는 구간 계산
# ------------------------------------------------------------

bins = pd.cut(
    df["total_audi"],
    bins=20,
    include_lowest=True
)

counts = bins.value_counts().sort_index()

most_common_bin = counts.idxmax()


# ------------------------------------------------------------
# 가장 관객이 많은 영화 찾기
# ------------------------------------------------------------

max_index = df["total_audi"].idxmax()

most_audience_movie = df.loc[
    max_index,
    "movieNm"
]

most_audience = df.loc[
    max_index,
    "total_audi"
]


with st.container(border=True):

    st.markdown("### 💡 이 그래프로 알 수 있는 것")

    st.write(
        f"대부분의 영화는 "
        f"**{most_common_bin.left:,.0f}명 ~ "
        f"{most_common_bin.right:,.0f}명** "
        f"구간에 몰려 있다."
    )

    st.write(
        f"가장 관객이 많은 영화는 "
        f"**{most_audience_movie}**이며, "
        f"총 관객은 **{most_audience:,.0f}명**이다."
    )


# ============================================================
# 그래프 4
# 개봉일 스크린 수와 총 관객의 관계 - 산점도
# ============================================================

st.divider()

st.header("📊 그래프 4. 개봉일 스크린 수와 총 관객의 관계")

st.write(
    "개봉일에 몇 개의 스크린에서 상영했는지와 "
    "최종적으로 얼마나 많은 관객을 모았는지의 관계를 나타냅니다."
)


# 산점도에 사용할 데이터
scatter_df = df[
    [
        "movieNm",
        "genre",
        "first_scrn",
        "total_audi"
    ]
].copy()


# 스크린 수 또는 총 관객이 없는 행 제거
scatter_df = scatter_df.dropna(
    subset=[
        "first_scrn",
        "total_audi"
    ]
)


# 음수 값 제거
scatter_df = scatter_df[
    (scatter_df["first_scrn"] >= 0)
    & (scatter_df["total_audi"] >= 0)
]


# ------------------------------------------------------------
# 산점도
# ------------------------------------------------------------

fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린 수와 총 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "genre": "장르"
    },
    hover_data={
        "movieNm": False,
        "genre": True,
        "first_scrn": ":,.0f",
        "total_audi": ":,.0f"
    }
)


fig4.update_traces(
    marker=dict(
        size=10,
        opacity=0.75
    )
)


fig4.update_layout(
    height=650,
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수",
    legend_title="장르"
)


st.plotly_chart(
    fig4,
    use_container_width=True
)


# ------------------------------------------------------------
# 그래프 4 설명
# ------------------------------------------------------------

with st.container(border=True):

    st.markdown("### 💡 이 그래프로 알 수 있는 것")

    st.write(
        "개봉일 스크린 수와 총 관객 수가 어떤 관계를 보이는지 "
        "영화별로 비교할 수 있으며, 장르에 따라 점의 색이 다르게 나타난다."
    )


# ============================================================
# 장르별 영화 편수 표
# ============================================================

st.divider()

st.subheader("📋 장르별 영화 편수")


genre_table = genre_count.copy()

genre_table["비율"] = (
    genre_table["count"]
    / genre_table["count"].sum()
    * 100
).round(1)


genre_table = genre_table.rename(
    columns={
        "genre": "장르",
        "count": "영화 편수"
    }
)


st.dataframe(
    genre_table,
    use_container_width=True,
    hide_index=True
)
# ==============================
# 5. 장르별 총 관객 수 상자 그림
# ==============================
st.subheader("5️⃣ 장르별 총 관객 수 분포")

# 영화가 10편 이상인 장르만 선택
genre_counts = df["genre"].value_counts()
selected_genres = genre_counts[genre_counts >= 10].index

box_df = df[df["genre"].isin(selected_genres)].copy()
box_df = box_df.dropna(subset=["total_audi"])

fig5 = px.box(
    box_df,
    x="genre",
    y="total_audi",
    color="genre",
    points="outliers",
    hover_name="movieNm",
    title="영화가 10편 이상인 장르별 총 관객 수 분포",
    labels={
        "genre": "장르",
        "total_audi": "총 관객 수"
    }
)

fig5.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    height=650,
    xaxis_title="장르",
    yaxis_title="총 관객 수",
    showlegend=False
)

st.plotly_chart(fig5, use_container_width=True)

# 그래프에서 알 수 있는 것
with st.container(border=True):
    st.markdown("### 💡 이 그래프로 알 수 있는 것")
    st.write(
        "영화가 10편 이상인 장르끼리 총 관객 수의 중앙값과 분포, "
        "그리고 다른 영화보다 유난히 관객이 많은 이상치를 비교할 수 있다."
    )
# ── 그래프 6. 첫 주 관객에 따른 버블 그래프 ──
st.header("6. 첫 주 관객에 따른 버블 그래프")

fig6 = px.scatter(
    df,
    x="first_week_audi",
    y="total_audi",
    size="first_week_audi",
    hover_name="movieNm",
    hover_data=["first_week_audi", "total_audi"],
    labels={
        "first_week_audi": "첫 주 관객",
        "total_audi": "총 관객"
    },
    title="첫 주 관객과 총 관객의 관계"
)

st.plotly_chart(fig6, width="stretch")
st.caption("이 그래프로 알 수 있는 것: 첫 주 관객이 많을수록 총 관객도 많은 경향이 있는지 버블의 크기와 위치를 통해 확인할 수 있다.")

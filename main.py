import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write(
    "1년간 박스오피스 10위권에 든 영화 가운데 "
    "이 기간에 개봉한 216편의 데이터를 살펴봅니다."
)

# -----------------------------
# 데이터 불러오기
# -----------------------------
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_movies.csv"
)

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 개봉일을 문자열로 처리
    df["openDt"] = df["openDt"].astype(str).str.zfill(8)

    # 장르가 여러 개라면 첫 번째 장르만 사용
    # 예: "액션|범죄" → "액션"
    df["genre"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    return df


try:
    df = load_data()

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.error(f"오류 내용: {e}")
    st.stop()


# -----------------------------
# 데이터 확인
# -----------------------------
st.subheader("📋 데이터 요약")

col1, col2 = st.columns(2)

with col1:
    st.metric("전체 영화 수", f"{len(df):,}편")

with col2:
    st.metric("장르 수", f"{df['genre'].nunique():,}개")


# -----------------------------
# 그래프 1
# -----------------------------
st.divider()

st.header("📊 그래프 1. 장르별 영화 편수")

genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["genre", "count"]

fig = px.pie(
    genre_count,
    names="genre",
    values="count",
    hole=0.45,
    title="장르별 영화 편수",
)

fig.update_traces(
    textposition="inside",
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig.update_layout(
    height=550,
    legend_title_text="장르"
)

st.plotly_chart(fig, use_container_width=True)

# 그래프 설명 영역
with st.container(border=True):
    st.markdown("### 💡 이 그래프로 알 수 있는 것")
    st.write("장르별로 영화가 몇 편씩 분포되어 있는지 한눈에 비교할 수 있다.")


# -----------------------------
# 데이터 표
# -----------------------------
st.divider()

st.subheader("📋 장르별 영화 편수")

genre_table = genre_count.copy()
genre_table["비율"] = (
    genre_table["count"] / genre_table["count"].sum() * 100
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
```python
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")

st.write(
    "1년간 박스오피스 10위권에 든 영화 가운데 "
    "이 기간에 개봉한 216편의 데이터를 살펴봅니다."
)

# -----------------------------
# 데이터 불러오기
# -----------------------------
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_movies.csv"
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 개봉일을 문자열로 처리
    df["openDt"] = df["openDt"].astype(str).str.zfill(8)

    # 장르가 여러 개라면 첫 번째 장르만 사용
    # 예: 액션|범죄 → 액션
    df["genre"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    # 총 관객 수를 숫자로 변환
    df["total_audi"] = pd.to_numeric(
        df["total_audi"],
        errors="coerce"
    ).fillna(0)

    # 영화명이 없는 경우 처리
    df["movieNm"] = (
        df["movieNm"]
        .fillna("영화명 없음")
        .astype(str)
    )

    return df


try:
    df = load_data()

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.error(f"오류 내용: {e}")
    st.stop()


# -----------------------------
# 데이터 요약
# -----------------------------
st.subheader("📋 데이터 요약")

col1, col2 = st.columns(2)

with col1:
    st.metric("전체 영화 수", f"{len(df):,}편")

with col2:
    st.metric("장르 수", f"{df['genre'].nunique():,}개")


# ============================================================
# 그래프 1
# ============================================================

st.divider()

st.header("📊 그래프 1. 장르별 영화 편수")

genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["genre", "count"]

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

# 그래프 1 설명
with st.container(border=True):
    st.markdown("### 💡 이 그래프로 알 수 있는 것")
    st.write(
        "장르별로 영화가 몇 편씩 분포되어 있는지 한눈에 비교할 수 있다."
    )


# ============================================================
# 그래프 2
# ============================================================

st.divider()

st.header("📊 그래프 2. 장르별 영화와 총 관객 트리맵")

st.write(
    "큰 네모일수록 총 관객 수가 많은 영화입니다. "
    "장르 안에서 영화별 관객 규모를 비교할 수 있습니다."
)

fig2 = px.treemap(
    df,
    path=["genre", "movieNm"],
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
    margin=dict(t=60, l=10, r=10, b=10)
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# 그래프 2 설명
with st.container(border=True):
    st.markdown("### 💡 이 그래프로 알 수 있는 것")
    st.write(
        "장르별로 어떤 영화가 많은 관객을 모았는지와 영화별 총 관객 규모의 차이를 알 수 있다."
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
```

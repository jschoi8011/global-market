import streamlit as st
import pandas as pd

# 1. 앱 설정 및 제목
st.set_page_config(page_title="James의 글로벌 경제 마켓", layout="wide")
st.title("🌎 James의 글로벌 경제 데이터 마켓")

# 2. 사이드바 - 환율 설정 (선생님 전용)
st.sidebar.header("⚙️ 실시간 환율 설정 (1원 기준)")
usd_rate = st.sidebar.number_input("🇺🇸 USD 환율 (1달러당 원)", value=1350)
jpy_rate = st.sidebar.number_input("🇯🇵 JPY 환율 (100엔당 원)", value=900) / 100
eur_rate = st.sidebar.number_input("🇪🇺 EUR 환율 (1유로당 원)", value=1450)
vnd_rate = st.sidebar.number_input("🇻🇳 VND 환율 (100동당 원)", value=5.5) / 100

# 매출 저장소 초기화
if 'sales' not in st.session_state:
    st.session_state.sales = {"서울": 0, "뉴욕": 0, "하노이": 0, "파리": 0, "도쿄": 0}

# 3. 도시별 탭 구성
tabs = st.tabs(["💰 환전소", "🇰🇷 서울", "🇺🇸 뉴욕", "🇻🇳 하노이", "🇫🇷 파리", "🇯🇵 도쿄", "📊 매출현황"])

# --- 탭 1: 환전소 ---
with tabs[0]:
    st.header("💵 원화를 외화로 환전하기")
    krw_amount = st.number_input("환전할 한국 돈(원)을 입력하세요", min_value=0, step=1000)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🇺🇸 달러", f"${krw_amount / usd_rate:.2f}")
    col2.metric("🇯🇵 엔화", f"¥{krw_amount / jpy_rate:.0f}")
    col3.metric("🇪🇺 유로", f"€{krw_amount / eur_rate:.2f}")
    col4.metric("🇻🇳 동", f"₫{krw_amount / vnd_rate:.0f}")

# --- 도시별 매장 함수 ---
def shop_interface(city, currency, rate, menu):
    st.header(f"📍 {city} 매장 (단위: {currency})")
    for item, price in menu.items():
        if st.button(f"{item} 구매 ({price}{currency})"):
            st.session_state.sales[city] += price * rate
            st.success(f"{item} 결제 완료! (약 {int(price * rate)}원)")

# --- 각 도시별 메뉴 설정 ---
seoul_menu = {"빅맥": 5500, "카페라떼": 5000, "생크림 카스텔라": 4500}
ny_menu = {"Big Mac": 5.8, "Caffe Latte": 5.25, "Cookie": 3.5}
hanoi_menu = {"Banh Mi": 45000, "Cafe Sua Da": 65000, "Big Mac": 74000}
paris_menu = {"Croissant": 3.5, "Cafe Latte": 4.9, "Big Mac": 5.4}
tokyo_menu = {"Teriyaki Burger": 480, "Caffe Latte": 490, "Matcha Latte": 550}

with tabs[1]: shop_interface("서울", "원", 1, seoul_menu)
with tabs[2]: shop_interface("뉴욕", "$", usd_rate, ny_menu)
with tabs[3]: shop_interface("하노이", "₫", vnd_rate, hanoi_menu)
with tabs[4]: shop_interface("파리", "€", eur_rate, paris_menu)
with tabs[5]: shop_interface("도쿄", "¥", jpy_rate, tokyo_menu)

# --- 탭 7: 매출 현황 ---
with tabs[6]:
    st.header("📈 도시별 총 매출 (한국 원화 환산)")
    df = pd.DataFrame(list(st.session_state.sales.items()), columns=['도시', '매출(원)'])
    st.bar_chart(df.set_index('도시'))
    st.table(df)

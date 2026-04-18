import streamlit as st
import pandas as pd

# 1. 앱 설정
st.set_page_config(page_title="James의 글로벌 가계부 마켓", layout="wide")
st.title("🌎 James의 글로벌 경제 데이터 마켓 & 가계부")

# 2. 사이드바 - 환율 설정 및 초기 자산 설정
st.sidebar.header("⚙️ 선생님용 설정")
usd_rate = st.sidebar.number_input("🇺🇸 USD 환율 (1달러당 원)", value=1350)
jpy_rate = st.sidebar.number_input("🇯🇵 JPY 환율 (100엔당 원)", value=900) / 100
eur_rate = st.sidebar.number_input("🇪🇺 EUR 환율 (1유로당 원)", value=1450)
vnd_rate = st.sidebar.number_input("🇻🇳 VND 환율 (100동당 원)", value=5.5) / 100

st.sidebar.markdown("---")
st.sidebar.header("💰 나의 지갑 설정")
if 'budget' not in st.session_state:
    st.session_state.budget = 100000  # 기본 자산 10만원
my_budget = st.sidebar.number_input("나의 시작 자산(원)", value=st.session_state.budget)
st.session_state.budget = my_budget

# 데이터 초기화
if 'total_spent' not in st.session_state:
    st.session_state.total_spent = 0
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. 상단 대시보드 (가계부 요약)
balance = st.session_state.budget - st.session_state.total_spent
col_b1, col_b2, col_b3 = st.columns(3)
col_b1.metric("💳 시작 자산", f"{st.session_state.budget:,}원")
col_b2.metric("💸 총 지출액", f"{st.session_state.total_spent:,}원", delta_color="inverse")
col_b3.metric("💰 남은 잔액", f"{balance:,}원")

# 4. 메뉴 통일 (맥도날드: 빅맥, 콜라 / 스타벅스: 라테, 쿠키)
# 각 나라별 현지 가격 설정 (예시 수치)
menus = {
    "서울": {"currency": "원", "rate": 1, "m_bigmac": 5500, "m_cola": 2000, "s_latte": 5000, "s_cookie": 4500},
    "뉴욕": {"currency": "$", "rate": usd_rate, "m_bigmac": 5.8, "m_cola": 2.5, "s_latte": 5.25, "s_cookie": 3.5},
    "하노이": {"currency": "₫", "rate": vnd_rate, "m_bigmac": 74000, "m_cola": 25000, "s_latte": 65000, "s_cookie": 45000},
    "파리": {"currency": "€", "rate": eur_rate, "m_bigmac": 5.4, "m_cola": 3.0, "s_latte": 4.9, "s_cookie": 4.0},
    "도쿄": {"currency": "¥", "rate": jpy_rate, "m_bigmac": 480, "m_cola": 200, "s_latte": 490, "s_cookie": 350}
}

tabs = st.tabs(["💰 환전소", "🇰🇷 서울", "🇺🇸 뉴욕", "🇻🇳 하노이", "🇫🇷 파리", "🇯🇵 도쿄", "📝 가계부 내역"])

# --- 탭별 기능 구현 ---
for i, city in enumerate(["서울", "뉴욕", "하노이", "파리", "도쿄"]):
    with tabs[i+1]:
        st.header(f"📍 {city} 매장")
        data = menus[city]
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🍔 맥도날드")
            if st.button(f"빅맥 ({data['m_bigmac']}{data['currency']})", key=f"bm_{city}"):
                cost_krw = int(data['m_bigmac'] * data['rate'])
                st.session_state.total_spent += cost_krw
                st.session_state.history.append({"장소": f"{city} 맥도날드", "항목": "빅맥", "현지가격": f"{data['m_bigmac']}{data['currency']}", "원화환산": cost_krw})
            if st.button(f"콜라 ({data['m_cola']}{data['currency']})", key=f"cl_{city}"):
                cost_krw = int(data['m_cola'] * data['rate'])
                st.session_state.total_spent += cost_krw
                st.session_state.history.append({"장소": f"{city} 맥도날드", "항목": "콜라", "현지가격": f"{data['m_cola']}{data['currency']}", "원화환산": cost_krw})
        
        with col2:
            st.subheader("☕ 스타벅스")
            if st.button(f"카페라테 ({data['s_latte']}{data['currency']})", key=f"lt_{city}"):
                cost_krw = int(data['s_latte'] * data['rate'])
                st.session_state.total_spent += cost_krw
                st.session_state.history.append({"장소": f"{city} 스타벅스", "항목": "카페라테", "현지가격": f"{data['s_latte']}{data['currency']}", "원화환산": cost_krw})
            if st.button(f"쿠키/케이크 ({data['s_cookie']}{data['currency']})", key=f"ck_{city}"):
                cost_krw = int(data['s_cookie'] * data['rate'])
                st.session_state.total_spent += cost_krw
                st.session_state.history.append({"장소": f"{city} 스타벅스", "항목": "쿠키/케이크", "현지가격": f"{data['s_cookie']}{data['currency']}", "원화환산": cost_krw})

# --- 가계부 내역 탭 ---
with tabs[6]:
    st.header("📝 나의 소비 이력")
    if st.session_state.history:
        history_df = pd.DataFrame(st.session_state.history)
        st.table(history_df)
        if st.button("내역 초기화"):
            st.session_state.total_spent = 0
            st.session_state.history = []
            st.rerun()
    else:
        st.write("아직 구매 내역이 없습니다.")

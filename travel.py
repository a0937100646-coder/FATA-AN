import streamlit as st
import random
from datetime import datetime, date

# ==========================================
# 1. 系統設定 (太魯閣專屬配置)
# ==========================================
st.set_page_config(
    page_title="太魯閣峽谷深度遊 | 壯麗秘境探索",
    page_icon="⛰️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS 美學 (大理石灰 x 峽谷深綠)
# ==========================================
st.markdown("""
    <style>
    /* 全站背景：象徵大理石的淺灰白色 */
    .stApp {
        background-color: #F8F9FA;
        font-family: "Microsoft JhengHei", sans-serif;
        color: #2C3E50 !important;
    }
    
    p, div, span, h1, h2, h3, h4, h5, h6, label, .stMarkdown {
        color: #2C3E50 !important;
    }

    /* 深色模式防禦：強制輸入框白底黑字 */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] {
        background-color: #ffffff !important; 
        border: 1px solid #AAB7B8 !important;
        color: #2C3E50 !important; 
    }
    input { color: #2C3E50 !important; }
    div[data-baseweb="select"] span { color: #2C3E50 !important; }
    ul[data-baseweb="menu"] { background-color: #ffffff !important; }
    li[data-baseweb="option"] { color: #2C3E50 !important; }
    svg { fill: #2C3E50 !important; color: #2C3E50 !important; }

    /* 日期選單高亮 (立霧溪青水綠) */
    div[data-testid="stDateInput"] > label {
        color: #117A65 !important; 
        font-size: 20px !important;
        font-weight: 900 !important;
        margin-bottom: 10px !important;
        display: block;
    }
    div[data-testid="stDateInput"] div[data-baseweb="input"] {
        border: 2px solid #1ABC9C !important; 
        background-color: #E8F8F5 !important;
        border-radius: 10px !important;
    }

    /* 隱藏官方元件 */
    header {visibility: hidden;}
    footer {display: none !important;}
    
    /* 標題區：峽谷深綠 到 大理石岩壁的漸層 */
    .header-box {
        background: linear-gradient(135deg, #145A32 0%, #5D6D7E 100%);
        padding: 35px 20px;
        border-radius: 0 0 30px 30px;
        color: white !important;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(20, 90, 50, 0.4);
        margin-top: -60px;
    }
    .header-box h1, .header-box div, .header-box span { color: white !important; }
    .header-title { font-size: 32px; font-weight: bold; letter-spacing: 3px; margin-bottom: 5px;}
    .header-subtitle { font-size: 15px; color: #D5DBDB !important; font-style: italic; }
    
    /* 卡片模組 */
    .section-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        border-top: 4px solid #1ABC9C;
        margin-bottom: 20px;
    }
    
    /* 轉換率按鈕 (峽谷大地橘) */
    .stButton>button {
        width: 100%;
        background-color: #D35400; 
        color: white !important;
        border-radius: 50px;
        border: none;
        padding: 12px 0;
        font-weight: bold;
        transition: 0.3s;
        font-size: 18px;
        box-shadow: 0 4px 6px rgba(211, 84, 0, 0.3);
    }
    .stButton>button:hover { background-color: #E67E22; transform: translateY(-2px); }
    
    /* 導覽時間軸 */
    .tour-item {
        border-left: 4px solid #7F8C8D;
        padding-left: 15px;
        margin-bottom: 18px;
        position: relative;
    }
    .tour-item::before {
        content: '⛰️';
        position: absolute;
        left: -15px;
        top: 0;
        background: #F8F9FA;
    }
    .tour-title { font-weight: bold; color: #145A32 !important; font-size: 19px; }
    .tour-tag { font-size: 12px; background: #EAEDED; color: #34495E !important; padding: 3px 10px; border-radius: 12px; margin-right: 6px; font-weight: bold;}
    
    /* 商品網格卡片 */
    .product-card {
        background: #FFFFFF;
        border: 1px solid #BDC3C7;
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 15px;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .product-card:hover { border-color: #1ABC9C; box-shadow: 0 8px 15px rgba(26,188,156,0.15); transform: translateY(-3px);}
    .product-price { font-size: 20px; color: #C0392B !important; font-weight: 900; margin: 8px 0; }
    .product-tag { font-size: 11px; background: #E8F8F5; color: #117A65 !important; padding: 3px 8px; border-radius: 8px; font-weight: bold;}
    .badge { position: absolute; top: 10px; right: -25px; background: #C0392B; color: white !important; font-size: 10px; font-weight: bold; padding: 3px 30px; transform: rotate(45deg); }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 核心資料庫 (太魯閣觀光資源：行程與在地特產)
# ==========================================
tours_db = [
    {"name": "砂卡礑步道生態漫遊", "type": "輕鬆健行", "duration": "2小時", "fee": "$450", "desc": "沿著清澈的湛藍溪水漫步，步道平緩好走，適合全家大小一同觀察豐富的附生植物與昆蟲生態。"},
    {"name": "錐麓古道絕壁挑戰", "type": "極限探險", "duration": "5小時", "fee": "$1,200", "desc": "走在海拔700公尺、寬僅90公分的斷崖上，俯瞰太魯閣峽谷的壯麗。需事前申請入山證，挑戰自我首選。"},
    {"name": "燕子口與九曲洞峽谷奇觀", "type": "經典必遊", "duration": "3小時", "fee": "$600", "desc": "搭乘專車搭配徒步，由專業解說員帶領深入欣賞大理岩峽谷最精華的壺穴地形與斷層奇景。"},
    {"name": "白楊步道水濂洞探秘", "type": "深度體驗", "duration": "3.5小時", "fee": "$800", "desc": "穿過多個隧道，感受獨特的水濂洞天然水柱 SPA，並欣賞壯闊的白楊瀑布與吊橋風光。"}
]

products_db = [
    {"name": "天然玫瑰石手工項鍊", "category": "在地工藝", "price": 1280, "icon": "💎", "desc": "嚴選花蓮特產玫瑰石，每一塊都有獨特的天然山水紋理，純手工打磨鑲嵌。", "hot": True},
    {"name": "太魯閣族傳統圖騰編織包", "category": "文化創生", "price": 850, "icon": "🎒", "desc": "由部落婦女手工編織，使用傳統苧麻材質與祖靈之眼圖騰，兼具文化傳承與實用性。", "hot": False},
    {"name": "花蓮蜜香紅茶禮盒", "category": "在地好味", "price": 600, "icon": "🍵", "desc": "經小綠葉蟬叮咬後產生天然蜜香，無毒農法栽種，茶湯溫潤回甘。", "hot": True},
    {"name": "馬告風味剝皮辣椒", "category": "在地好味", "price": 250, "icon": "🌶️", "desc": "融合原住民特有香料「馬告」（山胡椒），微辣中帶有獨特的檸檬香茅氣息。", "hot": False},
    {"name": "大理石紋高質感杯墊組", "category": "在地工藝", "price": 499, "icon": "🪨", "desc": "利用太魯閣邊角大理岩材製作，質地冰涼吸水性佳，將峽谷的記憶留在桌面上。", "hot": True},
    {"name": "山林舒緩馬告精油", "category": "舒壓香氛", "price": 980, "icon": "🌿", "desc": "萃取高山馬告精華，適合健行後按摩舒緩肌肉疲勞，帶給您森林般的清新感受。", "hot": False}
]

# ==========================================
# 4. 邏輯核心：精準推薦系統
# ==========================================
def recommend_tours(group):
    if group == "親子家庭 (帶小孩/長輩)":
        return [t for t in tours_db if t['name'] in ["砂卡礑步道生態漫遊", "燕子口與九曲洞峽谷奇觀"]]
    elif group == "戶外極限玩家":
        return [t for t in tours_db if t['name'] in ["錐麓古道絕壁挑戰", "白楊步道水濂洞探秘"]]
    elif group == "情侶約會/攝影愛好":
        return [t for t in tours_db if t['name'] in ["燕子口與九曲洞峽谷奇觀", "白楊步道水濂洞探秘"]]
    else: # 一人慢遊 或 其他
        return tours_db[:3]

# ==========================================
# 5. 頁面內容
# ==========================================
st.markdown("""
    <div class="header-box">
        <div class="header-title">⛰️ 太魯閣峽谷深度遊</div>
        <div class="header-subtitle">鬼斧神工的大自然傑作 • 您的專屬峽谷嚮導</div>
    </div>
""", unsafe_allow_html=True)

# --- 區塊 1：導覽預約模組 ---
st.markdown("### 🗺️ 規劃您的峽谷探險")
with st.container():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        visit_date = st.date_input("📅 預計入山日期", value=date.today())
    with col2:
        group = st.selectbox("👥 您的同行旅伴", ["情侶約會/攝影愛好", "親子家庭 (帶小孩/長輩)", "戶外極限玩家", "一人慢遊"])
    
    if st.button("🔍 尋找適合的秘境路線"):
        st.session_state['show_tours'] = True
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.get('show_tours'):
    st.markdown(f"**為「{group}」推薦的專屬行程：**")
    recs = recommend_tours(group)
    for tour in recs:
        st.markdown(f"""
        <div class="tour-item">
            <div class="tour-title">{tour['name']}</div>
            <div style="margin: 6px 0;">
                <span class="tour-tag">⏱️ {tour['duration']}</span>
                <span class="tour-tag">💰 {tour['fee']}/人</span>
                <span class="tour-tag" style="background:#E8F8F5; color:#117A65!important;">{tour['type']}</span>
            </div>
            <div style="font-size: 14px; color: #555; line-height: 1.5;">{tour['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

# --- 區塊 2：太魯閣伴手禮市集 ---
st.markdown("---")
st.markdown("### 🛍️ 太魯閣紀念品市集")
st.markdown("<p style='font-size:14px; color:#7F8C8D;'>將大自然的鬼斧神工與原民部落的溫暖手作帶回家。</p>", unsafe_allow_html=True)

category_filter = st.radio("商品分類", ["全部", "🪨 在地工藝/文化", "🍽️ 嚴選在地好味", "🌿 舒壓香氛"], horizontal=True)

filtered_products = products_db
if category_filter == "🪨 在地工藝/文化":
    filtered_products = [p for p in products_db if p['category'] in ["在地工藝", "文化創生"]]
elif category_filter == "🍽️ 嚴選在地好味":
    filtered_products = [p for p in products_db if p['category'] == "在地好味"]
elif category_filter == "🌿 舒壓香氛":
    filtered_products = [p for p in products_db if p['category'] == "舒壓香氛"]

cols = st.columns(2)
for i, product in enumerate(filtered_products):
    with cols[i % 2]:
        badge_html = '<div class="badge">熱銷</div>' if product.get('hot') else ''
        st.markdown(f"""
        <div class="product-card">
            {badge_html}<div style="font-size: 35px; margin-bottom:10px;">{product['icon']}</div>
            <span class="product-tag">{product['category']}</span>
            <div style="font-weight: 900; color: #2C3E50; margin-top: 10px; font-size:16px;">{product['name']}</div>
            <div class="product-price">NT$ {product['price']}</div>
            <div style="font-size: 13px; color: #757575; margin-top: 8px; line-height:1.4;">{product['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

# --- 頁尾：導引購買與聯絡 ---
st.markdown("""
<div style="text-align:center; margin-top:40px; padding:25px; background: linear-gradient(180deg, #F8F9FA 0%, #EAEDED 100%); border-radius:15px; border: 1px solid #BDC3C7;">
    <h4 style="color:#145A32 !important; font-weight:bold; margin-bottom:10px;">預約行程 / 購買紀念品</h4>
    <p style="font-size:14px; color:#5D6D7E; margin-bottom:25px;">部分古道需提前申請入園證，歡迎直接聯繫專屬嚮導為您代辦與規劃。</p>
    <a href="https://lin.ee/您的專屬網址" target="_blank" style="text-decoration: none; display: inline-block; background-color:#00C300; color:white; border:none; padding:12px 30px; border-radius:50px; font-weight:900; font-size: 16px; box-shadow: 0 4px 10px rgba(0, 195, 0, 0.3); cursor:pointer;">💬 加入官方 LINE 預約</a>
</div>
""", unsafe_allow_html=True)

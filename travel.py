import streamlit as st
import random
from datetime import datetime, date

# ==========================================
# 1. 系統設定
# ==========================================
st.set_page_config(
    page_title="2026 馬太鞍部落深度旅遊指南",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS 美學 (大地綠/竹林系 - 兼具 iPhone 深色模式修復)
# ==========================================
st.markdown("""
    <style>
    /* 1. 強制全站背景為淺大地色，字體為深色 */
    .stApp {
        background-color: #F4F9F4;
        font-family: "Microsoft JhengHei", sans-serif;
        color: #2F4F4F !important;
    }
    
    /* 2. 強制所有一般文字元素為深色 */
    p, div, span, h1, h2, h3, h4, h5, h6, label, .stMarkdown {
        color: #2F4F4F !important;
    }

    /* === 3. 核心修復：強制輸入框與選單在深色模式下維持「白底黑字」 === */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
        border: 1px solid #A9DFBF !important;
        color: #2F4F4F !important;
    }
    input { color: #2F4F4F !important; }
    div[data-baseweb="select"] span { color: #2F4F4F !important; }
    ul[data-baseweb="menu"] { background-color: #ffffff !important; }
    li[data-baseweb="option"] { color: #2F4F4F !important; }
    svg { fill: #2F4F4F !important; color: #2F4F4F !important; }

    /* === 4. 特別加強：日期選單高亮 (馬太鞍專屬綠色) === */
    div[data-testid="stDateInput"] > label {
        color: #1E8449 !important; 
        font-size: 24px !important; 
        font-weight: 900 !important;
        text-shadow: 0px 0px 5px rgba(46, 204, 113, 0.5);
        margin-bottom: 10px !important;
        display: block;
    }
    div[data-testid="stDateInput"] div[data-baseweb="input"] {
        border: 3px solid #27AE60 !important;
        background-color: #EAFAF1 !important;
        border-radius: 10px !important;
        box-shadow: 0 0 15px rgba(39, 174, 96, 0.2); 
    }

    /* 隱藏官方元件 */
    header {visibility: hidden;}
    footer {display: none !important;}
    
    /* 標題區 (阿美族竹林/濕地漸層) */
    .header-box {
        background: linear-gradient(135deg, #2E8B57 0%, #81C784 100%);
        padding: 30px 20px;
        border-radius: 0 0 30px 30px;
        color: white !important;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(46, 139, 87, 0.4);
        margin-top: -60px;
    }
    .header-box h1, .header-box div, .header-box span { color: white !important; }
    .header-title { font-size: 28px; font-weight: bold; text-shadow: 1px 1px 3px rgba(0,0,0,0.3); }
    
    /* 輸入卡片 */
    .input-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border: 1px solid #D5F5E3;
        margin-bottom: 20px;
    }
    
    /* 按鈕 */
    .stButton>button {
        width: 100%;
        background-color: #27AE60;
        color: white !important;
        border-radius: 50px;
        border: none;
        padding: 12px 0;
        font-weight: bold;
        transition: 0.3s;
        font-size: 18px;
    }
    .stButton>button:hover { background-color: #1E8449; }
    
    /* 資訊看板 */
    .info-box {
        background-color: #FEF9E7;
        border-left: 5px solid #F1C40F;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    
    /* 時間軸 */
    .timeline-item {
        border-left: 3px solid #2ECC71;
        padding-left: 20px;
        margin-bottom: 20px;
        position: relative;
    }
    .timeline-item::before {
        content: '🐟';
        position: absolute;
        left: -13px;
        top: 0;
        background: #F4F9F4;
        border-radius: 50%;
    }
    .day-header {
        background: #E8F8F5;
        color: #0E6655 !important;
        padding: 5px 15px;
        border-radius: 15px;
        display: inline-block;
        margin-bottom: 15px;
        font-weight: bold;
    }
    .spot-title { font-weight: bold; color: #117864 !important; font-size: 18px; }
    .spot-tag { 
        font-size: 12px; background: #D5F5E3; color: #196F3D !important; 
        padding: 2px 8px; border-radius: 10px; margin-right: 5px;
    }
    
    /* 住宿卡片 */
    .hotel-card {
        background: #FAFAFA;
        border-left: 5px solid #D35400;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .hotel-tag {
        font-size: 11px; background: #E67E22; color: white !important;
        padding: 2px 6px; border-radius: 8px; margin-right: 5px;
    }
    
    /* 景點名錄小卡 */
    .mini-card {
        background: white; padding: 10px; border-radius: 8px; border: 1px solid #eee;
        font-size: 14px; margin-bottom: 8px; border-left: 3px solid #27AE60;
    }
    .theme-badge {
        background: #27AE60; color: white !important; padding: 1px 5px; border-radius: 4px; font-size: 11px; margin-left: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 核心資料庫 (馬太鞍與光復周邊)
# ==========================================
all_spots_db = [
    # --- 【核心區】馬太鞍部落體驗 ---
    {"name": "馬太鞍濕地生態園區", "region": "核心", "theme": "生態", "type": "自然", "fee": "免門票", "desc": "花蓮面積最大的生態濕地，湧泉不絕，可觀察多樣水生植物與鳥類。"},
    {"name": "欣綠農園", "region": "核心", "theme": "美食/體驗", "type": "特色", "fee": "依體驗計費", "desc": "必體驗「Palakaw (巴拉告)」阿美族傳統捕魚法，以及震撼視覺的「石頭火鍋 (石煮鍋)」。"},
    {"name": "拉藍的家民宿與文史", "region": "核心", "theme": "文化", "type": "導覽", "fee": "需預約", "desc": "深入了解阿美族母系社會文化、聽頭目的故事，體驗搗麻糬與木雕。"},
    {"name": "紅瓦屋老地方文化餐廳", "region": "核心", "theme": "美食", "type": "餐廳", "fee": "單點/合菜", "desc": "以原住民藝術木雕裝潢，招牌菜包含鹽烤魚、野菜拼盤與在地風味餐。"},
    {"name": "瑪布隆農場", "region": "核心", "theme": "農事", "type": "體驗", "fee": "預約制", "desc": "推廣部落保種運動，可體驗採摘特有種黑豆，品嚐在地黑豆茶與農事體驗。"},
    {"name": "芙登溪木棧道", "region": "核心", "theme": "生態", "type": "散步", "fee": "免門票", "desc": "沿著清澈的芙登溪漫步，夏季可見滿池荷花與睡蓮綻放。"},

    # --- 【周邊區】光復鄉延伸景點 ---
    {"name": "花蓮光復糖廠 (漪漣園)", "region": "周邊", "theme": "休閒", "type": "打卡", "fee": "免門票", "desc": "吃傳統冰棒與冰淇淋，餵食池塘裡的錦鯉，感受濃厚的日式建築風情。"},
    {"name": "大農大富平地森林園區", "region": "周邊", "theme": "自然", "type": "單車", "fee": "免門票", "desc": "全國首座平地森林，秋季賞楓，3-4月有全台最早的螢火蟲季。"},
    {"name": "吉利潭", "region": "周邊", "theme": "秘境", "type": "景觀", "fee": "免門票", "desc": "昔日阿美族人祈雨與洗浴的聖地，現為群山環繞的靜謐湖泊秘境。"},
    {"name": "太巴塱部落", "region": "周邊", "theme": "文化", "type": "導覽", "fee": "預約制", "desc": "與馬太鞍齊名的大部落，擁有獨特的紅嘴黑鵯傳說與傳統阿美族祖祠。"},
]

hotels_db = [
    {"name": "光復糖廠日式木屋", "region": "周邊", "tag": "日式風情", "price": 3500, "desc": "全台唯一全日式百年檜木聚落，附贈腳踏車券。"},
    {"name": "欣綠農園石頭屋民宿", "region": "核心", "tag": "深度體驗", "price": 2800, "desc": "住在濕地中央，夜晚伴隨蛙鳴入睡。"},
    {"name": "拉藍的家", "region": "核心", "tag": "文化交流", "price": 2000, "desc": "體驗阿美族家庭的熱情，適合背包客與深度旅人。"},
    {"name": "綠野森林民宿", "region": "周邊", "tag": "鄉村風", "price": 2500, "desc": "鄰近大農大富，環境清幽。"},
    {"name": "麵包樹舍", "region": "周邊", "tag": "手作早餐", "price": 3200, "desc": "光復鄉知名高評價民宿，充滿溫馨感。"}
]

# ==========================================
# 4. 邏輯核心：動態行程生成演算法
# ==========================================
def generate_dynamic_itinerary(travel_date, days_str, group):
    m = travel_date.month
    
    core_spots = [s for s in all_spots_db if s['region'] == "核心"]
    surround_spots = [s for s in all_spots_db if s['region'] == "周邊"]
    
    if "一日" in days_str: day_count = 1
    elif "二日" in days_str: day_count = 2
    else: day_count = 3
    
    itinerary = {}
    
    # --- Day 1: 馬太鞍核心深度體驗 ---
    d1_spot1 = next(s for s in core_spots if s['name'] == "馬太鞍濕地生態園區")
    d1_spot2 = next(s for s in core_spots if s['name'] == "欣綠農園") # 午餐與 Palakaw
    d1_spot3 = next(s for s in core_spots if s['name'] == "拉藍的家民宿與文史") 
    
    if group == "親子家庭":
        d1_spot3 = next(s for s in core_spots if s['name'] == "瑪布隆農場") # 換成農事體驗
        
    itinerary[1] = [d1_spot1, d1_spot2, d1_spot3][:2] # 取兩個時段
    
    # --- Day 2: 延伸周邊與糖廠 ---
    if day_count >= 2:
        d2_spot1 = next(s for s in surround_spots if s['name'] == "大農大富平地森林園區")
        d2_spot2 = next(s for s in surround_spots if s['name'] == "花蓮光復糖廠 (漪漣園)")
        itinerary[2] = [d2_spot1, d2_spot2]

    # --- Day 3: 秘境與太巴塱雙部落 ---
    if day_count == 3:
        d3_spot1 = next(s for s in surround_spots if s['name'] == "吉利潭")
        d3_spot2 = next(s for s in surround_spots if s['name'] == "太巴塱部落")
        itinerary[3] = [d3_spot1, d3_spot2]

    # 季節特色標題
    if m in [3, 4]: status_title = "✨ 春季限定：螢火蟲與濕地綠意"
    elif m in [7, 8]: status_title = "🌾 豐年祭 (Ilisin) 熱血祭典季"
    elif m in [5, 6]: status_title = "🪷 芙登溪荷花與湧泉避暑"
    else: status_title = "🌿 阿美族生態智慧深度漫遊"
    
    return status_title, itinerary

# ==========================================
# 5. 頁面內容
# ==========================================
st.markdown("""
    <div class="header-box">
        <div class="header-title">🌿 2026 馬太鞍部落觀光指南</div>
        <div class="header-subtitle">Nga'ay ho！探索 Fataan 生態與阿美族文化</div>
    </div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        travel_date = st.date_input("📅 抵達日期 (必填)", value=date(2026, 7, 15))
    with col2:
        days_str = st.selectbox("🕒 停留天數", ["一日遊 (深度探索)", "二日遊 (部落住一晚)", "三日遊 (光復全境)"])
        group = st.selectbox("👥 旅客類型", ["情侶/夫妻", "親子家庭", "長輩同行", "熱血獨旅"])
    
    if st.button("🚀 生成部落專屬行程"):
        st.session_state['generated'] = True
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.get('generated'):
    status_title, itinerary = generate_dynamic_itinerary(travel_date, days_str, group)
    
    st.markdown(f"""
    <div class="info-box">
        <h4>{status_title}</h4>
        <p>為您規劃 <b>{travel_date.strftime('%Y/%m/%d')}</b> 展開的 <b>{group}</b> 永續生態之旅！</p>
    </div>
    """, unsafe_allow_html=True)

    # --- 顯示行程 ---
    for day, spots in itinerary.items():
        st.markdown(f'<div class="day-header">Day {day}</div>', unsafe_allow_html=True)
        
        for i, spot in enumerate(spots):
            time_label = "☀️ 上午" if i == 0 else "🌤️ 下午"
            
            # 標籤生成
            tags_html = f'<span class="spot-tag">{spot["type"]}</span>'
            tags_html += f'<span class="spot-tag">{spot["theme"]}</span>'
            if spot['region'] == "核心": 
                tags_html += '<span class="spot-tag" style="background:#FAD7A1;color:#A04000!important;">馬太鞍境內</span>'
            
            st.markdown(f"""
            <div class="timeline-item">
                <div class="spot-title">{time_label}：{spot['name']}</div>
                <div style="margin: 5px 0;">{tags_html}</div>
                <div style="font-size: 14px; color: #555;">
                    💰 {spot['fee']} <br>
                    📝 {spot['desc']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- 住宿推薦 ---
    if "一日" not in days_str:
        st.markdown("### 🛖 部落與周邊推薦住宿")
        
        # 隨機秀 3 間
        for h in random.sample(hotels_db, min(3, len(hotels_db))):
            st.markdown(f"""
            <div class="hotel-card">
                <div style="font-weight:bold; color:#B9770E;">{h['name']} <span class="hotel-tag">{h['tag']}</span></div>
                <div style="font-size:13px; color:#666; margin-top:3px;">
                    💲 {h['price']}起 | {h['desc']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- 頁尾景點總覽 ---
with st.expander("📖 查看馬太鞍與光復鄉景點名錄"):
    st.markdown("#### 部落與周邊探索地圖")
    for region in ["核心", "周邊"]:
        st.markdown(f"**【{region}區】**")
        region_spots = [s for s in all_spots_db if s['region'] == region]
        cols = st.columns(2)
        for i, s in enumerate(region_spots):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="mini-card">
                    <b>{s['name']}</b> <span class="theme-badge">{s['theme']}</span><br>
                    <span style="color:#888; font-size:12px;">{s['desc']}</span>
                </div>
                """, unsafe_allow_html=True)

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 設置頁面配置
st.set_page_config(
    page_title="熱門話題搜尋器",
    page_icon="🔍",
    layout="wide"
)

# 初始化 session state
if 'search_results' not in st.session_state:
    st.session_state.search_results = None

# 定義常數
COUNTRIES = ["台灣", "美國", "日本", "韓國"]
CATEGORIES = ["全部", "政治", "娛樂", "體育", "科技", "財經"]
TIME_RANGES = {
    "過去24小時": 1,
    "過去一週": 7,
    "過去一個月": 30,
    "過去三個月": 90,
    "過去一年": 365
}

# 標題和說明
st.title("🔍 熱門話題搜尋器")
st.markdown("根據您的選擇，搜尋並顯示最熱門的新聞與文章")

# 創建搜尋區域
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        # 搜尋條件選擇
        selected_country = st.selectbox("選擇國家", COUNTRIES)
        selected_category = st.selectbox("選擇領域", CATEGORIES)
        
    with col2:
        # 時間範圍和關鍵字
        selected_time = st.selectbox("選擇時間範圍", list(TIME_RANGES.keys()))
        keywords = st.text_input("輸入關鍵字", placeholder="請輸入搜尋關鍵字")

# 按鈕區域
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    search_button = st.button("搜尋", type="primary", use_container_width=True)
with col2:
    reset_button = st.button("重置", type="secondary", use_container_width=True)

# 預定義的關鍵字對應表
KEYWORD_MAPPING = {
    "AI": ["人工智慧", "機器學習", "深度學習", "神經網路", "自然語言處理", 
           "電腦視覺", "機器人", "自動化", "演算法", "大數據"],
    "科技": ["創新", "數位轉型", "物聯網", "雲端運算", "區塊鏈",
            "5G", "資訊安全", "軟體開發", "硬體設備", "智慧城市"],
    "教育": ["線上學習", "遠距教學", "教育科技", "課程設計", "學習平台",
            "教學方法", "教育資源", "學習成效", "教師培訓", "教育創新"],
    # 可以繼續添加更多關鍵字對應
}

def generate_related_keywords(keyword):
    """使用預定義的對應表生成相關關鍵字"""
    # 將輸入轉換為小寫以進行比對
    keyword_lower = keyword.lower()
    
    # 在預定義表中查找
    for key, values in KEYWORD_MAPPING.items():
        if keyword_lower in key.lower():
            return values
    
    # 如果找不到完全匹配，返回部分匹配的關鍵字
    for key, values in KEYWORD_MAPPING.items():
        if keyword_lower in key.lower() or any(keyword_lower in v.lower() for v in values):
            return values
    
    # 如果完全找不到相關的，返回一些通用的關鍵字
    return [
        f"{keyword}趨勢",
        f"{keyword}發展",
        f"{keyword}應用",
        f"{keyword}新聞",
        f"{keyword}分析",
        f"{keyword}報導",
        f"{keyword}評論",
        f"{keyword}研究",
        f"{keyword}創新",
        f"{keyword}未來"
    ]

# 修改搜尋函數
def search_articles(country, category, time_range, keywords):
    # 生成相關關鍵字
    with st.expander("相關關鍵字分析", expanded=True):
        related_keywords = generate_related_keywords(keywords)
        
        # 顯示相關關鍵字
        st.write("### 相關關鍵字")
        keywords_cols = st.columns(2)
        for i, keyword in enumerate(related_keywords):
            col_index = i % 2
            with keywords_cols[col_index]:
                st.write(f"- {keyword}")
        
        # 將原始關鍵字和相關關鍵字合併
        all_keywords = [keywords] + related_keywords
        st.write("---")
    
    # 這裡之後會替換成實際的搜尋 API 調用
    # 現在用假資料示範，但加入相關關鍵字的使用
    dummy_data = {
        "標題": [
            f"{kw} 相關新聞 {i}" 
            for kw in all_keywords[:3]  # 使用部分關鍵字作為示例
            for i in range(1, 8)  # 每個關鍵字生成7筆資料
        ],
        "來源": ["新聞網站" for _ in range(21)],  # 3 * 7 = 21
        "發布時間": [
            (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d %H:%M")
            for i in range(21)
        ],
        "瀏覽數": [1000 - i * 30 for i in range(21)],
        "網址": ["https://example.com" for _ in range(21)],
        "摘要": [
            f"這是一篇包含「{kw}」的新聞摘要..." 
            for kw in all_keywords[:3]
            for _ in range(7)
        ],
        "關鍵字匹配": [
            kw 
            for kw in all_keywords[:3]
            for _ in range(7)
        ]
    }
    
    df = pd.DataFrame(dummy_data)
    # 根據瀏覽數排序
    return df.sort_values('瀏覽數', ascending=False)

# 處理搜尋
if search_button and keywords:
    with st.spinner("搜尋中..."):
        # 執行搜尋
        st.session_state.search_results = search_articles(
            selected_country,
            selected_category,
            TIME_RANGES[selected_time],
            keywords
        )

# 重置搜尋
if reset_button:
    st.session_state.search_results = None
    st.rerun()

# 顯示搜尋結果
if st.session_state.search_results is not None:
    st.markdown("### 搜尋結果")
    st.markdown(f"共找到 {len(st.session_state.search_results)} 筆結果")
    
    # 顯示每個搜尋結果
    for _, row in st.session_state.search_results.iterrows():
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"#### [{row['標題']}]({row['網址']})")
                st.markdown(row['摘要'])
                st.markdown(f"來源: {row['來源']} | 發布時間: {row['發布時間']} | 匹配關鍵字: {row['關鍵字匹配']}")
            with col2:
                st.metric("瀏覽數", f"{row['瀏覽數']:,}")
            st.divider() 
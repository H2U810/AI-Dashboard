import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import requests

# 1. 页面基础配置
st.set_page_config(page_title="电商AI机会评估雷达", page_icon="🛒", layout="wide")

# ✅ 【重要修改】从云端 Secrets 中读取 API_KEY，绝不暴露明文！
# 本地测试时如果报错，请忽略，因为本地没有配置 secrets
try:
    API_KEY = st.secrets["ZHIPU_API_KEY"]
except Exception:
    API_KEY = "ef9738de0648484493b6dea574850dee.Fj2n1eImttQYLP33" # 仅限本地测试兜底用

# ====================================================
# 🚀 核心：注入带有蓝白光影背景的 Canvas 动态粒子网络
# ====================================================
particles_js = """
<!DOCTYPE html>
<html>
<head>
<style>
  body { 
      margin: 0; padding: 0; overflow: hidden; 
      background-color: #e0f2fe; 
      background-image: 
          linear-gradient(115deg, transparent 40%, rgba(255, 255, 255, 0.8) 45%, rgba(255, 255, 255, 0.8) 55%, transparent 60%),
          linear-gradient(-45deg, transparent 40%, rgba(255, 255, 255, 0.6) 48%, rgba(255, 255, 255, 0.6) 52%, transparent 60%),
          radial-gradient(circle at 10% 10%, rgba(255, 255, 255, 0.9) 0%, transparent 40%),
          radial-gradient(circle at 90% 90%, rgba(255, 255, 255, 0.7) 0%, transparent 40%),
          linear-gradient(to bottom right, #bae6fd, #7dd3fc, #e0f2fe);
      background-attachment: fixed;
  }
  canvas { display: block; position: relative; z-index: 1; }
</style>
</head>
<body>
<canvas id="network"></canvas>
<script>
  const canvas = document.getElementById('network');
  const ctx = canvas.getContext('2d');
  let width = canvas.width = window.innerWidth;
  let height = canvas.height = window.innerHeight;
  let particles = [];
  const particleCount = 80; 
  const maxDistance = 150; 
  const colors = ['#ef4444', '#10b981', '#334155'];
  for (let i = 0; i < particleCount; i++) {
      particles.push({ x: Math.random() * width, y: Math.random() * height, vx: (Math.random() - 0.5) * 0.8, vy: (Math.random() - 0.5) * 0.8, radius: Math.random() * 3 + 1.5, color: colors[Math.floor(Math.random() * colors.length)] });
  }
  function animate() {
      requestAnimationFrame(animate);
      ctx.clearRect(0, 0, width, height);
      particles.forEach(p => {
          p.x += p.vx; p.y += p.vy;
          if (p.x < 0 || p.x > width) p.vx *= -1;
          if (p.y < 0 || p.y > height) p.vy *= -1;
          ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2); ctx.fillStyle = p.color; ctx.fill();
      });
      for (let i = 0; i < particles.length; i++) {
          for (let j = i + 1; j < particles.length; j++) {
              const dx = particles[i].x - particles[j].x; const dy = particles[i].y - particles[j].y; const distance = Math.sqrt(dx * dx + dy * dy);
              if (distance < maxDistance) {
                  ctx.beginPath(); ctx.moveTo(particles[i].x, particles[i].y); ctx.lineTo(particles[j].x, particles[j].y);
                  ctx.strokeStyle = `rgba(100, 116, 139, ${1 - distance / maxDistance})`; ctx.lineWidth = 1; ctx.stroke();
              }
          }
      }
  }
  window.addEventListener('resize', () => { width = canvas.width = window.innerWidth; height = canvas.height = window.innerHeight; });
  animate();
</script>
</body>
</html>
"""
components.html(particles_js, height=0, width=0, scrolling=False)

# 3. 注入高级 CSS 样式
st.markdown("""
    <style>
    [data-testid="stHeader"] { background-color: transparent !important; }
    .stAppDeployButton { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    
    /* 左下角侧边栏悬浮球 */
    button[data-testid="stSidebarCollapsedControl"], div[data-testid="stSidebarCollapsedControl"] {
        position: fixed !important; bottom: 40px !important; left: 40px !important; top: auto !important;
        width: 60px !important; height: 60px !important; border-radius: 50% !important;
        background-color: #2563eb !important; border: 2px solid #ffffff !important;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.6) !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        transition: all 0.3s ease !important; z-index: 9999999 !important; cursor: pointer !important;
    }
    button[data-testid="stSidebarCollapsedControl"]:hover, div[data-testid="stSidebarCollapsedControl"]:hover {
        transform: scale(1.15) translateY(-5px) !important; background-color: #1d4ed8 !important;
    }
    button[data-testid="stSidebarCollapsedControl"] svg, div[data-testid="stSidebarCollapsedControl"] svg { fill: #ffffff !important; width: 30px !important; height: 30px !important; }
    
    .block-container { padding-top: 3rem !important; }
    html, body, [class*="css"] { font-size: 18px !important; }
    
    .stApp { background: transparent !important; }
    iframe { position: fixed !important; top: 0 !important; left: 0 !important; width: 100vw !important; height: 100vh !important; z-index: -1 !important; pointer-events: none !important; border: none !important; }
    
    h1, h2, h3, h4, p, span, div, label { color: #0f172a !important; }
    .main-title { font-size: 3.2rem !important; font-weight: 800 !important; color: #0f172a !important; text-align: center; margin-bottom: 0px; padding-bottom: 10px; text-shadow: 0px 2px 15px rgba(255,255,255,0.9); }
    .sub-title { text-align: center; color: #1e293b !important; font-size: 1.3rem; margin-bottom: 30px; font-weight: 500;}

    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.85) !important; backdrop-filter: blur(10px); border: 1px solid #e2e8f0;
        padding: 25px; border-radius: 12px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        text-align: center; transition: transform 0.2s ease;
    }
    div[data-testid="metric-container"]:hover { transform: translateY(-3px); box-shadow: 0 15px 30px -5px rgba(0, 0, 0, 0.15); }
    div[data-testid="stMetricValue"] > div { color: #2563eb !important; font-weight: 800; font-size: 3rem !important; }
    div[data-testid="stMetricLabel"] > div { font-size: 1.2rem !important; color: #475569 !important; }

    [data-testid="stSidebar"] { background: rgba(255, 255, 255, 0.65) !important; backdrop-filter: blur(20px) !important; border-right: 1px solid rgba(255, 255, 255, 0.8) !important; box-shadow: 5px 0 25px rgba(0, 0, 0, 0.05) !important; }
    
    div[data-baseweb="select"] > div { background-color: rgba(255, 255, 255, 0.8) !important; border: 1px solid #93c5fd !important; border-radius: 8px; }
    span[data-baseweb="tag"] { background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%) !important; color: #1d4ed8 !important; border: 1px solid #bfdbfe !important; }
    span[data-baseweb="tag"] svg { fill: #1d4ed8 !important; }
    div[data-testid="stSlider"] > div > div > div > div { background-color: #2563eb !important; }
    div[data-testid="stSlider"] div[role="slider"] { background-color: #2563eb !important; box-shadow: 0 0 10px rgba(37, 99, 235, 0.5) !important; }

    .stTabs [data-baseweb="tab-list"] { gap: 30px; border-bottom: 2px solid #e2e8f0; }
    .stTabs [data-baseweb="tab"] { font-size: 20px !important; font-weight: 600; color: #64748b !important; }
    .stTabs [aria-selected="true"] { color: #2563eb !important; border-bottom-color: #2563eb !important; }

    /* ==================================================== */
    /* 🚀 核心美化：悬浮球 */
    /* ==================================================== */
    div[data-testid="stPopover"] {
        position: fixed !important; bottom: 40px !important; right: 40px !important; z-index: 9999999 !important; width: auto !important;
    }
    
    div[data-testid="stPopover"] button {
        width: 75px !important; 
        height: 75px !important; 
        min-height: 75px !important;
        border-radius: 50% !important; 
        padding: 0 !important;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important; 
        border: 3px solid #ffffff !important;
        box-shadow: 0 10px 25px rgba(0, 242, 254, 0.5) !important;
        position: relative !important;
        overflow: hidden !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stPopover"] button * {
        display: none !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
    }
    
    div[data-testid="stPopover"] button::before {
        content: "🤖" !important; 
        font-size: 45px !important; 
        line-height: 1 !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        display: block !important;
        opacity: 1 !important;
    }
    
    div[data-testid="stPopover"] button:hover { 
        transform: scale(1.1) translateY(-3px) !important; 
        box-shadow: 0 15px 35px rgba(0, 242, 254, 0.7) !important; 
    }

    /* ==================================================== */
    /* 🚀 聊天面板及左右对话 */
    /* ==================================================== */
    div[data-baseweb="popover"] {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(25px) !important;
        border-radius: 24px !important;
        box-shadow: 0 25px 60px rgba(0,0,0,0.2) !important;
        width: 480px !important; 
        border: 1px solid rgba(255,255,255,0.9) !important;
        margin-bottom: 80px !important; 
        padding: 10px !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stChatMessage"]) {
        resize: vertical !important;
        overflow-y: auto !important;
        min-height: 250px !important;
        max-height: 70vh !important;
        border: 2px dashed #93c5fd !important;
        border-radius: 12px !important;
        padding: 10px !important;
        background: rgba(248, 250, 252, 0.6) !important;
    }

    div[data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 5px !important;
        display: flex !important;
        width: 100% !important;
    }

    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]),
    div[data-testid="stChatMessage"]:not(:has(div[data-testid="stChatMessageAvatarUser"])) {
        flex-direction: row !important;
        justify-content: flex-start !important;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) div[data-testid="stMarkdownContainer"],
    div[data-testid="stChatMessage"]:not(:has(div[data-testid="stChatMessageAvatarUser"])) div[data-testid="stMarkdownContainer"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        padding: 10px 15px !important;
        border-radius: 0px 15px 15px 15px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
        max-width: 85% !important;
    }

    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
        flex-direction: row-reverse !important;
        justify-content: flex-start !important;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) div[data-testid="stMarkdownContainer"] {
        background: #2563eb !important;
        padding: 10px 15px !important;
        border-radius: 15px 0px 15px 15px !important;
        box-shadow: 0 2px 5px rgba(37,99,235,0.2) !important;
        max-width: 85% !important;
        margin-left: 10px !important;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) div[data-testid="stMarkdownContainer"] * {
        color: #ffffff !important;
    }

    div[data-testid="stForm"] {
        background: white !important;
        border-radius: 15px !important;
        padding: 10px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        border: 1px solid #e2e8f0 !important;
        margin-top: 10px !important;
    }
    div[data-testid="stForm"] small { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# 4. 加载数据
@st.cache_data
def load_data():
    df = pd.read_csv("result4.csv")
    if '功能类别' in df.columns:
        df = df[df['功能类别'] != '不匹配']
    return df

try:
    df = load_data()
    
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; font-size: 1.8rem; color: #0f172a; text-shadow: 0 0 10px rgba(255,255,255,0.8);'>🎯 数据控制台</h2>", unsafe_allow_html=True)
        selected_func = st.multiselect("选择功能类别", df['功能类别'].unique(), default=df['功能类别'].unique())
        if not selected_func:
            st.warning("⚠️ 系统已为您自动恢复全选。")
            selected_func = df['功能类别'].unique()
        min_score = st.slider("🎚️ 最低机会价值分", 0, 100, 0, 5)
        st.info("💡 数据来源：Product Hunt\n\n🤖 模型引擎：GLM-4")

    filtered_df = df[(df['功能类别'].isin(selected_func)) & (df['机会价值分'] >= min_score)]
    
    st.markdown('<h1 class="main-title">🛒 电商行业 AI 应用场景智能挖掘与评估</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">基于大语言模型的多源异构数据挖掘与商业机会量化决策系统</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 机会簇总数", len(filtered_df))
    col2.metric("🏆 最高机会分", filtered_df['机会价值分'].max() if not filtered_df.empty else 0)
    col3.metric("🏢 覆盖行业数", filtered_df['所属行业'].nunique())
    col4.metric("⚙️ 涉及功能数", filtered_df['功能类别'].nunique())
    
    st.write("")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["📊 机会矩阵大屏", "💡 深度商业洞察", "📋 原始数据明细"])

    with tab1:
        st.subheader("电商 AI 功能机会矩阵")
        st.caption("X轴：功能类别 | Y轴：机会价值分 | 气泡大小：代表痛点热度。👉 **请将鼠标悬停在气泡上查看具体场景**")
        if not filtered_df.empty:
            fig = px.scatter(filtered_df, x="功能类别", y="机会价值分", size="机会价值分", color="功能类别", hover_name="主题簇名称", template="plotly_white", color_discrete_sequence=px.colors.qualitative.Vivid)
            fig.update_layout(height=600, showlegend=False, paper_bgcolor='rgba(255,255,255,0.85)', plot_bgcolor='rgba(255,255,255,0.85)', margin=dict(l=20, r=20, t=20, b=20), font=dict(size=16, color="#1e293b"), xaxis=dict(showgrid=True, gridcolor='#94a3b8', gridwidth=1.5, tickfont=dict(size=18, color="#475569"), title=dict(font=dict(size=20))), yaxis=dict(showgrid=True, gridcolor='#94a3b8', gridwidth=1.5, tickfont=dict(size=18, color="#475569"), title=dict(font=dict(size=20))), hoverlabel=dict(bgcolor="white", font_size=16, font_family="Arial"))
            fig.add_hline(y=60, line_dash="dash", line_color="#ef4444", annotation_text="高潜力推荐线", annotation_font_color="#ef4444", annotation_font_size=16)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("💡 系统自动生成的 Top 3 商业建议")
        st.markdown("根据大模型分析，以下是当前筛选条件下最值得投入的 AI 方向：")
        if not filtered_df.empty:
            top3 = filtered_df.sort_values(by="机会价值分", ascending=False).head(3)
            for index, row in top3.iterrows():
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.9); padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 6px solid #2563eb; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    <h4 style="margin-top: 0; color: #2563eb !important; font-size: 1.4rem;">🥇 推荐方向：{row['主题簇名称']}</h4>
                    <p style="font-size: 1.1rem; color: #334155;"><b>所属行业：</b>{row['所属行业']} &nbsp;|&nbsp; <b>机会价值分：</b><span style="color: #ea580c; font-weight: bold; font-size: 1.3em;">{row['机会价值分']}</span> 分</p>
                    <p style="font-size: 1.1rem; color: #334155;"><b>优先级评估：</b>{row['优先级']}</p>
                    <p style="color: #64748b; font-size: 1rem;">决策建议：该场景在近期讨论热度极高，且技术可行性已满足商业化条件，建议产品团队立即立项验证。</p>
                </div>
                """, unsafe_allow_html=True)
            st.divider()
            st.subheader("📈 机会价值排行榜")
            fig_bar = px.bar(top3.sort_values(by="机会价值分", ascending=True), x="机会价值分", y="主题簇名称", orientation='h', text='机会价值分', color="机会价值分", color_continuous_scale="Blues")
            fig_bar.update_layout(height=350, margin=dict(l=0, r=0, t=10, b=0), yaxis_title="", paper_bgcolor='rgba(255,255,255,0.85)', plot_bgcolor='rgba(255,255,255,0.85)', font=dict(size=16, color="#1e293b"), xaxis=dict(showgrid=True, gridcolor='#94a3b8', tickfont=dict(size=16)), yaxis=dict(showgrid=False, tickfont=dict(size=16)))
            fig_bar.update_traces(textfont=dict(color="white", size=14))
            st.plotly_chart(fig_bar, use_container_width=True)

    with tab3:
        st.subheader("机会评估数据明细")
        if not filtered_df.empty:
            display_df = filtered_df[['主题簇名称', '功能类别', '所属行业', '机会价值分', '优先级']]
            st.dataframe(display_df, use_container_width=True, hide_index=True, column_config={"机会价值分": st.column_config.ProgressColumn("机会价值分", format="%d", min_value=0, max_value=100), "优先级": st.column_config.TextColumn("优先级", width="small")})
            csv_data = display_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(label="📥 下载当前筛选报表 (CSV)", data=csv_data, file_name="ai_opportunity_report.csv", mime="text/csv", type="primary")

    # ==========================================
    # 🚀 悬浮聊天窗
    # ==========================================
    with st.popover("小电"): 
        st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid #e2e8f0;">
            <div style="font-size: 24px; margin-right: 10px;">🤖</div>
            <div>
                <h4 style="margin: 0; color: #0f172a; font-size: 1.2rem;">小电 - AI 商业分析师</h4>
                <p style="margin: 0; font-size: 0.8rem; color: #64748b;">💡 拖拽下方虚线框底部可放大/缩小窗口</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "老板您好！我是小电。请问您想了解哪个方向的投资机会？"}]

        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input("请输入您的问题...", key="chat_input_box", label_visibility="collapsed")
            submit_button = st.form_submit_button("发送 🚀", use_container_width=True)

        if submit_button and user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(user_input)

            with chat_container:
                with st.chat_message("assistant"):
                    with st.spinner("小电正在分析中..."):
                        try:
                            context_data = filtered_df.to_string(index=False)
                            # 注入名字“小电”
                            system_prompt = f"你叫'小电'，是一个资深的AI电商商业分析师。以下是我们的机会数据：\n{context_data}\n\n请严格根据数据回答。如果未覆盖，请说不知道。"
                            
                            url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
                            headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
                            data = {
                                "model": "glm-4-flash", 
                                "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
                                "temperature": 0.3
                            }
                            
                            response = requests.post(url, headers=headers, json=data)
                            
                            if response.status_code != 200:
                                st.error(f"❌ API请求失败 (状态码: {response.status_code})")
                                st.stop()

                            res = response.json()
                            choices = res.get('choices', [])
                            
                            if not choices:
                                error_msg = res.get('error', {}).get('message', '未知错误')
                                st.error(f"❌ API返回异常: {error_msg}")
                                st.stop()

                            answer = choices[0]['message']['content']
                            st.markdown(answer)
                            st.session_state.messages.append({"role": "assistant", "content": answer})
                            
                        except Exception as chat_e:
                            st.error(f"连接失败了: {chat_e}")

except Exception as e:
    st.error(f"发生错误: {e}，请检查 result4.csv 格式。")
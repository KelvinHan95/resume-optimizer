#Streamlit 命令脚本变网页
import streamlit as st
import requests

#API_KEY = "sk-394f7c1ada594438a59f2716e440b727"
API_KEY = st.secrets["DEEPSEEK_API_KEY"]  #streamlit 加密api写法

SYSTEM_PROMPT = """你是一位资深简历优化专家，帮用户把简历改写得更专业。
规则：
1. 把模糊描述改成量化成果
2. 每条经历用强动词开头（主导、搭建、推动、优化）
3. 输出两部分：先给优化后的简历，空一行，再给3条改进建议
4. 不要编造经历"""

st.title("简历优化器")          #创建标题

resume = st.text_area("请粘贴你的简历内容", height=200)     #创建输入框和提示内容

if st.button("开始优化"):            #创建按钮
    if not resume:
        st.warning("先粘贴简历内容再点击按钮")   #错误提示
    else:
        with st.spinner("AI 正在优化中..."):
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"帮我优化以下简历： \n{resume}"}
            ]
            response = requests.post(
                "https://api.deepseek.com/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json = {
                    "model": "deepseek-flash",
                    "messages": messages,
                    "stream": False
                }
            )
            result = response.json()
            optimized = result["choices"][0]["message"]["content"]
            st.subheader("优化结果")
            st.write(optimized)

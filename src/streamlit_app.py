import streamlit as st
import json
from datetime import datetime
from hybrid_wealth_advisor_langgraph import (
    run_wealth_advisor,
    SAMPLE_CUSTOMER_PROFILES
)

# 初始化session state
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# 页面配置
st.set_page_config(
    page_title="财富管理投顾AI助手",
    page_icon="💰",
    layout="centered"
)

st.title("💰 财富管理投顾AI助手")

# 客户选择
st.subheader("👤 选择客户类型")
customer_options = {
    "平衡型投资者 (Customer 1)": "customer1",
    "进取型投资者 (Customer 2)": "customer2"
}
selected_customer_label = st.selectbox(
    "选择客户类型",
    options=list(customer_options.keys()),
    index=0
)
customer_id = customer_options[selected_customer_label]

# 显示客户基本信息
customer_info = SAMPLE_CUSTOMER_PROFILES[customer_id]
st.json({
    "风险承受能力": customer_info["risk_tolerance"],
    "投资期限": customer_info["investment_horizon"],
    "财务目标": customer_info["financial_goals"]
})

# 用户输入
st.subheader("❓ 输入您的投资问题")
user_input = st.text_area(
    "请输入您的投资咨询问题:",
    value=st.session_state.user_input,
    height=120,
    placeholder="""例如：
- 今天上证指数的表现如何？
- 我的投资组合中股票占比是多少？
- 根据当前市场情况，我应该如何调整投资组合？"""
)

# 更新session state中的用户输入
st.session_state.user_input = user_input

# 提交按钮
if st.button("提交咨询", type="primary"):
    if user_input.strip():
        with st.spinner("AI助手正在分析您的问题..."):
            try:
                result = run_wealth_advisor(user_input, customer_id)
                
                # 显示结果
                st.subheader("🤖 AI助手回应")
                
                # 显示处理模式
                process_mode = result.get("processing_mode", "未知")
                if process_mode == "reactive":
                    mode_text = "【反应式】- 快速响应"
                else:
                    mode_text = "【深思熟虑】- 深度分析"
                st.caption(f"{mode_text}")
                
                # 显示回答
                final_response = result.get("final_response", "未生成响应")
                st.success(final_response)
                
            except Exception as e:
                st.error(f"处理过程中出现错误: {str(e)}")
    else:
        st.warning("请输入您的问题")

# 示例问题
st.subheader("💡 示例问题")
examples = [
    "今天上证指数的表现如何？",
    "我的投资组合中股票占比是多少？",
    "根据当前市场情况，我应该如何调整投资组合？",
    "请评估我当前的投资策略并提供优化建议。"
]

for i, example in enumerate(examples):
    if st.button(f"• {example}", key=f"example_btn_{i}"):
        st.session_state.user_input = example
        st.rerun()
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict

from src.hybrid_wealth_advisor_langgraph import (
    run_wealth_advisor,
    SAMPLE_CUSTOMER_PROFILES,
)

app = FastAPI(
    title="混合式智能投研顾问 Agent API",
    description="基于 LangGraph 的混合式财富管理投顾 AI 服务",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    query: str = Field(..., description="用户提问")
    customer_id: str = Field("customer1", description="客户画像ID，可选 customer1 / customer2")


class ChatResponse(BaseModel):
    query: str
    customer_id: str
    processing_mode: Optional[str] = None
    query_type: Optional[str] = None
    final_response: str
    market_data: Optional[Dict[str, Any]] = None
    analysis_results: Optional[Dict[str, Any]] = None


@app.get("/")
def root():
    return {
        "message": "混合式智能投研顾问 Agent API 运行中",
        "docs": "/docs",
        "available_customers": list(SAMPLE_CUSTOMER_PROFILES.keys())
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if req.customer_id not in SAMPLE_CUSTOMER_PROFILES:
        raise HTTPException(
            status_code=400,
            detail=f"无效的 customer_id: {req.customer_id}，可选值为 {list(SAMPLE_CUSTOMER_PROFILES.keys())}"
        )

    try:
        result = run_wealth_advisor(
            user_query=req.query,
            customer_id=req.customer_id
        )

        return ChatResponse(
            query=req.query,
            customer_id=req.customer_id,
            processing_mode=result.get("processing_mode"),
            query_type=result.get("query_type"),
            final_response=result.get("final_response", "未生成响应"),
            market_data=result.get("market_data"),
            analysis_results=result.get("analysis_results"),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务执行失败: {str(e)}")
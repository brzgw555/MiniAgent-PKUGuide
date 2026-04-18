from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
import random
usr_id=["1001","1002","1003","1004","1005","1006","1007","1008","1009","1010"]

rag = RagSummarizeService()

@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str)->str:
    return rag.rag_summarize(query)


@tool(description="获取用户ID,以纯字符串形式返回")
def get_user_id()->str:
    return random.choice(usr_id)

@tool(description="无入参,无返回值,调用后触发中间件自动为报告生成的场景动态注入上下文信息,为后续提示词切换提供上下文信息")
def fill_context_for_report():
    return None



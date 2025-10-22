"""
초간단 MCP 서버 - 테스트용
"""
from fastmcp import FastMCP

# MCP 서버 생성
mcp = FastMCP("Test Server")

@mcp.tool()
def hello(name: str) -> str:
    """인사하기"""
    return f"안녕하세요, {name}님!"

if __name__ == "__main__":
    mcp.run()

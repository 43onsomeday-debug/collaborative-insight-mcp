"""
MCP 서버 직접 테스트
"""
import sys
import os

print("=" * 60)
print("MCP Server Test")
print("=" * 60)

# 1. Python 버전 확인
print(f"\nPython: {sys.version}")
print(f"Python 경로: {sys.executable}")

# 2. FastMCP 확인
try:
    import fastmcp
    print(f"FastMCP: {fastmcp.__version__}")
except ImportError as e:
    print(f"FastMCP 오류: {e}")
    sys.exit(1)

# 3. 모듈 import 테스트
try:
    print("\n모듈 import 테스트:")
    from models import WorkflowState, RequestType
    print("  - models.py: OK")
    
    from phases.phase0 import RequestAnalyzer
    print("  - phases.phase0: OK")
    
    from phases.phase1 import ExpertAssigner
    print("  - phases.phase1: OK")
    
    from phases.phase4 import DesignGenerator
    print("  - phases.phase4: OK")
    
    from llm_integration import LLMClient
    print("  - llm_integration: OK")
    
except ImportError as e:
    print(f"  - Import 오류: {e}")
    sys.exit(1)

# 4. MCP 서버 초기화 테스트
try:
    print("\nMCP 서버 초기화 테스트:")
    from fastmcp import FastMCP
    
    mcp = FastMCP("Collaborative Insight Framework")
    print("  - MCP 서버 생성: OK")
    
    # 간단한 도구 등록 테스트
    @mcp.tool()
    def test_tool(message: str) -> str:
        """테스트 도구"""
        return f"Echo: {message}"
    
    print("  - 도구 등록: OK")
    
except Exception as e:
    print(f"  - MCP 초기화 오류: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("[SUCCESS] 모든 테스트 통과!")
print("=" * 60)
print("\nMCP 서버가 정상적으로 작동할 수 있습니다.")
print("Claude Desktop에서 인식되지 않는다면:")
print("1. Claude Desktop 완전 재시작 (작업 관리자 확인)")
print("2. 설정 파일 경로 재확인")
print("3. Claude Desktop 로그 확인")

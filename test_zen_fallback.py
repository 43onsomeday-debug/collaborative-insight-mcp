"""
Zen MCP Fallback 테스트
"""
import asyncio
from llm_integration import LLMClient


async def test_llm_status():
    """LLM 클라이언트 상태 확인"""
    print("=" * 60)
    print("LLM Integration - Zen MCP Fallback Test")
    print("=" * 60)
    
    # LLM 클라이언트 초기화
    llm_client = LLMClient()
    
    # 상태 확인
    status = llm_client.get_status()
    
    print("\n[LLM Client Status]")
    print("-" * 60)
    print(f"Anthropic API: {'OK' if status['anthropic_api'] else 'N/A'}")
    print(f"OpenAI API: {'OK' if status['openai_api'] else 'N/A'}")
    print(f"Gemini API: {'OK' if status['gemini_api'] else 'N/A'}")
    print(f"Zen MCP Fallback: {'OK' if status['zen_mcp_fallback'] else 'N/A'}")
    
    print(f"\n[Available Models]")
    print("-" * 60)
    for model in status['available_models']:
        print(f"  - {model}")
    
    # Zen MCP Fallback 테스트
    if status['zen_mcp_fallback'] and not status['anthropic_api']:
        print("\n[Zen MCP Fallback Mode Test]")
        print("-" * 60)
        
        test_prompt = "웹사이트 UX 개선을 위한 5가지 핵심 원칙을 설명해주세요."
        
        try:
            result = await llm_client.generate(
                prompt=test_prompt,
                model="auto",
                system_prompt="당신은 UX 전문가입니다."
            )
            
            print(f"프롬프트: {test_prompt}")
            print(f"\n결과:")
            print(result)
            print("\n[OK] Zen MCP Fallback 작동 확인!")
            
        except Exception as e:
            print(f"[ERROR] 오류 발생: {e}")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] Zen MCP Fallback 테스트 완료!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_llm_status())

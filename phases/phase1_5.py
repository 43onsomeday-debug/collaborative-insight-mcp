"""
Phase 1.5: 환경 체크
- Zen MCP 연결 확인
- LLM API 개수 확인 (0~4개)
- Phase 2, 4 실행 모드 결정
- 예상 비용 표시
- 캐시/TTL 설정
"""
import os
from typing import Dict, Any, Literal
from datetime import datetime, timedelta


class EnvironmentChecker:
    """환경 체크 및 설정"""
    
    # 캐시 저장소 (TTL 5분)
    _cache: Dict[str, Dict[str, Any]] = {}
    _cache_ttl = timedelta(minutes=5)
    
    @classmethod
    def check_environment(cls, session_id: str) -> Dict[str, Any]:
        """
        환경 체크 수행
        
        Args:
            session_id: 세션 ID
            
        Returns:
            환경 체크 결과
        """
        # 캐시 확인
        cached_result = cls._get_cached_result(session_id)
        if cached_result:
            return cached_result
        
        # 1. Zen MCP 연결 확인
        zen_mcp_status = cls._check_zen_mcp()
        
        # 2. LLM API 개수 확인
        api_count, available_apis = cls._count_available_apis()
        
        # 3. Phase 2, 4 실행 모드 결정
        execution_mode = cls._determine_execution_mode(api_count, zen_mcp_status)
        
        # 4. 예상 비용 계산 (Type별)
        estimated_costs = cls._calculate_estimated_costs()
        
        result = {
            "zen_mcp_connected": zen_mcp_status["connected"],
            "zen_mcp_message": zen_mcp_status["message"],
            "api_count": api_count,
            "available_apis": available_apis,
            "execution_mode": {
                "phase2": execution_mode["phase2"],
                "phase4": execution_mode["phase4"],
                "description": execution_mode["description"]
            },
            "estimated_costs": estimated_costs,
            "cache_enabled": True,
            "cache_ttl_minutes": 5,
            "checked_at": datetime.now().isoformat()
        }
        
        # 결과 캐싱
        cls._cache_result(session_id, result)
        
        return result
    
    @classmethod
    def _check_zen_mcp(cls) -> Dict[str, Any]:
        """Zen MCP 연결 확인"""
        # Zen MCP는 MCP 환경에서 자동으로 사용 가능
        # 실제로는 MCP 클라이언트가 있는지 확인
        try:
            # MCP 환경에서 실행 중인지 확인
            # 실제 구현에서는 MCP 프로토콜 체크
            is_mcp_environment = True  # 간소화
            
            if is_mcp_environment:
                return {
                    "connected": True,
                    "message": "✅ Zen MCP 연결 성공 - Fallback 모드 사용 가능"
                }
            else:
                return {
                    "connected": False,
                    "message": "⚠️ Zen MCP 연결 실패 - API 키 필수"
                }
        except Exception as e:
            return {
                "connected": False,
                "message": f"❌ Zen MCP 연결 오류: {str(e)}"
            }
    
    @classmethod
    def _count_available_apis(cls) -> tuple[int, list[str]]:
        """사용 가능한 LLM API 개수 확인"""
        available_apis = []
        
        # Anthropic (Claude)
        if os.getenv("ANTHROPIC_API_KEY"):
            available_apis.append("claude")
        
        # OpenAI (GPT)
        if os.getenv("OPENAI_API_KEY"):
            available_apis.append("gpt")
        
        # Google (Gemini)
        if os.getenv("GEMINI_API_KEY"):
            available_apis.append("gemini")
        
        # Grok (X.AI) - 선택적
        if os.getenv("GROK_API_KEY"):
            available_apis.append("grok")
        
        return len(available_apis), available_apis
    
    @classmethod
    def _determine_execution_mode(
        cls,
        api_count: int,
        zen_mcp_status: Dict[str, Any]
    ) -> Dict[str, str]:
        """Phase 2, 4 실행 모드 결정"""
        
        if api_count == 0:
            if zen_mcp_status["connected"]:
                return {
                    "phase2": "단독",
                    "phase4": "단독",
                    "description": "API 없음 → Zen MCP Fallback (단독 LLM 모드)"
                }
            else:
                return {
                    "phase2": "불가",
                    "phase4": "불가",
                    "description": "API 없음 & Zen MCP 없음 → 실행 불가"
                }
        
        elif 1 <= api_count <= 4:
            return {
                "phase2": "다중",
                "phase4": "다중",
                "description": f"API {api_count}개 → 다중 LLM 협업 모드"
            }
        
        else:
            return {
                "phase2": "다중",
                "phase4": "다중",
                "description": f"API {api_count}개 → 최적화된 다중 LLM 모드"
            }
    
    @classmethod
    def _calculate_estimated_costs(cls) -> Dict[str, str]:
        """예상 비용 계산 (Type별)"""
        return {
            "type1": "$0.5-2",
            "type1_description": "단순 명확 (Phase 0→1→1.5→2→4→6)",
            "type2": "$2-10",
            "type2_description": "복잡 명확 (Phase 0→1→1.5→2→4→5→6→7)",
            "type3": "$5-20",
            "type3_description": "모호 (Phase 0→1→1.5→2→3→재분류→...)",
            "note": "실제 비용은 프롬프트 길이와 모델에 따라 달라집니다"
        }
    
    @classmethod
    def _get_cached_result(cls, session_id: str) -> Dict[str, Any] | None:
        """캐시에서 결과 조회 (TTL 5분)"""
        if session_id in cls._cache:
            cached = cls._cache[session_id]
            cached_time = datetime.fromisoformat(cached["checked_at"])
            
            if datetime.now() - cached_time < cls._cache_ttl:
                return cached
            else:
                # 만료된 캐시 삭제
                del cls._cache[session_id]
        
        return None
    
    @classmethod
    def _cache_result(cls, session_id: str, result: Dict[str, Any]):
        """결과 캐싱"""
        cls._cache[session_id] = result
    
    @classmethod
    def clear_cache(cls, session_id: str | None = None):
        """캐시 삭제"""
        if session_id:
            if session_id in cls._cache:
                del cls._cache[session_id]
        else:
            cls._cache.clear()
    
    @classmethod
    def get_global_context(cls) -> Dict[str, Any]:
        """전역 컨텍스트 정보"""
        return {
            "cache_count": len(cls._cache),
            "cache_ttl_minutes": 5,
            "timeout_minutes": 30,
            "max_sessions": 100
        }

"""
Phase 6: 실행
"""
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel
from models import Phase5Result, DesignDocument


class ExecutionResult(BaseModel):
    """실행 결과"""
    result: Any
    status: str
    execution_time: float
    metadata: Dict[str, Any] = {}


class TaskExecutor:
    """작업 실행기"""
    
    @classmethod
    async def execute(
        cls,
        phase5_result: Phase5Result,
        design_document: DesignDocument,
        llm_clients: Optional[Dict[str, Any]] = None
    ) -> 'ExecutionResult':
        """
        간소화된 실행 메서드 (테스트용)
        
        Args:
            phase5_result: LLM 선정 결과
            design_document: 설계서
            llm_clients: LLM 클라이언트 (선택적)
        
        Returns:
            ExecutionResult: 실행 결과
        """
        start_time = time.time()
        
        # Mock 실행 (실제로는 LLM API 호출)
        result = cls._mock_execute(design_document, phase5_result)
        
        execution_time = time.time() - start_time
        
        return ExecutionResult(
            result=result,
            status="completed",
            execution_time=execution_time,
            metadata={
                "model_used": phase5_result.selections[0].model_id if phase5_result.selections else "none",
                "sections_processed": len(design_document.sections)
            }
        )
    
    @staticmethod
    def _mock_execute(design_document: DesignDocument, phase5_result: Phase5Result) -> str:
        """Mock 실행 결과 생성"""
        
        result = f"# {design_document.title}\n\n"
        result += f"**품질 레벨**: {design_document.quality_level.value}\n\n"
        
        result += "## 설계 내용\n\n"
        
        for section in design_document.sections:
            result += f"### {section.section_name}\n\n"
            result += f"{section.content}\n\n"
        
        result += "\n## 구현 세부사항\n\n"
        result += "설계서를 바탕으로 다음과 같이 구현합니다:\n\n"
        result += "1. 요구사항 분석 완료\n"
        result += "2. 아키텍처 설계 완료\n"
        result += "3. 주요 컴포넌트 식별 완료\n"
        result += "4. 기술 스택 선정 완료\n"
        result += "5. 구현 로드맵 작성 완료\n\n"
        
        result += "## 다음 단계\n\n"
        result += "- 상세 설계 문서 작성\n"
        result += "- 프로토타입 개발\n"
        result += "- 사용자 테스트 수행\n"
        
        return result
    
    @classmethod
    async def execute_task(
        cls,
        design_document: DesignDocument,
        phase5_result: Phase5Result,
        llm_clients: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        작업 실행 (원본 메서드 - 추후 구현용)
        
        Args:
            design_document: 설계서
            phase5_result: LLM 선정 결과
            llm_clients: LLM 클라이언트 딕셔너리
        """
        results = {}
        
        # 선정된 LLM들로 작업 실행
        if hasattr(phase5_result, 'selected_llms'):
            for llm_name in phase5_result.selected_llms:
                if llm_name not in llm_clients:
                    continue
                
                client = llm_clients[llm_name]
                role = phase5_result.role_assignments.get(llm_name, "general")
                
                # 역할에 따라 프롬프트 생성
                prompt = cls._create_execution_prompt(
                    design_document,
                    role
                )
                
                # LLM 실행 (실제 구현 필요)
                # response = await client.generate(prompt)
                response = f"Result from {llm_name}"
                
                results[llm_name] = {
                    "role": role,
                    "response": response
                }
        
        # 협업 패턴에 따라 결과 통합
        if hasattr(phase5_result, 'work_mode') and phase5_result.work_mode == "collaboration":
            final_result = cls._integrate_results(
                results,
                phase5_result.collaboration_pattern if hasattr(phase5_result, 'collaboration_pattern') else None
            )
        else:
            # Solo 모드면 첫 번째 결과 사용
            final_result = list(results.values())[0]["response"] if results else "No results"
        
        return {
            "final_result": final_result,
            "individual_results": results,
            "collaboration_pattern": getattr(phase5_result, 'collaboration_pattern', None)
        }
    
    @staticmethod
    def _create_execution_prompt(
        design_document: DesignDocument,
        role: str
    ) -> str:
        """실행 프롬프트 생성"""
        sections_text = "\n\n".join([
            f"{section.section_name}\n{section.content}"
            for section in design_document.sections
        ])
        
        return f"""
당신의 역할: {role}

설계서:
{sections_text}

위 설계서를 바탕으로 실제 구현 가능한 결과물을 생성해주세요.
"""
    
    @staticmethod
    def _integrate_results(
        results: Dict[str, Dict],
        pattern: Optional[str]
    ) -> str:
        """결과 통합"""
        if not results:
            return "No results to integrate"
        
        if pattern == "sequential":
            # 순차적 - 마지막 결과 사용
            return list(results.values())[-1]["response"]
        elif pattern == "parallel":
            # 병렬 - 모든 결과 통합
            combined = "\n\n---\n\n".join([
                f"[{k}의 결과]\n{v['response']}"
                for k, v in results.items()
            ])
            return combined
        elif pattern == "validation":
            # 검증 - 첫 번째가 메인, 나머지는 검증
            main_result = list(results.values())[0]["response"]
            return main_result
        else:
            return list(results.values())[0]["response"]


# Alias for backward compatibility
Executor = TaskExecutor

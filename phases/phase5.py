"""
Phase 5: LLM 선정
"""
from typing import List, Dict, Any, Optional
from models import (
    LLMSelection, ModelCapability, SelectionReason,
    Phase5Result, Phase4Result
)


class LLMSelector:
    """LLM 모델 선정 및 프롬프트 최적화"""
    
    # 사용 가능한 LLM 목록
    AVAILABLE_MODELS = {
        "claude-3-5-sonnet-20241022": {
            "provider": "anthropic",
            "strengths": ["reasoning", "code", "analysis", "long_context"],
            "context_window": 200000,
            "cost_tier": "high",
            "best_for": ["복잡한 추론", "코드 생성", "긴 문서 분석"]
        },
        "gpt-4-turbo": {
            "provider": "openai",
            "strengths": ["creative", "general", "multimodal"],
            "context_window": 128000,
            "cost_tier": "high",
            "best_for": ["창의적 작업", "일반 대화", "이미지 분석"]
        },
        "gpt-3.5-turbo": {
            "provider": "openai",
            "strengths": ["speed", "general"],
            "context_window": 16000,
            "cost_tier": "low",
            "best_for": ["빠른 응답", "간단한 작업"]
        },
        "gemini-1.5-pro": {
            "provider": "google",
            "strengths": ["multimodal", "long_context", "reasoning"],
            "context_window": 1000000,
            "cost_tier": "medium",
            "best_for": ["매우 긴 문서", "멀티모달", "복잡한 추론"]
        }
    }
    
    @staticmethod
    def select_models(
        design_document: Any,  # DesignDocument
        complexity_score: float,
        context: Optional[Dict[str, Any]] = None
    ) -> Phase5Result:
        """
        작업에 적합한 LLM 선정
        
        Args:
            design_document: Phase 4의 설계서
            complexity_score: 복잡도 점수
            context: 추가 컨텍스트
        
        Returns:
            Phase5Result: LLM 선정 결과
        """
        
        # 1. 작업 특성 분석
        task_characteristics = LLMSelector._analyze_task(
            design_document,
            complexity_score
        )
        
        # 2. 모델 후보 평가
        candidates = LLMSelector._evaluate_candidates(task_characteristics)
        
        # 3. 최종 선정
        selections = LLMSelector._make_selections(candidates, task_characteristics)
        
        # 4. 프롬프트 최적화
        optimized_prompts = LLMSelector._optimize_prompts(
            selections,
            design_document
        )
        
        return Phase5Result(
            selections=selections,
            optimized_prompts=optimized_prompts,
            metadata={
                "task_characteristics": task_characteristics,
                "model_count": len(selections)
            }
        )
    
    @staticmethod
    def _analyze_task(
        design_document: Any,
        complexity_score: float
    ) -> Dict[str, Any]:
        """작업 특성 분석"""
        
        characteristics = {
            "complexity": complexity_score,
            "requires_reasoning": complexity_score > 5,
            "requires_code": False,
            "requires_creativity": False,
            "requires_long_context": False,
            "budget_constraint": "medium"
        }
        
        # 설계서 내용 분석
        if hasattr(design_document, 'sections'):
            for section in design_document.sections:
                content = section.content.lower()
                
                if any(word in content for word in ['코드', 'code', '개발', '구현']):
                    characteristics["requires_code"] = True
                
                if any(word in content for word in ['창의', 'creative', '디자인']):
                    characteristics["requires_creativity"] = True
                
                if len(design_document.sections) > 5:
                    characteristics["requires_long_context"] = True
        
        return characteristics
    
    @staticmethod
    def _evaluate_candidates(
        characteristics: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """모델 후보 평가"""
        
        candidates = []
        
        for model_name, model_info in LLMSelector.AVAILABLE_MODELS.items():
            score = 0
            reasons = []
            
            # 복잡도 평가
            if characteristics["complexity"] > 5:
                if "reasoning" in model_info["strengths"]:
                    score += 3
                    reasons.append("강력한 추론 능력")
            
            # 코드 요구사항
            if characteristics["requires_code"]:
                if "code" in model_info["strengths"]:
                    score += 3
                    reasons.append("코드 생성에 특화")
            
            # 창의성 요구사항
            if characteristics["requires_creativity"]:
                if "creative" in model_info["strengths"]:
                    score += 2
                    reasons.append("창의적 작업에 적합")
            
            # 긴 컨텍스트
            if characteristics["requires_long_context"]:
                if "long_context" in model_info["strengths"]:
                    score += 2
                    reasons.append("긴 문서 처리 가능")
            
            # 비용 고려
            budget = characteristics.get("budget_constraint", "medium")
            if budget == "low" and model_info["cost_tier"] == "low":
                score += 1
                reasons.append("비용 효율적")
            elif budget == "high" and model_info["cost_tier"] == "high":
                score += 1
            
            candidates.append({
                "model_name": model_name,
                "score": score,
                "reasons": reasons,
                "info": model_info
            })
        
        # 점수 순 정렬
        candidates.sort(key=lambda x: x["score"], reverse=True)
        
        return candidates
    
    @staticmethod
    def _make_selections(
        candidates: List[Dict[str, Any]],
        characteristics: Dict[str, Any]
    ) -> List[LLMSelection]:
        """최종 LLM 선정"""
        
        selections = []
        
        # 주 모델 선정 (최고 점수)
        if candidates:
            main_model = candidates[0]
            
            # Capability 매핑
            capabilities = []
            for strength in main_model["info"]["strengths"]:
                if strength == "reasoning":
                    capabilities.append(ModelCapability.REASONING)
                elif strength == "code":
                    capabilities.append(ModelCapability.CODE_GENERATION)
                elif strength == "creative":
                    capabilities.append(ModelCapability.CREATIVE_WRITING)
            
            # SelectionReason 생성
            reasons = [
                SelectionReason(
                    criterion=r,
                    weight=0.8,
                    score=main_model["score"] / 10.0
                )
                for r in main_model["reasons"]
            ]
            
            selection = LLMSelection(
                model_id=main_model["model_name"],
                provider=main_model["info"]["provider"],
                role="primary",
                capabilities=capabilities,
                reasons=reasons,
                confidence=min(main_model["score"] / 10.0, 1.0)
            )
            
            selections.append(selection)
        
        # 보조 모델 (필요시)
        if characteristics["complexity"] > 6 and len(candidates) > 1:
            backup_model = candidates[1]
            
            backup_selection = LLMSelection(
                model_id=backup_model["model_name"],
                provider=backup_model["info"]["provider"],
                role="fallback",
                capabilities=[],
                reasons=[],
                confidence=0.7
            )
            
            selections.append(backup_selection)
        
        return selections
    
    @staticmethod
    def _optimize_prompts(
        selections: List[LLMSelection],
        design_document: Any
    ) -> Dict[str, str]:
        """모델별 프롬프트 최적화"""
        
        prompts = {}
        
        for selection in selections:
            provider = selection.provider
            
            # 기본 프롬프트
            base_prompt = f"다음 설계서를 바탕으로 작업을 수행해주세요:\n\n"
            
            # Provider별 최적화
            if provider == "anthropic":
                # Claude는 구조화된 프롬프트 선호
                optimized = base_prompt + "작업을 단계별로 수행하며, 각 단계의 근거를 명확히 설명해주세요."
            
            elif provider == "openai":
                # GPT는 명확한 지시 선호
                optimized = base_prompt + "요청사항을 정확히 따라 작업을 완료해주세요."
            
            elif provider == "google":
                # Gemini는 자연스러운 대화 스타일
                optimized = base_prompt + "설계서의 내용을 충실히 구현해주시기 바랍니다."
            
            else:
                optimized = base_prompt
            
            prompts[selection.model_id] = optimized
        
        return prompts

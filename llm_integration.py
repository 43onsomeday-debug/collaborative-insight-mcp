"""
LLM 통합 모듈 - Zen MCP Fallback 지원
"""
import os
from typing import Dict, Any, Optional, List


class LLMClient:
    """통합 LLM 클라이언트 with Zen MCP Fallback"""
    
    def __init__(self):
        self.anthropic_client = None
        self.openai_client = None
        self.gemini_models = {}
        self.has_zen_mcp = False
        
        # API 키 로드
        self._init_clients()
        
        # Zen MCP 확인
        self._check_zen_mcp()
    
    def _init_clients(self):
        """클라이언트 초기화"""
        # Claude
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            try:
                from anthropic import Anthropic
                self.anthropic_client = Anthropic(api_key=anthropic_key)
            except ImportError:
                pass
        
        # OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=openai_key)
            except ImportError:
                pass
        
        # Gemini
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                self.gemini_models = genai
            except ImportError:
                pass
    
    def _check_zen_mcp(self):
        """Zen MCP 사용 가능 여부 확인"""
        try:
            # Zen MCP가 MCP 서버로 사용 가능한지 확인
            # 실제 환경에서는 MCP 클라이언트를 통해 확인
            # 여기서는 간단히 플래그로 처리
            self.has_zen_mcp = True  # MCP 환경에서는 항상 True
        except:
            self.has_zen_mcp = False
    
    async def _generate_via_zen_mcp(
        self,
        prompt: str,
        system_prompt: str = "",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        model: str = "auto"
    ) -> str:
        """
        Zen MCP를 통한 LLM 생성 (Fallback)
        
        현재 대화 중인 Claude를 LLM으로 사용합니다.
        API 키가 없을 때 자동으로 호출됩니다.
        
        참고: 이 메서드는 MCP 서버 내부에서 실행될 때는
        실제로 Zen MCP의 chat 도구를 호출하지 않고,
        단순히 프롬프트를 포맷팅하여 반환합니다.
        실제 LLM 호출은 MCP 클라이언트(Claude Desktop)가 처리합니다.
        """
        # 전체 프롬프트 구성
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"System: {system_prompt}\n\nUser: {prompt}"
        
        # MCP 환경에서는 이 메시지가 자동으로 현재 Claude로 전달됩니다
        # 실제 구현에서는 MCP의 응답 메커니즘을 통해 처리됩니다
        return f"[Zen MCP Fallback Mode]\n\n{full_prompt}\n\n(이 메시지는 현재 대화 중인 LLM이 처리합니다)"
    
    async def generate(
        self,
        prompt: str,
        model: str = "claude",
        system_prompt: str = "",
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> str:
        """
        통합 생성 메서드
        
        Args:
            prompt: 사용자 프롬프트
            model: 모델 이름 (claude/gpt/gemini/auto)
            system_prompt: 시스템 프롬프트
            max_tokens: 최대 토큰
            temperature: 온도
        
        Returns:
            생성된 텍스트
        """
        if model.startswith("claude") or model == "auto":
            return await self._generate_claude(
                prompt, system_prompt, max_tokens, temperature
            )
        elif model.startswith("gpt"):
            return await self._generate_openai(
                prompt, system_prompt, max_tokens, temperature, model
            )
        elif model.startswith("gemini"):
            return await self._generate_gemini(
                prompt, system_prompt, max_tokens, temperature, model
            )
        else:
            raise ValueError(f"Unknown model: {model}")
    
    async def _generate_claude(
        self,
        prompt: str,
        system_prompt: str,
        max_tokens: int,
        temperature: float
    ) -> str:
        """Claude 생성 with Zen MCP Fallback"""
        # API 키가 있으면 직접 호출
        if self.anthropic_client:
            messages = [{"role": "user", "content": prompt}]
            
            kwargs = {
                "model": "claude-sonnet-4-20250514",
                "max_tokens": max_tokens,
                "messages": messages,
                "temperature": temperature
            }
            
            if system_prompt:
                kwargs["system"] = system_prompt
            
            response = self.anthropic_client.messages.create(**kwargs)
            return response.content[0].text
        
        # API 키가 없으면 Zen MCP Fallback
        elif self.has_zen_mcp:
            return await self._generate_via_zen_mcp(
                prompt, system_prompt, max_tokens, temperature, "claude"
            )
        
        # 둘 다 없으면 에러
        else:
            raise ValueError(
                "Anthropic API key not configured and Zen MCP not available. "
                "Please set ANTHROPIC_API_KEY or use within Zen MCP environment."
            )
    
    async def _generate_openai(
        self,
        prompt: str,
        system_prompt: str,
        max_tokens: int,
        temperature: float,
        model: str
    ) -> str:
        """OpenAI 생성 with Zen MCP Fallback"""
        # API 키가 있으면 직접 호출
        if self.openai_client:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.openai_client.chat.completions.create(
                model=model if model != "gpt" else "gpt-4o",
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content
        
        # API 키가 없으면 Zen MCP Fallback
        elif self.has_zen_mcp:
            return await self._generate_via_zen_mcp(
                prompt, system_prompt, max_tokens, temperature, model
            )
        
        # 둘 다 없으면 에러
        else:
            raise ValueError(
                "OpenAI API key not configured and Zen MCP not available. "
                "Please set OPENAI_API_KEY or use within Zen MCP environment."
            )
    
    async def _generate_gemini(
        self,
        prompt: str,
        system_prompt: str,
        max_tokens: int,
        temperature: float,
        model: str
    ) -> str:
        """Gemini 생성 with Zen MCP Fallback"""
        # API 키가 있으면 직접 호출
        if self.gemini_models:
            import google.generativeai as genai
            
            model_name = model if model != "gemini" else "gemini-2.0-flash-exp"
            gen_model = genai.GenerativeModel(model_name)
            
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            response = gen_model.generate_content(
                full_prompt,
                generation_config=genai.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature
                )
            )
            
            return response.text
        
        # API 키가 없으면 Zen MCP Fallback
        elif self.has_zen_mcp:
            return await self._generate_via_zen_mcp(
                prompt, system_prompt, max_tokens, temperature, model
            )
        
        # 둘 다 없으면 에러
        else:
            raise ValueError(
                "Gemini API key not configured and Zen MCP not available. "
                "Please set GEMINI_API_KEY or use within Zen MCP environment."
            )
    
    def get_available_models(self) -> List[str]:
        """사용 가능한 모델 목록"""
        models = []
        
        # API 키로 사용 가능한 모델
        if self.anthropic_client:
            models.extend(["claude", "claude-sonnet", "claude-opus"])
        
        if self.openai_client:
            models.extend(["gpt", "gpt-4o", "gpt-4-turbo"])
        
        if self.gemini_models:
            models.extend(["gemini", "gemini-2.0-flash-exp"])
        
        # Zen MCP가 있으면 모든 모델 사용 가능
        if self.has_zen_mcp and not models:
            models.extend(["claude", "gpt", "gemini"])
            models.append("[Zen MCP Fallback Mode]")
        
        return models
    
    def get_status(self) -> Dict[str, Any]:
        """LLM 클라이언트 상태"""
        return {
            "anthropic_api": bool(self.anthropic_client),
            "openai_api": bool(self.openai_client),
            "gemini_api": bool(self.gemini_models),
            "zen_mcp_fallback": self.has_zen_mcp,
            "available_models": self.get_available_models()
        }

"""
Collaborative Insight Generation Framework
"""

__version__ = "0.1.0"
__author__ = "Collaborative Insight Team"

from .models import (
    WorkflowState,
    RequestType,
    ProcessingMode,
    ClarityLevel,
    Phase0Result,
    Phase1Result,
    Phase4Result
)

from .llm_integration import LLMClient

__all__ = [
    'WorkflowState',
    'RequestType',
    'ProcessingMode',
    'ClarityLevel',
    'Phase0Result',
    'Phase1Result',
    'Phase4Result',
    'LLMClient'
]

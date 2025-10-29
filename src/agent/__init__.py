"""
Inicializador del módulo agent
"""

from .tools import (
    SearchProductsTool,
    CalculateDiscountTool,
    CheckInventoryTool,
    CustomerHistoryTool,
    initialize_tools
)

from .agent_executor import (
    PasteleriaAgentExecutor,
    create_agent
)

from .prompts import (
    AGENT_SYSTEM_PROMPT,
    INTENT_ANALYSIS_PROMPT,
    RECOMMENDATION_PROMPT
)

__all__ = [
    'SearchProductsTool',
    'CalculateDiscountTool', 
    'CheckInventoryTool',
    'CustomerHistoryTool',
    'initialize_tools',
    'PasteleriaAgentExecutor',
    'create_agent',
    'AGENT_SYSTEM_PROMPT'
]

from langchain_core.messages import SystemMessage, HumanMessage
from ..models.schema import AgentState
from ..utils.logging import get_logger
import yaml
import os

logger = get_logger(__name__)

class WriterAgent(BaseAgent):
    def __init__(self, settings, model, style="default"):
        self.model = model
        self.style = style
        self.WRITER_PROMPT = self._load_prompt(style)

    def _load_prompt(self, style: str) -> str:
        """Load the prompt from the styles.yaml file based on the given style."""
        styles_file = os.path.join(os.path.dirname(__file__), 'styles.yaml')
        with open(styles_file, 'r') as f:
            styles = yaml.safe_load(f)
        
        if style in styles:
            return styles[style]['prompt']
        else:
            # Default prompt if the style is not found
            return styles['default']['prompt']

    async def execute(self, state: AgentState) -> dict:
        try:
            content = "\n\n".join(state['content'] or [])
            user_message = HumanMessage(
                content=f"{state['task']}\n\nHere is my plan:\n\n{state['plan']}")
            messages = [
                SystemMessage(
                    content=self.WRITER_PROMPT.format(content=content)
                ),
                user_message
            ]
            response = await self.model.ainvoke(messages)
            return {
                "draft": response.content, 
                "revision_number": state.get("revision_number", 1) + 1,
                "lnode": "generate",
                "count": state.count + 1
            }
        except Exception as e:
            logger.exception(f"Error during writer execution: {e}")
            return {
                "draft": "Error occurred. Check logs.",
                "revision_number": state.get("revision_number", 1) + 1,
                "lnode": "generate",
                "count": state.count + 1
            }

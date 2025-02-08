+from langchain_core.messages import SystemMessage, HumanMessage
+from ..models.schema import AgentState
+
+class WriterAgent(BaseAgent):
+    def __init__(self, settings, model):
+        self.model = model
+        self.WRITER_PROMPT = ("You are an essay assistant tasked with writing excellent 3 paragraph essays. "
+                              "Generate the best essay possible for the user's request and the initial outline. "
+                              "If the user provides critique, respond with a revised version of your previous attempts. "
+                              "Utilize all the information below as needed: \n"
+                              "------\n"
+                              "{content}")
+
+    async def execute(self, state: AgentState) -> dict:
+        content = "\n\n".join(state['content'] or [])
+        user_message = HumanMessage(
+            content=f"{state['task']}\n\nHere is my plan:\n\n{state['plan']}")
+        messages = [
+            SystemMessage(
+                content=self.WRITER_PROMPT.format(content=content)
+            ),
+            user_message
+            ]
+        response = await self.model.ainvoke(messages)
+        return {
+            "draft": response.content, 
+            "revision_number": state.get("revision_number", 1) + 1,
+            "lnode": "generate",
+            "count": state.count + 1,
+        }

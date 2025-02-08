import gradio as gr
from ..utils.state import StateManager
from ..config import Settings

class EssayWriterUI:
    def __init__(self, state_manager: StateManager, settings: Settings):
        self.state_manager = state_manager
        self.settings = settings
        
    def create_interface(self) -> gr.Blocks:
        with gr.Blocks() as interface:
            with gr.Tab("Essay Writer"):
                with gr.Row():
                    topic_input = gr.Textbox(
                        label="Essay Topic",
                        placeholder="Enter topic here..."
                    )
                    generate_btn = gr.Button("Generate Essay")
                
                with gr.Row():
                    output_text = gr.Textbox(
                        label="Generated Essay",
                        interactive=False
                    )
                    
                generate_btn.click(
                    fn=self._handle_generate,
                    inputs=[topic_input],
                    outputs=[output_text]
                )
            
            return interface
            
    async def _handle_generate(self, topic: str) -> str:
        state = await self.state_manager.get_state("main")
        state.task = topic
        # Implementation of essay generation workflow
        return "Generated essay would appear here"
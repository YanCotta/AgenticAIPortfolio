import gradio as gr
from ..utils.state import StateManager
from ..config import Settings
import os
from ..workflow.essay_workflow import EssayWorkflow
from ..agents.planner import PlannerAgent
from ..agents.researcher import ResearchAgent
from ..agents.writer import WriterAgent
from ..agents.critic import CriticAgent
from langchain_openai import ChatOpenAI
from typing import List, Dict, Tuple, Any
from ..controller.essay_controller import EssayController
from ..utils.logging import get_logger

logger = get_logger(__name__)

class EssayWriterUI:
    def __init__(self, state_manager: StateManager, settings: Settings):
        self.state_manager = state_manager
        self.settings = settings
        self.model = ChatOpenAI(model=settings.MODEL_NAME, temperature=0)
        self.research_service = ResearchService(settings)
        self.planner = PlannerAgent(settings, self.model)
        self.researcher = ResearchAgent(settings, self.research_service, self.model)
        self.writer = WriterAgent(settings, self.model)
        self.critic = CriticAgent(settings, self.model)
        self.essay_workflow = EssayWorkflow(self.planner, self.researcher, self.writer, self.critic)
        
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
        try:
            essay_state = await self.essay_workflow.generate_essay(topic)
            return essay_state.draft
        except Exception as e:
            logger.exception(f"Error during essay generation: {e}")
            return "An error occurred during essay generation. Please check the logs."

import time

class GradioUI:
    def __init__(self, planner: PlannerAgent, researcher: ResearchAgent, writer: WriterAgent, critic: CriticAgent, graph: Any, share: bool=False):
        self.planner = planner
        self.researcher = researcher
        self.writer = writer
        self.critic = critic
        self.controller = EssayController(graph)
        self.share = share
        self.demo: gr.Blocks = self.create_interface()

    def run_agent(self, start: bool, topic: str, stop_after: List[str]) -> Tuple[str, str, str, int, int, int]:
        if start:
            self.controller.start_new_thread(topic)
        try:
            for output in self.controller.run_agent(start, topic, stop_after):
                # output is a tuple: (live_output, lnode, nnode, thread_id, rev, acount)
                yield *output  # Yield all elements of the tuple
        except Exception as e:
            logger.exception(f"Error during agent execution: {e}")
            yield "Error occurred. Check logs.", "", "", self.controller.thread_id, 0, 0

    def get_disp_state(self) -> Tuple[str, str, int, int, int]:
        return self.controller.get_disp_state()

    def get_state(self, key: str) -> gr.Textbox:
        return self.controller.get_state(key)

    def get_content(self) -> gr.Textbox:
        return self.controller.get_content()

    def update_hist_pd(self) -> gr.Dropdown:
        return self.controller.update_hist_pd()

    def find_config(self, thread_ts: str) -> Dict[str, Any]:
        return self.controller.find_config(thread_ts)

    def copy_state(self, hist_str: str) -> Tuple[str, str, str, int, int]:
        return self.controller.copy_state(hist_str)

    def update_thread_pd(self) -> gr.Dropdown:
        return self.controller.update_thread_pd()

    def switch_thread(self, new_thread_id: int) -> None:
        self.controller.switch_thread(new_thread_id)

    def modify_state(self, key: str, asnode: str, new_state: str) -> None:
        self.controller.modify_state(key, asnode, new_state)

    def create_interface(self) -> gr.Blocks:
        with gr.Blocks(theme=gr.themes.Default(spacing_size='sm', text_size="sm")) as demo:
            def updt_disp() -> Dict[str, Any]:
                current_state = self.controller.graph.get_state(self.controller.thread)
                hist: List[str] = []
                for state in self.controller.graph.get_state_history(self.controller.thread):
                    if state.metadata['step'] < 1:
                        continue
                    s_thread_ts: str = state.config['configurable']['thread_ts']
                    s_tid: str = state.config['configurable']['thread_id']
                    s_count: int = state.values['count']
                    s_lnode: str = state.values['lnode']
                    s_rev: int = state.values['revision_number']
                    s_nnode: str = state.next
                    st: str = f"{s_tid}:{s_count}:{s_lnode}:{s_nnode}:{s_rev}:{s_thread_ts}"
                    hist.append(st)
                if not current_state.metadata:
                    return {}
                else:
                    return {
                        topic_bx: current_state.values["task"],
                        lnode_bx: current_state.values["lnode"],
                        count_bx: current_state.values["count"],
                        revision_bx: current_state.values["revision_number"],
                        nnode_bx: current_state.next,
                        threadid_bx: self.controller.thread_id,
                        thread_pd: gr.Dropdown(label="choose thread", choices=self.controller.threads, value=self.controller.thread_id, interactive=True),
                        step_pd: gr.Dropdown(label="update_state from: thread:count:last_node:next_node:rev:thread_ts", 
                                             choices=hist, value=hist[0], interactive=True),
                    }
            
            def get_snapshots() -> gr.Textbox:
                new_label: str = f"thread_id: {self.controller.thread_id}, Summary of snapshots"
                sstate: str = ""
                for state in self.controller.graph.get_state_history(self.controller.thread):
                    for key in ['plan', 'draft', 'critique']:
                        if key in state.values:
                            state.values[key] = state.values[key][:80] + "..."
                    if 'content' in state.values:
                        for i in range(len(state.values['content'])):
                            state.values['content'][i] = state.values['content'][i][:20] + '...'
                    if 'writes' in state.metadata:
                        state.metadata['writes'] = "not shown"
                    sstate += str(state) + "\n\n"
                return gr.update(label=new_label, value=sstate)

            def vary_btn(stat: str) -> gr.Button:
                return gr.update(variant=stat)
            
            with gr.Tab("Agent"):
                with gr.Row():
                    topic_bx = gr.Textbox(label="Essay Topic", value="Pizza Shop")
                    gen_btn = gr.Button("Generate Essay", scale=0, min_width=80, variant='primary')
                    cont_btn = gr.Button("Continue Essay", scale=0, min_width=80)
                with gr.Row():
                    lnode_bx = gr.Textbox(label="last node", min_width=100)
                    nnode_bx = gr.Textbox(label="next node", min_width=100)
                    threadid_bx = gr.Textbox(label="Thread", scale=0, min_width=80)
                    revision_bx = gr.Textbox(label="Draft Rev", scale=0, min_width=80)
                    count_bx = gr.Textbox(label="count", scale=0, min_width=80)
                with gr.Accordion("Manage Agent", open=False):
                    checks: List[str] = list(self.controller.graph.nodes.keys())
                    checks.remove('__start__')
                    stop_after = gr.CheckboxGroup(checks, label="Interrupt After State", value=checks, scale=0, min_width=400)
                    with gr.Row():
                        thread_pd = gr.Dropdown(choices=self.controller.threads, interactive=True, label="select thread", min_width=120, scale=0)
                        step_pd = gr.Dropdown(choices=['N/A'], interactive=True, label="select step", min_width=160, scale=1)
                live = gr.Textbox(label="Live Agent Output", lines=5, max_lines=5)
                progress_bar = gr.Progress(label="Essay Progress")
        
                sdisps: List[gr.Textbox] = [topic_bx, lnode_bx, nnode_bx, threadid_bx, revision_bx, count_bx, step_pd, thread_pd]
                thread_pd.input(self.switch_thread, [thread_pd], None).then(
                    fn=updt_disp, inputs=None, outputs=sdisps)
                step_pd.input(self.copy_state, [step_pd], None).then(
                    fn=updt_disp, inputs=None, outputs=sdisps)
                gen_btn.click(vary_btn, gr.Number("secondary", visible=False), gen_btn).then(
                    fn=self.run_agent, inputs=[gr.Number(True, visible=False), topic_bx, stop_after], 
                    outputs=[live, lnode_bx, nnode_bx, threadid_bx, revision_bx, count_bx], show_progress=True).then(
                    fn=updt_disp, inputs=None, outputs=sdisps).then(
                    vary_btn, gr.Number("primary", visible=False), gen_btn).then(
                    vary_btn, gr.Number("primary", visible=False), cont_btn)
                cont_btn.click(vary_btn, gr.Number("secondary", visible=False), cont_btn).then(
                    fn=self.run_agent, inputs=[gr.Number(False, visible=False), topic_bx, stop_after], 
                    outputs=[live, lnode_bx, nnode_bx, threadid_bx, revision_bx, count_bx], show_progress=True).then(
                    fn=updt_disp, inputs=None, outputs=sdisps).then(
                    vary_btn, gr.Number("primary", visible=False), cont_btn)
        
            with gr.Tab("Plan"):
                with gr.Row():
                    refresh_btn = gr.Button("Refresh")
                    modify_btn = gr.Button("Modify")
                plan = gr.Textbox(label="Plan", lines=10, interactive=True)
                refresh_btn.click(fn=self.get_state, inputs=gr.Number("plan", visible=False), outputs=plan)
                modify_btn.click(fn=self.modify_state, inputs=[gr.Number("plan", visible=False),
                                                               gr.Number("planner", visible=False), plan], outputs=None).then(
                    fn=updt_disp, inputs=None, outputs=sdisps)
            with gr.Tab("Research Content"):
                refresh_btn = gr.Button("Refresh")
                content_bx = gr.Textbox(label="content", lines=10)
                refresh_btn.click(fn=self.get_content, inputs=None, outputs=content_bx)
            with gr.Tab("Draft"):
                with gr.Row():
                    refresh_btn = gr.Button("Refresh")
                    modify_btn = gr.Button("Modify")
                draft_bx = gr.Textbox(label="draft", lines=10, interactive=True)
                refresh_btn.click(fn=self.get_state, inputs=gr.Number("draft", visible=False), outputs=draft_bx)
                modify_btn.click(fn=self.modify_state, inputs=[gr.Number("draft", visible=False),
                                                               gr.Number("generate", visible=False), draft_bx], outputs=None).then(
                    fn=updt_disp, inputs=None, outputs=sdisps)
            with gr.Tab("Critique"):
                with gr.Row():
                    refresh_btn = gr.Button("Refresh")
                    modify_btn = gr.Button("Modify")
                critique_bx = gr.Textbox(label="Critique", lines=10, interactive=True)
                refresh_btn.click(fn=self.get_state, inputs=gr.Number("critique", visible=False), outputs=critique_bx)
                modify_btn.click(fn=self.modify_state, inputs=[gr.Number("critique", visible=False),
                                                               gr.Number("reflect", visible=False), 
                                                               critique_bx], outputs=None).then(
                    fn=updt_disp, inputs=None, outputs=sdisps)
            with gr.Tab("StateSnapShots"):
                with gr.Row():
                    refresh_btn = gr.Button("Refresh")
                snapshots = gr.Textbox(label="State Snapshots Summaries")
                refresh_btn.click(fn=get_snapshots, inputs=None, outputs=snapshots)
        return demo

    def launch(self, share: bool=None) -> None:
        if port := os.getenv("PORT1"):
            self.demo.launch(share=True, server_port=int(port), server_name="0.0.0.0")
        else:
            self.demo.launch(share=self.share)
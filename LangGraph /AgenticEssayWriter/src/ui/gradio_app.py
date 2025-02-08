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
        essay_state = await self.essay_workflow.generate_essay(topic)
        return essay_state.draft

import time

class GradioUI:
    def __init__(self, planner: PlannerAgent, researcher: ResearchAgent, writer: WriterAgent, critic: CriticAgent, graph: Any, share: bool=False):
        self.planner = planner
        self.researcher = researcher
        self.writer = writer
        self.critic = critic
        self.controller = EssayController(graph)
        self.share = share
        #self.sdisps = {} #global    
        self.demo: gr.Blocks = self.create_interface()

    def run_agent(self, start: bool, topic: str, stop_after: List[str]) -> Tuple[str, str, str, int, int, int]:int] = []
        if start:
            self.controller.start_new_thread(topic)tr, str]] = {"configurable": {"thread_id": str(self.thread_id)}}
        while self.controller.iterations[self.controller.thread_id] < self.controller.max_iterations:
            self.controller.response = self.controller.graph.invoke(self.controller.config, self.controller.thread)        self.demo: gr.Blocks = self.create_interface()
            self.controller.iterations[self.controller.thread_id] += 1
            self.controller.partial_message += str(self.controller.response)stop_after: List[str]) -> Tuple[str, str, str, int, int, int]:
            self.controller.partial_message += f"\n------------------\n\n"
            lnode, nnode, _, rev, acount = self.get_disp_state()esponse, max_iterations, iterations, threads
            yield self.controller.partial_message, lnode, nnode, self.controller.thread_id, rev, acount
            self.controller.config = None
            if not nnode:
                returnue': "no critique", 
            if lnode in stop_after:es': "no queries", 'count':0}
                returnew thread
        returnelf.threads.append(self.thread_id)
    
    def get_disp_state(self):
        current_state = self.controller.graph.get_state(self.controller.thread)_id)}}
        lnode = current_state.values["lnode"]s:
        acount = current_state.values["count"]nfig, self.thread)
        rev = current_state.values["revision_number"]
        nnode = current_state.next
        return lnode, nnode, self.controller.thread_id, rev, acountartial_message += f"\n------------------\n\n"
    
    def get_state(self, key):
        current_values = self.controller.graph.get_state(self.controller.thread)message,lnode,nnode,self.thread_id,rev,acount
        if key in current_values.values:
            lnode, nnode, self.controller.thread_id, rev, astep = self.get_disp_state()ent:{lnode}")
            new_label = f"last_node: {lnode}, thread_id: {self.controller.thread_id}, rev: {rev}, step: {astep}"
            return gr.update(label=new_label, value=current_values.values[key])("Hit the end")
        else:
            return ""  
    (f"stopping due to stop_after {lnode}")
    def get_content(self):eturn
        current_values = self.controller.graph.get_state(self.controller.thread)
        if "content" in current_values.values:nt(f"Not stopping on lnode {lnode}")
            content = current_values.values["content"]  pass
            lnode, nnode, thread_id, rev, astep = self.get_disp_state()    return
            new_label = f"last_node: {lnode}, thread_id: {thread_id}, rev: {rev}, step: {astep}"
            return gr.update(label=new_label, value="\n\n".join(item for item in content) + "\n\n"), int]:
        else:self.thread)
            return ""  de"]
    
    def update_hist_pd(self):alues["revision_number"]
        hist = []
        for state in self.controller.graph.get_state_history(self.controller.thread):nt)
            if state.metadata['step'] < 1:    return lnode,nnode,self.thread_id,rev,acount
                continue
            thread_ts = state.config['configurable']['thread_ts']
            tid = state.config['configurable']['thread_id']state(self.thread)
            count = state.values['count']
            lnode = state.values['lnode']
            rev = state.values['revision_number'] {rev}, step: {astep}"
            nnode = state.nexteturn gr.update(label=new_label, value=current_values.values[key])
            st = f"{tid}:{count}:{lnode}:{nnode}:{rev}:{thread_ts}"
            hist.append(st)        return ""  
        return gr.Dropdown(label="update_state from: thread:count:last_node:next_node:rev:thread_ts", 
                           choices=hist, value=hist[0], interactive=True)
    self.thread)
    def find_config(self, thread_ts):
        for state in self.controller.graph.get_state_history(self.controller.thread):
            config = state.config
            if config['configurable']['thread_ts'] == thread_ts:
                return configeturn gr.update(label=new_label, value="\n\n".join(item for item in content) + "\n\n")
        return None
                    return ""  
    def copy_state(self, hist_str):
        thread_ts = hist_str.split(":")[-1] gr.Dropdown:
        config = self.find_config(thread_ts)pdate_hist_pd")
        state = self.controller.graph.get_state(config)
        self.controller.graph.update_state(self.controller.thread, state.values, as_node=state.values['lnode'])
        new_state = self.controller.graph.get_state(self.controller.thread)history(self.thread):
        new_thread_ts = new_state.config['configurable']['thread_ts']adata['step'] < 1:
        tid = new_state.config['configurable']['thread_id']
        count = new_state.values['count']thread_ts']
        lnode = new_state.values['lnode']igurable']['thread_id']
        rev = new_state.values['revision_number']unt']
        nnode = new_state.next
        return lnode, nnode, new_thread_ts, rev, countalues['revision_number']
    
    def update_thread_pd(self):d}:{count}:{lnode}:{nnode}:{rev}:{thread_ts}"
        return gr.Dropdown(label="choose thread", choices=self.controller.threads, value=self.controller.thread_id, interactive=True)
    ode:next_node:rev:thread_ts", 
    def switch_thread(self, new_thread_id):                       choices=hist, value=hist[0],interactive=True)
        self.controller.thread = {"configurable": {"thread_id": str(new_thread_id)}}
        self.controller.thread_id = new_thread_id
        return et_state_history(self.thread):
    
    def modify_state(self, key, asnode, new_state):urable']['thread_ts'] == thread_ts:
        current_values = self.controller.graph.get_state(self.controller.thread)rn config
        current_values.values[key] = new_statern(None)
        self.controller.graph.update_state(self.controller.thread, current_values.values, as_node=asnode)
        return
ldown. Note does not change thread. 
    def create_interface(self):  This copies an old state to a new current state. 
        with gr.Blocks(theme=gr.themes.Default(spacing_size='sm', text_size="sm")) as demo:
            1]
            def updt_disp():")
                current_state = self.controller.graph.get_state(self.controller.thread)tr, Any] = self.find_config(thread_ts)
                hist = []
                for state in self.controller.graph.get_state_history(self.controller.thread):
                    if state.metadata['step'] < 1:.values['lnode'])
                        continuetch
                    s_thread_ts = state.config['configurable']['thread_ts']']['thread_ts']
                    s_tid = state.config['configurable']['thread_id']igurable']['thread_id']
                    s_count = state.values['count']unt']
                    s_lnode = state.values['lnode']
                    s_rev = state.values['revision_number']alues['revision_number']
                    s_nnode = state.next
                    st = f"{s_tid}:{s_count}:{s_lnode}:{s_nnode}:{s_rev}:{s_thread_ts}"    return lnode,nnode,new_thread_ts,rev,count
                    hist.append(st)
                if not current_state.metadata: gr.Dropdown:
                    return {}
                else:    return gr.Dropdown(label="choose thread", choices=threads, value=self.thread_id,interactive=True)
                    return {
                        topic_bx: current_state.values["task"],-> None:
                        lnode_bx: current_state.values["lnode"],
                        count_bx: current_state.values["count"], {"thread_id": str(new_thread_id)}}
                        revision_bx: current_state.values["revision_number"],read_id = new_thread_id
                        nnode_bx: current_state.next,    return 
                        threadid_bx: self.controller.thread_id,
                        thread_pd: gr.Dropdown(label="choose thread", choices=self.controller.threads, value=self.controller.thread_id, interactive=True),
                        step_pd: gr.Dropdown(label="update_state from: thread:count:last_node:next_node:rev:thread_ts", 
                                             choices=hist, value=hist[0], interactive=True),multiple times with different keys, it will create
                    } for each update. Note also that it doesn't resume after the update
            
            def get_snapshots():self.thread)
                new_label = f"thread_id: {self.controller.thread_id}, Summary of snapshots"
                sstate = ""raph.update_state(self.thread, current_values.values,as_node=asnode)
                for state in self.controller.graph.get_state_history(self.controller.thread):        return
                    for key in ['plan', 'draft', 'critique']:
                        if key in state.values:
                            state.values[key] = state.values[key][:80] + "..."
                    if 'content' in state.values: gr.Blocks(theme=gr.themes.Default(spacing_size='sm',text_size="sm")) as demo:
                        for i in range(len(state.values['content'])):
                            state.values['content'][i] = state.values['content'][i][:20] + '...'
                    if 'writes' in state.metadata:
                        state.metadata['writes'] = "not shown"tate = self.graph.get_state(self.thread)
                    sstate += str(state) + "\n\n"
                return gr.update(label=new_label, value=sstate)

            def vary_btn(stat):adata['step'] < 1:  #ignore early states
                return gr.update(variant=stat)
            thread_ts']
            with gr.Tab("Agent"):igurable']['thread_id']
                with gr.Row():unt']
                    topic_bx = gr.Textbox(label="Essay Topic", value="Pizza Shop")
                    gen_btn = gr.Button("Generate Essay", scale=0, min_width=80, variant='primary')alues['revision_number']
                    cont_btn = gr.Button("Continue Essay", scale=0, min_width=80)
                with gr.Row():tid}:{s_count}:{s_lnode}:{s_nnode}:{s_rev}:{s_thread_ts}"
                    lnode_bx = gr.Textbox(label="last node", min_width=100)
                    nnode_bx = gr.Textbox(label="next node", min_width=100)nt_state.metadata: #handle init call
                    threadid_bx = gr.Textbox(label="Thread", scale=0, min_width=80)eturn{}
                    revision_bx = gr.Textbox(label="Draft Rev", scale=0, min_width=80)
                    count_bx = gr.Textbox(label="count", scale=0, min_width=80)
                with gr.Accordion("Manage Agent", open=False):
                    checks = list(self.controller.graph.nodes.keys())
                    checks.remove('__start__')
                    stop_after = gr.CheckboxGroup(checks, label="Interrupt After State", value=checks, scale=0, min_width=400)lues["revision_number"],
                    with gr.Row():,
                        thread_pd = gr.Dropdown(choices=self.controller.threads, interactive=True, label="select thread", min_width=120, scale=0)
                        step_pd = gr.Dropdown(choices=['N/A'], interactive=True, label="select step", min_width=160, scale=1)tive=True),
                live = gr.Textbox(label="Live Agent Output", lines=5, max_lines=5)d:count:last_node:next_node:rev:thread_ts", 
                  choices=hist, value=hist[0],interactive=True),
                sdisps = [topic_bx, lnode_bx, nnode_bx, threadid_bx, revision_bx, count_bx, step_pd, thread_pd]
                thread_pd.input(self.switch_thread, [thread_pd], None).then(
                    fn=updt_disp, inputs=None, outputs=sdisps)str = f"thread_id: {self.thread_id}, Summary of snapshots"
                step_pd.input(self.copy_state, [step_pd], None).then(
                    fn=updt_disp, inputs=None, outputs=sdisps)f.thread):
                gen_btn.click(vary_btn, gr.Number("secondary", visible=False), gen_btn).then(, 'critique']:
                    fn=self.run_agent, inputs=[gr.Number(True, visible=False), topic_bx, stop_after], outputs=[live], show_progress=True).then(
                    fn=updt_disp, inputs=None, outputs=sdisps).then(tate.values[key][:80] + "..."
                    vary_btn, gr.Number("primary", visible=False), gen_btn).then(
                    vary_btn, gr.Number("primary", visible=False), cont_btn)
                cont_btn.click(vary_btn, gr.Number("secondary", visible=False), cont_btn).then(][i] = state.values['content'][i][:20] + '...'
                    fn=self.run_agent, inputs=[gr.Number(False, visible=False), topic_bx, stop_after], 
                    outputs=[live]).then(= "not shown"
                    fn=updt_disp, inputs=None, outputs=sdisps).then(
                    vary_btn, gr.Number("primary", visible=False), cont_btn)                return gr.update(label=new_label, value=sstate)
        
            with gr.Tab("Plan"):.Button:
                with gr.Row():
                    refresh_btn = gr.Button("Refresh")    return(gr.update(variant=stat))
                    modify_btn = gr.Button("Modify")
                plan = gr.Textbox(label="Plan", lines=10, interactive=True)"):
                refresh_btn.click(fn=self.get_state, inputs=gr.Number("plan", visible=False), outputs=plan)
                modify_btn.click(fn=self.modify_state, inputs=[gr.Number("plan", visible=False),
                                                               gr.Number("planner", visible=False), plan], outputs=None).then(variant='primary')
                    fn=updt_disp, inputs=None, outputs=sdisps) gr.Button("Continue Essay", scale=0,min_width=80)
            with gr.Tab("Research Content"):
                refresh_btn = gr.Button("Refresh")
                content_bx = gr.Textbox(label="content", lines=10)
                refresh_btn.click(fn=self.get_content, inputs=None, outputs=content_bx)
            with gr.Tab("Draft"):dth=80)
                with gr.Row():=0, min_width=80)
                    refresh_btn = gr.Button("Refresh")se):
                    modify_btn = gr.Button("Modify")elf.graph.nodes.keys())
                draft_bx = gr.Textbox(label="draft", lines=10, interactive=True)
                refresh_btn.click(fn=self.get_state, inputs=gr.Number("draft", visible=False), outputs=draft_bx)r.CheckboxGroup(checks,label="Interrupt After State", value=checks, scale=0, min_width=400)
                modify_btn.click(fn=self.modify_state, inputs=[gr.Number("draft", visible=False),
                                                               gr.Number("generate", visible=False), draft_bx], outputs=None).then( scale=0)
                    fn=updt_disp, inputs=None, outputs=sdisps)bel="select step", min_width=160, scale=1)
            with gr.Tab("Critique"):        live = gr.Textbox(label="Live Agent Output", lines=5, max_lines=5)
                with gr.Row():
                    refresh_btn = gr.Button("Refresh")
                    modify_btn = gr.Button("Modify")id_bx,revision_bx,count_bx,step_pd,thread_pd]
                critique_bx = gr.Textbox(label="Critique", lines=10, interactive=True)n(
                refresh_btn.click(fn=self.get_state, inputs=gr.Number("critique", visible=False), outputs=critique_bx)sdisps)
                modify_btn.click(fn=self.modify_state, inputs=[gr.Number("critique", visible=False),
                                                               gr.Number("reflect", visible=False), 
                                                               critique_bx], outputs=None).then(
                    fn=updt_disp, inputs=None, outputs=sdisps)e=False),topic_bx,stop_after], outputs=[live],show_progress=True).then(
            with gr.Tab("StateSnapShots"):
                with gr.Row():then(
                    refresh_btn = gr.Button("Refresh")
                snapshots = gr.Textbox(label="State Snapshots Summaries")
                refresh_btn.click(fn=get_snapshots, inputs=None, outputs=snapshots)puts=[gr.Number(False, visible=False),topic_bx,stop_after], 
        return demo

    def launch(self, share=None):                       vary_btn,gr.Number("primary", visible=False), cont_btn)
        if port := os.getenv("PORT1"):
            self.demo.launch(share=True, server_port=int(port), server_name="0.0.0.0")):
        else:
            self.demo.launch(share=self.share)            self.demo.launch(share=self.share)
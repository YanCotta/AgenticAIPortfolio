from typing import List, Dict, Any, Tuple
import gradio as gr
from ..utils.logging import get_logger

logger = get_logger(__name__)

class EssayController:
    def __init__(self, graph: Any):
        self.graph = graph
        self.threads: List[int] = []
        self.thread_id: int = -1
        self.thread: Dict[str, Dict[str, str]] = {"configurable": {"thread_id": str(self.thread_id)}}
        self.partial_message: str = ""
        self.response: Dict[str, Any] = {}
        self.max_iterations: int = 10
        self.iterations: List[int] = []
        self.config: Dict[str, Any] = {}

    def run_agent(self, start: bool, topic: str, stop_after: List[str]) -> Tuple[str, str, str, int, int, int]:
        if start:
            self.start_new_thread(topic)
        config: Dict[str, Any] = self.config
        self.thread = {"configurable": {"thread_id": str(self.thread_id)}}
        while self.iterations[self.thread_id] < self.max_iterations:
            try:
                self.response = self.graph.invoke(config, self.thread)
            except Exception as e:
                logger.exception(f"Error during graph invocation: {e}")
                yield "Error occurred. Check logs.", "", "", self.thread_id, 0, 0
                return
            self.iterations[self.thread_id] += 1
            self.partial_message += str(self.response)
            self.partial_message += f"\n------------------\n\n"
            ## fix
            lnode,nnode,_,rev,acount = self.get_disp_state()
            yield self.partial_message,lnode,nnode,self.thread_id,rev,acount
            config = None #need
            if not nnode:  
                return
            if lnode in stop_after:
                return
            else:
                pass
        return
    
    def start_new_thread(self, topic: str) -> None:
        self.iterations.append(0)
        self.config = {'task': topic,"max_revisions": 2,"revision_number": 0,
                  'lnode': "", 'planner': "no plan", 'draft': "no draft", 'critique': "no critique", 
                  'content': ["no content",], 'queries': "no queries", 'count':0}
        self.thread_id += 1  # new agent, new thread
        self.threads.append(self.thread_id)
     
    def get_disp_state(self,) -> Tuple[str, str, int, int, int]:
        current_state = self.graph.get_state(self.thread)
        lnode: str = current_state.values["lnode"]
        acount: int = current_state.values["count"]
        rev: int = current_state.values["revision_number"]
        nnode: str = current_state.next
        return lnode,nnode,self.thread_id,rev,acount
    
    def get_state(self,key: str) -> gr.Textbox:
        current_values = self.graph.get_state(self.thread)
        if key in current_values.values:
            lnode,nnode,self.thread_id,rev,astep = self.get_disp_state()
            new_label = f"last_node: {lnode}, thread_id: {self.thread_id}, rev: {rev}, step: {astep}"
            return gr.update(label=new_label, value=current_values.values[key])
        else:
            return ""  
    
    def get_content(self,) -> gr.Textbox:
        current_values = self.graph.get_state(self.thread)
        if "content" in current_values.values:
            content: List[str] = current_values.values["content"]
            lnode,nnode,thread_id,rev,astep = self.get_disp_state()
            new_label = f"last_node: {lnode}, thread_id: {thread_id}, rev: {rev}, step: {astep}"
            return gr.update(label=new_label, value="\n\n".join(item for item in content) + "\n\n")
        else:
            return ""  
    
    def update_hist_pd(self,) -> gr.Dropdown:
        hist: List[str] = []
        for state in self.graph.get_state_history(self.thread):
            if state.metadata['step'] < 1:
                continue
            thread_ts: str = state.config['configurable']['thread_ts']
            tid: str = state.config['configurable']['thread_id']
            count: int = state.values['count']
            lnode: str = state.values['lnode']
            rev: int = state.values['revision_number']
            nnode: str = state.next
            st: str = f"{tid}:{count}:{lnode}:{nnode}:{rev}:{thread_ts}"
            hist.append(st)
        return gr.Dropdown(label="update_state from: thread:count:last_node:next_node:rev:thread_ts", 
                           choices=hist, value=hist[0],interactive=True)
    
    def find_config(self,thread_ts: str) -> Dict[str, Any]:
        for state in self.graph.get_state_history(self.thread):
            config: Dict[str, Any] = state.config
            if config['configurable']['thread_ts'] == thread_ts:
                return config
        return(None)
            
    def copy_state(self,hist_str: str) -> Tuple[str, str, str, int, int]:
        ''' result of selecting an old state from the step pulldown. Note does not change thread. 
             This copies an old state to a new current state. 
        '''
        thread_ts: str = hist_str.split(":")[-1]
        config: Dict[str, Any] = self.find_config(thread_ts)
        state = self.graph.get_state(config)
        self.graph.update_state(self.thread, state.values, as_node=state.values['lnode'])
        new_state = self.graph.get_state(self.thread)  #should now match
        new_thread_ts: str = new_state.config['configurable']['thread_ts']
        tid: str = new_state.config['configurable']['thread_id']
        count: int = new_state.values['count']
        lnode: str = new_state.values['lnode']
        rev: int = new_state.values['revision_number']
        nnode: str = new_state.next
        return lnode,nnode,new_thread_ts,rev,count
    
    def update_thread_pd(self,) -> gr.Dropdown:
        return gr.Dropdown(label="choose thread", choices=self.threads, value=self.thread_id,interactive=True)
    
    def switch_thread(self,new_thread_id: int) -> None:
        self.thread = {"configurable": {"thread_id": str(new_thread_id)}}
        self.thread_id = new_thread_id
        return 
    
    def modify_state(self,key: str, asnode: str, new_state: str) -> None:
        ''' gets the current state, modifes a single value in the state identified by key, and updates state with it.
        note that this will create a new 'current state' node. If you do this multiple times with different keys, it will create
        one for each update. Note also that it doesn't resume after the update
        '''
        current_values = self.graph.get_state(self.thread)
        current_values.values[key] = new_state
        self.graph.update_state(self.thread, current_values.values,as_node=asnode)
        return

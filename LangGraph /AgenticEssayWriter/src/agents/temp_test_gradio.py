#!/usr/bin/env python
# coding: utf-8

# # Lesson 6: Essay Writer

# In[ ]:


from dotenv import load_dotenv

_ = load_dotenv()


# In[ ]:


from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ChatMessage

#memory = SqliteSaver.from_conn_string(":memory:")


# In[ ]:


# import sqlite3
# def from_conn_stringx(cls, conn_string: str,) -> "SqliteSaver":
#     return SqliteSaver(conn=sqlite3.connect(conn_string, check_same_thread=False))
# SqliteSaver.from_conn_stringx=classmethod(from_conn_stringx)
# memory = SqliteSaver.from_conn_stringx(":memory:")
# type(memory)


# In[ ]:


# modified to allow sqlite to allow requests from other python threads (read only - not write safe)
# import sqlite3
# conn_string = ":memory:"
# memory = SqliteSaver(conn=sqlite3.connect(conn_string, check_same_thread=False))
#


# In[ ]:


#def inc_steps(left: int, right: int) -> int:
#    return left + right

class AgentState(TypedDict):
    task: str
    lnode: str
    plan: str
    draft: str
    critique: str
    content: List[str]
    queries: List[str]
    revision_number: int
    max_revisions: int
    steps: Annotated[int, operator.add]


# In[ ]:


from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


# In[ ]:


PLAN_PROMPT = """You are an expert writer tasked with writing a high level outline of an 3-paragraph essay. \
Write such an outline for the user provided topic. Give the main headers of an outline of the essay along with any relevant notes \
or instructions for the sections.Just provide the five headings, dont elaborate, this is a short essay."""


# In[ ]:


WRITER_PROMPT = """You are an essay assistant tasked with writing excellent 3-paragraph essays.\
Generate the best essay possible for the user's request and the initial outline. \
If the user provides critique, respond with a revised version of your previous attempts. \
Utilize all the information below as needed: 

------

{content}"""


# In[ ]:


RESEARCH_PLAN_PROMPT = """You are a researcher charged with providing information that can \
be used when writing the following essay. Generate a list of search queries that will gather \
any relevant information. Only generate 3 queries max."""


# In[ ]:


REFLECTION_PROMPT = """You are a teacher grading an 3-paragraph essay submission. \
Generate critique and recommendations for the user's submission. \
Provide detailed recommendations, including requests for length, depth, style, etc."""


# In[ ]:


RESEARCH_CRITIQUE_PROMPT = """You are a researcher charged with providing information that can \
be used when making any requested revisions (as outlined below). \
Generate a list of search queries that will gather any relevant information. Only generate 3 queries max."""


# In[ ]:


from langchain_core.pydantic_v1 import BaseModel

class Queries(BaseModel):
    queries: List[str]


# In[ ]:


from tavily import TavilyClient
import os
tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


# In[ ]:


def plan_node(state: AgentState):
    messages = [
        SystemMessage(content=PLAN_PROMPT), 
        HumanMessage(content=state['task'])
    ]
    response = model.invoke(messages)
    return {"plan": response.content,
           "lnode": "plan",
            "steps": 1,
           }


# In[ ]:


def research_plan_node(state: AgentState):
    queries = model.with_structured_output(Queries).invoke([
        SystemMessage(content=RESEARCH_PLAN_PROMPT),
        HumanMessage(content=state['task'])
    ])
    content = state['content'] or []  # add to content
    for q in queries.queries:
        response = tavily.search(query=q, max_results=2)
        for r in response['results']:
            content.append(r['content'])
    return {"content": content,
            "queries": queries.queries,
           "lnode": "research_plan",
            "steps": 1,
           }


# In[ ]:


def generation_node(state: AgentState):
    content = "\n\n".join(state['content'] or [])
    user_message = HumanMessage(
        content=f"{state['task']}\n\nHere is my plan:\n\n{state['plan']}")
    messages = [
        SystemMessage(
            content=WRITER_PROMPT.format(content=content)
        ),
        user_message
        ]
    response = model.invoke(messages)
    return {
        "draft": response.content, 
        "revision_number": state.get("revision_number", 1) + 1,
        "lnode": "generate",
        "steps": 1,
    }


# In[ ]:


def reflection_node(state: AgentState):
    messages = [
        SystemMessage(content=REFLECTION_PROMPT), 
        HumanMessage(content=state['draft'])
    ]
    response = model.invoke(messages)
    return {"critique": response.content,
           "lnode": "reflect",
            "steps": 1,
    }


# In[ ]:


def research_critique_node(state: AgentState):
    queries = model.with_structured_output(Queries).invoke([
        SystemMessage(content=RESEARCH_CRITIQUE_PROMPT),
        HumanMessage(content=state['critique'])
    ])
    content = state['content'] or []
    for q in queries.queries:
        response = tavily.search(query=q, max_results=2)
        for r in response['results']:
            content.append(r['content'])
    return {"content": content,
           "lnode": "research_critique",
            "steps": 1,
    }


# In[ ]:


def should_continue(state):
    if state["revision_number"] > state["max_revisions"]:
        return END
    return "reflect"


# In[ ]:


builder = StateGraph(AgentState)


# In[ ]:


builder.add_node("planner", plan_node)
builder.add_node("generate", generation_node)
builder.add_node("reflect", reflection_node)
builder.add_node("research_plan", research_plan_node)
builder.add_node("research_critique", research_critique_node)


# In[ ]:


builder.set_entry_point("planner")


# In[ ]:


builder.add_conditional_edges(
    "generate", 
    should_continue, 
    {END: END, "reflect": "reflect"}
)


# In[ ]:


builder.add_edge("planner", "research_plan")
builder.add_edge("research_plan", "generate")

builder.add_edge("reflect", "research_critique")
builder.add_edge("research_critique", "generate")


# In[ ]:


# import sqlite3
# conn_string = ":memory:"
# memory = SqliteSaver(conn=sqlite3.connect(conn_string, check_same_thread=False))
# graph = builder.compile(checkpointer=memory)
#graph = builder.compile()


# In[ ]:


def get_disp_state():
    current_state = graph.get_state(thread)
    lnode = current_state.values["lnode"]
    asteps = current_state.values["steps"]
    rev = current_state.values["revision_number"]
    nnode = current_state.next
    #step = steps[thread_id]
    print  (lnode,nnode,thread_id,rev,asteps)
    return lnode,nnode,thread_id,rev,asteps


partial_message = "" #global to hold state 
response = {}
max_steps = 10
steps = []
threads = []
def run_agent(start,topic,stop_after):
    global partial_message, thread_id,thread
    global response, max_steps, steps, threads
    if start:
        steps.append(0)
        config = {'task': topic,"max_revisions": 2,"revision_number": 0} 
        thread_id += 1  # new agent, new thread
        threads.append(thread_id)
    else:
        config = None
    thread = {"configurable": {"thread_id": str(thread_id)}}
    while steps[thread_id] < max_steps:
        response = graph.invoke(config, thread)
        steps[thread_id] += 1
        partial_message += str(response)
        partial_message += f"\n------------------\n\n"
        lnode,nnode,_,rev,asteps = get_disp_state()
        yield partial_message,lnode,nnode,thread_id,rev,asteps
        config = None #need
        if not nnode:  
            print("Hit the end")
            return
        if lnode in stop_after:
            print(f"stopping due to stop_after {lnode}")
            return
        else:
            print(f"Not stopping on lnode {lnode}")
    return



# In[ ]:


#dict_keys(['__start__', 'planner', 'generate', 'reflect', 'research_plan', 'research_critique'])
import sqlite3
conn_string = ":memory:"
memory = SqliteSaver(conn=sqlite3.connect(conn_string, check_same_thread=False))
graph = builder.compile(
    checkpointer=memory,
    interrupt_after=['planner', 'generate', 'reflect', 'research_plan', 'research_critique']
)
thread_id = -1
thread = {"configurable": {"thread_id": str(thread_id)}}

import gradio as gr
import time

def get_state(key):
    current_values = graph.get_state(thread)
    if key in current_values.values:
        lnode,nnode,thread_id,rev,astep = get_disp_state()
        new_label = f"last_node: {lnode}, thread_id: {thread_id}, rev: {rev}, step: {astep}"
        return gr.update(label=new_label, value=current_values.values[key])
    else:
        return ""  

def get_content():
    current_values = graph.get_state(thread)
    if "content" in current_values.values:
        content = current_values.values["content"]
        lnode,nnode,thread_id,rev,astep = get_disp_state()
        new_label = f"last_node: {lnode}, thread_id: {thread_id}, rev: {rev}, step: {astep}"
        return gr.update(label=new_label, value="\n\n".join(item for item in content) + "\n\n")
    else:
        return ""  

def update_pd():
    return gr.Dropdown(label="choose thread", choices=threads, value=thread_id,interactive=True)

def switch_state(new_tid):
    global thread, thread_id
    #print(f"switch_state{new_tid}")
    thread = {"configurable": {"thread_id": str(new_tid)}}
    thread_id = new_tid
    return get_disp_state()

def modify_state(key,asnode,new_state):
    print(f"modify_state: {key}\n{new_state}")
    current_values = graph.get_state(thread)
    print(f"modify_state before: {key}\n{current_values.values[key]}")
    current_values.values[key] = new_state
    graph.update_state(thread, current_values.values,as_node=asnode)
    print(f"modify_state: {key}\n{current_values.values[key]}")
    return

with gr.Blocks(theme=gr.themes.Default(spacing_size='sm',text_size="sm")) as demo:
    with gr.Tab("Agent"):
        with gr.Row():
            topic = gr.Textbox(label="Essay Topic", value="Pizza Shop")
            write_btn = gr.Button("Generate Essay", scale=0,min_width=80)
            cont_btn = gr.Button("Continue Essay", scale=0,min_width=80)
        checks = ["plan", "research_plan", "generate", "reflect", "research_critique"]
        stop_after = gr.CheckboxGroup(checks,label="Stop After State", value=checks)
        with gr.Row():
            lnode = gr.Textbox(label="last node", min_width=100)
            nnode = gr.Textbox(label="next node", min_width=100)
            threadid = gr.Textbox(label="Thread", scale=0, min_width=80)
            revision = gr.Textbox(label="Draft Rev", scale=0, min_width=80)
            stepsbox = gr.Textbox(label="steps", scale=0, min_width=80)
        with gr.Accordion("Edit State", open=False):
            with gr.Row():
                thread_pd = gr.Dropdown(choices=threads,interactive=True, label="select thread")
                thread_pd.change(switch_state, [thread_pd], [lnode,nnode,threadid,revision,stepsbox])
        live = gr.Textbox(label="Live Agent Output", lines=5)
        write_btn.click(fn=run_agent, inputs=[gr.Number(True, visible=False),topic,stop_after], 
                        outputs=[live,lnode,nnode,threadid,revision,stepsbox]).then(
                        fn=update_pd, inputs=None, outputs=[thread_pd]) #rewriting thread_pulldown also kicks off update to same outputs..
        cont_btn.click(fn=run_agent, inputs=[gr.Number(False, visible=False),topic,stop_after], 
                       outputs=[live,lnode,nnode,threadid,revision,stepsbox])
    with gr.Tab("Plan"):
        with gr.Row():
            refresh_btn = gr.Button("Refresh")
            modify_btn = gr.Button("Modify")
        plan = gr.Textbox(label="Plan", lines=10, interactive=True)
        refresh_btn.click(fn=get_state, inputs=gr.Number("plan", visible=False), outputs=plan)
        modify_btn.click(fn=modify_state, inputs=[gr.Number("plan", visible=False),
                                                  gr.Number("planner", visible=False), 
                                                  plan], outputs=None)
    with gr.Tab("Research Content"):
        refresh_btn = gr.Button("Refresh")
        content = gr.Textbox(label="content", lines=10)
        refresh_btn.click(fn=get_content, inputs=None, outputs=content)
    with gr.Tab("Draft"):
        with gr.Row():
            refresh_btn = gr.Button("Refresh")
            modify_btn = gr.Button("Modify")
        draft = gr.Textbox(label="draft", lines=10, interactive=True)
        refresh_btn.click(fn=get_state, inputs=gr.Number("draft", visible=False), outputs=draft)
        modify_btn.click(fn=modify_state, inputs=[gr.Number("draft", visible=False),
                                                  gr.Number("generate", visible=False), 
                                                  draft], outputs=None)
    with gr.Tab("Critique"):
        with gr.Row():
            refresh_btn = gr.Button("Refresh")
            modify_btn = gr.Button("Modify")
        critique = gr.Textbox(label="Critique", lines=10, interactive=True)
        refresh_btn.click(fn=get_state, inputs=gr.Number("critique", visible=False), outputs=critique)
        modify_btn.click(fn=modify_state, inputs=[gr.Number("critique", visible=False),
                                                  gr.Number("reflect", visible=False), 
                                                  critique], outputs=None)
demo.launch()


# In[ ]:


#12345678901234567890123456789012345678901234567890123456789012345678912


# In[ ]:


thread


# In[ ]:


threads


# In[ ]:


graph.nodes.keys()


# In[ ]:


graph.get_state(thread).values


# In[ ]:


current_values = graph.get_state(thread)
current_values.values['plan']



# In[ ]:


astring = ""
for item in alist:
    astring += item + "\n\n"


# In[ ]:


print(astring)


# In[ ]:


print(current_values.values["plan"])


# In[ ]:


dict_keys(['task', 'plan', 'draft', 'critique', 'content', 'revision_number', 'max_revisions'])


# In[ ]:


graph.nodes.keys()


# In[ ]:


graph.get_state(thread).next


# In[ ]:


hist = list(graph.get_state_history(thread))
hist[0].config


# In[ ]:


list(graph.get_state_history(thread))[2]


# In[ ]:


stop_after[0]


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





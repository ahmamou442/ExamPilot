import json
from app.core.config import API_KEY, MODEL
async def structured_agent(name,instructions,output_type,input_text):
    if not API_KEY: return None
    from agents import Agent, Runner
    agent=Agent(name=name,instructions=instructions,model=MODEL,output_type=output_type)
    result=await Runner.run(agent,input_text)
    return result.final_output

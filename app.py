import streamlit as st
from anthropic import AsyncAnthropic
import json
from typing import List, Dict
import asyncio
import time
from datetime import datetime
import re

def clean_text_for_json(text: str) -> str:
    """Clean text to make it JSON-compatible"""
    # Remove control characters
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
    
    # Handle escaped characters
    text = text.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
    
    # Remove any potential Unicode issues
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    return text

class Agent:
    def __init__(self, name: str, role: str, client: AsyncAnthropic):
        self.name = name
        self.role = role
        self.client = client
        self.conversation_history = []
    
    def get_system_prompt(self) -> str:
        return f"""You are {self.name}, a {self.role}. 
        Work collaboratively with other agents to solve tasks.
        Your response must be only a valid JSON string in this exact format, with no additional text or formatting:
        {{"thoughts": "your analytical process", "response": "your actual response"}}
        Keep all newlines and special characters properly escaped in your JSON."""
    
    async def process(self, input_text: str) -> Dict:
        try:
            message = await self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": f"Task input: {input_text}\n\nProvide your response as a single JSON object with 'thoughts' and 'response' fields only. No other text or formatting."
                }],
                system=self.get_system_prompt(),
                temperature=0.7
            )
            
            # Get the response text and clean it
            response_text = message.content[0].text.strip()
            
            # Try to extract JSON if it's wrapped in other text
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                response_text = json_match.group(0)
            
            # Clean the text for JSON parsing
            cleaned_text = clean_text_for_json(response_text)
            
            try:
                # Try to parse the cleaned JSON
                response_json = json.loads(cleaned_text)
            except json.JSONDecodeError:
                # If JSON parsing fails, create a structured response from the text
                response_json = {
                    "thoughts": "Processed the input and structured the response",
                    "response": cleaned_text
                }

            # Clean the values in the response
            response_json["thoughts"] = clean_text_for_json(str(response_json.get("thoughts", "")))
            response_json["response"] = clean_text_for_json(str(response_json.get("response", "")))

            self.conversation_history.append({
                "role": self.name,
                "content": response_json["response"]
            })
            
            return response_json

        except Exception as e:
            st.error(f"Processing error: {str(e)}")
            # Create a safe fallback response
            return {
                "thoughts": "Error occurred during processing",
                "response": f"I encountered an error while processing the input: {str(e)}. Please try rephrasing your request."
            }

class MultiAgentSystem:
    def __init__(self, api_key: str):
        self.client = AsyncAnthropic(api_key=api_key)
        self.agents = {
            "researcher": Agent("Researcher", "research and data analysis expert", self.client),
            "writer": Agent("Writer", "content creation expert", self.client),
            "critic": Agent("Critic", "quality control expert", self.client)
        }
    
    async def run_workflow(self, task: str) -> List[Dict]:
        results = []
        
        with st.status("Running workflow...", expanded=True) as status:
            try:
                # Research phase
                status.write("🔍 Researcher agent is analyzing the task...")
                research_result = await self.agents["researcher"].process(
                    f"Analyze this topic and provide key points: {task}"
                )
                results.append({"agent": "researcher", "output": research_result})
                
                # Writing phase
                status.write("✍️ Writer agent is creating content...")
                write_result = await self.agents["writer"].process(
                    f"Using these research points: {research_result['response']}\nCreate a well-structured explanation of: {task}"
                )
                results.append({"agent": "writer", "output": write_result})
                
                # Review phase
                status.write("📝 Critic agent is reviewing the content...")
                review_result = await self.agents["critic"].process(
                    f"Review this explanation of {task}:\n{write_result['response']}\nProvide specific feedback and suggestions."
                )
                results.append({"agent": "critic", "output": review_result})
                
                status.update(label="Workflow completed!", state="complete")
            
            except Exception as e:
                status.update(label=f"Error: {str(e)}", state="error")
                st.error(f"Workflow error: {str(e)}")
                return []
        
        return results

def create_agent_card(agent_name: str, thoughts: str, response: str):
    with st.container():
        st.subheader(f"🤖 {agent_name}")
        with st.expander("Show agent's thoughts", expanded=True):
            st.write("💭 **Thoughts:**")
            st.write(thoughts)
        st.write("📄 **Response:**")
        st.write(response)
        st.divider()

async def main():
    st.set_page_config(
        page_title="Multi-Agent System",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🤖 Multi-Agent Collaboration System")
    st.markdown("""
    This system demonstrates collaboration between three AI agents:
    - 🔍 **Researcher**: Analyzes tasks and provides key information
    - ✍️ **Writer**: Creates content based on research findings
    - 📝 **Critic**: Reviews and provides feedback on the content
    """)
    
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("Enter Anthropic API Key:", type="password")
        st.divider()
        st.markdown("""
        ### How it works
        1. Enter your API key
        2. Input your task
        3. Watch the agents collaborate
        4. Review the results
        """)
    
    if not api_key:
        st.warning("Please enter your Anthropic API key in the sidebar to continue.")
        return
    
    system = MultiAgentSystem(api_key)
    
    task = st.text_area(
        "Enter your task:",
        placeholder="e.g., Explain the theory of relativity",
        height=100
    )
    
    if st.button("Run Workflow", type="primary"):
        if not task:
            st.error("Please enter a task.")
            return
        
        try:
            with st.spinner("Processing your request..."):
                results = await system.run_workflow(task)
            
            if results:
                st.header("Results")
                for result in results:
                    create_agent_card(
                        result["agent"].title(),
                        result["output"]["thoughts"],
                        result["output"]["response"]
                    )
                    
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error("Please check your API key and try again.")

if __name__ == "__main__":
    asyncio.run(main())
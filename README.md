# Multi-Agent-Application-

> Harness the power of collaborative AI agents for enhanced content creation and analysis

## 🌟 Overview
It is an innovative multi-agent LLM application that leverages three specialized AI agents working in harmony: a Researcher, Writer, and Critic. The system orchestrates these agents to produce comprehensive, well-researched content through a collaborative workflow. The Researcher analyzes and gathers key information, the Writer transforms this research into coherent content, and the Critic provides quality control and refinement suggestions. Built with the Claude API and Streamlit, this application offers a user-friendly interface for tasks ranging from content creation to complex analysis, demonstrating the power of specialized AI collaboration over single-LLM solutions.

### Why Multi-Agent Architecture Matters
- 🔍 **Specialized Expertise**: Each agent focuses on its core competency, leading to better results than a one-size-fits-all approach
- 🤝 **Collaborative Intelligence**: Agents build upon each other's work, creating a workflow similar to human team collaboration
- 🔄 **Built-in Review Process**: The Critic agent provides automatic quality control and refinement suggestions
- 📈 **Iterative Improvement**: The multi-stage process allows for continuous refinement of content
- 💡 **Diverse Perspectives**: Multiple agents approach the task from different angles, ensuring comprehensive coverage

## 🚀 Features
- Three specialized AI agents working in harmony:
  - 📚 **Researcher**: Analyzes topics and gathers key information
  - ✍️ **Writer**: Crafts coherent and engaging content
  - 🎯 **Critic**: Reviews and provides constructive feedback
- Real-time workflow visualization
- Clean, intuitive Streamlit interface
- Secure API key management
- Extensible architecture for adding new agents

## 🛠️ Installation

1. Clone the repository:


2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

1. Get your API key from [Anthropic](https://www.anthropic.com/)

2. Start the application:
```bash
streamlit run src/app.py
```

3. Enter your API key in the sidebar
4. Input your task and watch the agents collaborate!

## 📊 Example Use Cases

1. **Content Creation**
   - Research papers
   - Blog posts
   - Technical documentation
   - Educational content

2. **Analysis & Review**
   - Literature review
   - Data analysis reports
   - Code review
   - Project proposals

3. **Educational Support**
   - Lesson planning
   - Study guide creation
   - Complex topic explanation
   - Quiz generation


## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## ✨ Acknowledgments

- Built with [Anthropic's Claude API](https://www.anthropic.com/)
- UI powered by [Streamlit](https://streamlit.io/)

---


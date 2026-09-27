# 🤖 AI Engineer Learning Journey

Complete learning path for becoming an AI Engineer, covering LLMs, RAG systems, agents, and production deployment.

## 📚 Course Structure

### Week 1: LLM Fundamentals
- **Day 1**: Hello LLM - First API call and basic setup
- **Day 2**: System Prompts - Controlling LLM behavior
- **Day 3**: Tokens & Tokenization - Understanding LLM inputs
- **Day 4**: JSON Mode & Pydantic - Structured outputs
- **Day 5**: Resume Parser - First practical project

### Week 2: Prompt Engineering & Chains
- **Day 6**: Advanced Prompt Engineering techniques
- **Day 7**: ReAct Agents - Reasoning and Acting
- **Day 8**: LLM Chains - Sequential processing
- **Day 9**: Streaming Responses - Real-time outputs

### Week 3: RAG (Retrieval Augmented Generation)
- **Day 11**: Basic RAG - Simple retrieval system
- **Day 12**: Embeddings - Vector representations
- **Day 13**: Full RAG Pipeline - Complete implementation
- **Day 14**: Qdrant Vector Database - Cloud storage
- **Day 15**: Advanced Qdrant - Filtering & metadata

### Week 4: Production & Advanced Topics
- **Day 16**: Text Chunking Strategies - Handling long documents
- **Day 18**: Tool-Calling Agents - Web search & calculations

## 🚀 Quick Start

Each day's folder contains:
- `main.py` or specific implementation files
- `EXPLANATION.md` - Comprehensive documentation (700-1000 lines)
- `README.md` - Quick overview
- `pyproject.toml` - Dependencies

### Installation

```bash
# Clone the repository
git clone https://github.com/Vaibhu79/Learning_Ai.git
cd Learning_Ai

# Navigate to specific day
cd week1/day1

# Install dependencies (using uv)
uv sync

# Or using pip
pip install -r requirements.txt

# Run the code
python main.py
```

## 🔑 API Keys Required

Most projects require API keys. Create a `.env` file in each day's folder:

```bash
# Groq (LLM API)
GROQ_API_KEY=your_groq_key_here

# Qdrant (Vector Database - Days 14-15)
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_key

# Tavily (Web Search - Day 18)
TAVILY_API_KEY=your_tavily_key
```

Get your API keys:
- **Groq**: https://console.groq.com/keys
- **Qdrant**: https://cloud.qdrant.io/
- **Tavily**: https://tavily.com/

## 📖 Documentation

Each day includes comprehensive documentation in Hinglish (Hindi + English) covering:
- Big picture overview
- Real-life analogies
- Line-by-line code explanation
- Common confusions & mistakes
- Mental models & takeaways

## 🛠️ Tech Stack

- **Python 3.11+**
- **LLM**: Groq API (Llama models)
- **Embeddings**: SentenceTransformers
- **Vector DB**: Qdrant
- **Frameworks**: LangChain, Pydantic
- **Tools**: uv (package manager)

## 📈 Learning Path

```
Week 1: Fundamentals → Week 2: Engineering → Week 3: RAG → Week 4: Production
```

## 🤝 Contributing

This is a learning repository. Feel free to:
- Report issues
- Suggest improvements
- Share your learning journey

## 📝 Notes

- All code is educational and documented for beginners
- Some bugs are intentionally kept in code with documentation explaining them
- Focus is on understanding concepts, not production-perfect code

## 📧 Contact

GitHub: [@Vaibhu79](https://github.com/Vaibhu79)

---

**Happy Learning! 🎓**

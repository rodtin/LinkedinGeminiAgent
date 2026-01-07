import os
import datetime
from tavily import TavilyClient
import google.generativeai as genai

# Configuration
TAVILY_KEY = os.getenv("TAVILY_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def run_daily_search(topics: list[str]) -> str:
    """
    Performs a search and analysis for the given topics.
    Returns the path to the generated markdown file.
    """
    if not TAVILY_KEY or not GEMINI_KEY:
        raise ValueError("Missing API Keys for Tavily or Gemini")

    topic_str = ", ".join(topics)
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    # 1. Search
    tavily = TavilyClient(api_key=TAVILY_KEY)
    print(f"Searching for: {topic_str}")
    search_result = tavily.search(query=f"latest important news and trends in {topic_str}", search_depth="advanced", max_results=10)
    
    # Format context for LLM
    context = ""
    for result in search_result.get('results', []):
        context += f"- Title: {result['title']}\n  URL: {result['url']}\n  Snippet: {result['content']}\n\n"

    # 2. Analysis (Prompt ported from news-agent.toml)
    from Automation.llm_wrapper import generate_llm_response
    
    prompt = f"""
    You are a Lead Strategic Intelligence Analyst. Your goal is to provide a 360-degree "Deep Dive" on the current top 5 today's news stories related to: {topic_str}.
    
    **Instructions:**
    1. **Analyze:** Using the provided search results below, select the top 5 most critical and recent stories.
    2. **Lenses:** For EACH of the top 5 stories, analyze it using **all 6 analytical lenses**.
    
    Required Output Format (Markdown):
    
    ---
    ### [Number]. [Headline]
    **The News:**
    [Concise factual summary, approx 10 sentences]

    **360° Analysis:**
    * 🟢 **Sentiment:** [Overall mood + Primary Driver]
    * ⚖️ **The Skeptic (Hype vs. Reality):** [Technical reality vs marketing claim]
    * 🔮 **The Futurist (Order 2 Effects):** [Ripple effect 3-5 years]
    * 🏆 **The Strategist (Winners/Losers):** [Who benefits/loses]
    * 💰 **The Investor (The Money):** [ROI thesis/transaction logic]
    * 🎓 **The Educator (ELI5):** [Simple analogy]

    **Sources:**
    * [Source Name](URL) -> MUST match exactly from the provided context.

    **Search Data Context:**
    {context}
    
    **Additional Rules:**
    - Provide an "Executive Synthesis" at the very beginning.
    - Use the exact URLs from the search data.
    """
    
    report_content = generate_llm_response(prompt)
    
    # 3. Save to File
    base_dir = f"News Agent/News/{today}"
    os.makedirs(base_dir, exist_ok=True)
    
    # Conflict resolution for filename
    base_name = f"News_{topic_str.replace(' ', '_')}"
    item_path = os.path.join(base_dir, f"{base_name}.md")
    counter = 1
    while os.path.exists(item_path):
        item_path = os.path.join(base_dir, f"{base_name}_{counter}.md")
        counter += 1
        
    with open(item_path, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    return item_path

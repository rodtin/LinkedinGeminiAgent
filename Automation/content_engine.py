import os
import datetime
import google.generativeai as genai

# Configuration
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def generate_draft(report_path: str, selection: str, mode: str = "persona", lens: str = "all") -> str:
    """
    Generates a LinkedIn draft based on a report and user selection.
    
    Args:
        report_path: Path to the MD news report.
        selection: The user's input (e.g., "Story 1" or "Cloud RAN").
        mode: "persona" (Rodrigo Tinte) or "direct" (Neutral).
        lens: Specific lens to focus on (default "all").
    """
    if not GEMINI_KEY:
        raise ValueError("Missing Gemini API Key")
        
    with open(report_path, "r", encoding="utf-8") as f:
        report_content = f.read()

    # Load Voice if needed
    persona_context = ""
    if mode == "persona":
        try:
            with open("News Agent/Setup/my-voice.md", "r", encoding="utf-8") as f:
                persona_context = f.read()
        except FileNotFoundError:
            persona_context = "Persona file not found. Use a professional, technical, yet personal tone (80/20)."

    from Automation.llm_wrapper import generate_llm_response
    
    # Construct Prompt
    prompt = f"""
    You are expert content creator.
    **Task:** Create a LinkedIn post based on the report below, focusing on the user's selection: "{selection}".
    
    **News Report Content:**
    {report_content[:15000]} 
    
    **Instructions:**
    1. Extract technical details about "{selection}" from the report.
    2. **Mode:** {mode.upper()}
       - IF "PERSONA": {persona_context}
       - IF "DIRECT": Write a professional, punchy summary without personal anecdotes. Just the facts and the insight.
    3. **Lens:** {lens}
       - If "all", use the general insights.
       - If a specific lens (e.g., "Strategist"), output ONLY that perspective but formatted as a post.
       
    4. **Structure:**
       - Hook (No "Hello team")
       - Insight/Body (2-3 sentences)
       - Conclusion
       - Hashtags
       - **Source Links**: Include exact URLs found in the report.
       
    Output ONLY the markdown content of the post.
    """
    
    post_content = generate_llm_response(prompt)
    
    # Save
    today = datetime.date.today().strftime("%Y-%m-%d")
    base_dir = f"News Agent/Posts/{today}"
    os.makedirs(base_dir, exist_ok=True)
    
    # Conflict resolution
    safe_topic = "".join(x for x in selection if x.isalnum() or x in " -_")[:20]
    base_name = f"LinkedIn_Draft_{safe_topic}"
    item_path = os.path.join(base_dir, f"{base_name}.md")
    
    counter = 1
    while os.path.exists(item_path):
        item_path = os.path.join(base_dir, f"{base_name}_{counter}.md")
        counter += 1
        
    with open(item_path, "w", encoding="utf-8") as f:
        f.write(post_content)
        
    return item_path, post_content

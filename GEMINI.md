# Gemini News Agent Workspace

## Project Overview
This directory contains the configuration and workspace for a **Telecom News & Content Automation Agent**. It is designed to leverage Gemini's capabilities to research specific telecommunications topics, analyze them through multiple strategic lenses, and generate professional LinkedIn posts in the specific voice of "Rodrigo Tinte".

## Directory Structure

### 📂 `.gemini/commands/`
Contains the command definitions that power the agent's specific workflows.
*   **`news-agent.toml`**: Defines the `news-agent` command. This command performs a "Deep Dive" 360° analysis on a given topic (e.g., "5G", "Open RAN"). It searches trusted sources, analyzes the top 5 stories using 6 distinct lenses (Sentiment, Skeptic, Futurist, Strategist, Investor, Educator), and saves a report to `News Agent/News/`.
*   **`linkedin-prepare.toml`**: Defines the `linkedin-prepare` command. This command takes a specific topic, reads the latest news report from `News Agent/News/`, and drafts a LinkedIn post adhering to the persona defined in `my-voice.md`. The result is saved to `News Agent/Posts/`.
*   **`linkedin-post.toml`**: Defines the `linkedin-post` command. This command automates the publishing of the latest post draft to LinkedIn using the Python script in `Application/`.

### 📂 `News Agent/`
The main working directory for the agent's output and configuration.

#### `Setup/`
Configuration files that control the behavior and style of the agent.
*   **`my-voice.md`**: **CRITICAL**. Defines the "Rodrigo Tinte" persona. It includes tone settings (Professional/Personal balance), structural blueprints for posts, and "Few-Shot" examples to ensure the AI mimics the user's specific writing style (technical, optimistic, team-focused).
*   **`urls.md`**: A whitelist of trusted telecommunications news sources (e.g., BNamericas, Ericsson Newsroom, IEEE, Anatel) to ensure high-quality, relevant research.

#### `News/`
*   **Output Directory**: Stores the generated Markdown reports from the `news-agent` command (e.g., `Top_5_5G_News_2026-01-01.md`).

#### `Posts/`
*   **Output Directory**: Stores the generated LinkedIn post drafts from the `linkedin-prepare` command (e.g., `LinkedIn_Post_5G_2026-01-01.md`). Successfully published posts are renamed with a `POSTED_` prefix.

### 📂 `Application/`
Contains the Python application for LinkedIn API integration.
*   **`post_linkedin.py`**: The script that handles the API request to publish a post. It renames the file upon success.
*   **`.env`**: (Ignored by Git) Stores sensitive credentials (`LINKEDIN_ACCESS_TOKEN`, `LINKEDIN_URN_ID`).
*   **`pyproject.toml`**: Manages dependencies (`requests`, `python-dotenv`) using `uv`.

## Usage

### 1. Research & Analysis
To generate a deep dive report on a specific topic:
*   **Command:** Invoke the `news-agent` capability with a topic.
*   **Example Input:** "Run the news-agent command for 'Cloud RAN'."
*   **Output:** A file in `News Agent/News/` containing a detailed 360° analysis of the top 5 news stories.

### 2. Content Creation
To draft a LinkedIn post based on previous research:
*   **Command:** Invoke the `linkedin-prepare` capability with a specific sub-topic found in the report.
*   **Example Input:** "Prepare a LinkedIn post about 'Ericsson Cloud RAN' using the latest report."
*   **Output:** A file in `News Agent/Posts/` containing a ready-to-post draft that matches the defined persona.

### 3. Publishing
To publish the latest draft to your LinkedIn profile:
*   **Command:** Invoke the `linkedin-post` capability.
*   **Example Input:** "Run linkedin-post."
*   **Action:** The agent executes the Python script, publishes the post, and renames the file to mark it as `POSTED_`.

## Configuration & Setup
*   **Credentials:** Ensure `Application/.env` contains your valid `LINKEDIN_ACCESS_TOKEN` and `LINKEDIN_URN_ID`.
*   **Dependencies:** The application uses `uv`. Run `uv sync` in the `Application/` folder to install dependencies.
*   **Adding Sources:** Edit `News Agent/Setup/urls.md` to add new trusted websites.
*   **Refining Voice:** Edit `News Agent/Setup/my-voice.md` to update the persona's tone.
# LinkedIn Gemini Agent (Telecom & Cloud Automation)

## Project Overview
This repository contains a specialized AI agent designed to automate the lifecycle of professional LinkedIn content for the Telecommunications and Cloud sector. It leverages Gemini to research industry topics, analyze them through strategic lenses, and generate posts in the specific technical voice of "Rodrigo Tinte".

## Directory Structure

### 📂 `.gemini/commands/`
Custom agent capabilities:
*   **`news-agent.toml`**: Performs 360° "Deep Dive" research on telecom topics.
*   **`linkedin-prepare.toml`**: Drafts LinkedIn posts based on research reports.
*   **`linkedin-post.toml`**: Automates the final publishing to LinkedIn.

### 📂 `News Agent/`
The primary workspace:
*   **`Setup/`**: Contains the `my-voice.md` persona definition and `urls.md` trusted sources.
*   **`News/`**: Stores generated technical reports.
*   **`Posts/`**: Stores drafted and published (`POSTED_`) LinkedIn content.

### 📂 `Application/`
Automated publishing layer:
*   **`post_linkedin.py`**: Python script for LinkedIn API integration.
*   **`pyproject.toml`**: Dependency management via `uv`.

## Usage

### 1. Research
Invoke the `news-agent` capability:
> "Run the news-agent command for '5G-Advanced'."

### 2. Prepare Post
Invoke the `linkedin-prepare` capability:
> "Prepare a LinkedIn post about '3GPP Release 18' using the latest report."

### 3. Publish
Invoke the `linkedin-post` capability:
> "Run linkedin-post."

## Setup
1.  Configure credentials in `Application/.env` (see `post_linkedin.py` for variables).
2.  Install dependencies: `cd Application && uv sync`.
3.  Customize your voice in `News Agent/Setup/my-voice.md`.
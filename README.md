# Naturalborne Streamlit AnythingLLM UI

A Streamlit-native frontend for your Naturalborne AnythingLLM workspace.

## What it does
- accepts your AnythingLLM base URL, workspace slug, and API key in the UI
- sends chat requests to your AnythingLLM workspace
- gives you response modes, suggested prompts, export chat, and a cleaner modern layout

## Run
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Fields
- Base URL: example `http://127.0.0.1:8001`
- Workspace Slug: your Naturalborne workspace slug
- API Key: your AnythingLLM API key
- Chat Path: defaults to `/api/v1/workspace/{workspace_slug}/chat`

## Important
If you later deploy this Streamlit app remotely, a local Docker URL like `127.0.0.1:8001` will only work if that deployed app can actually reach your machine.

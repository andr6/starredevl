CATEGORIES = ["Cyber Security", "Coding", "Machine Learning", "IT", "Network", "Others"]


def categorize(
    description: str,
    topics: list[str],
    api_key: str,
    model: str = "gpt-3.5-turbo",
    provider: str = "openai",
) -> str:
    """Categorize a repository using a selected LLM provider.

    Parameters
    ----------
    description : str
        Repository description.
    topics : list[str]
        Topics of the repository.
    api_key : str
        API key for the provider. If empty, ``Others`` will be returned.
    model : str, optional
        Model name to use when querying the provider.
    provider : str, optional
        Provider of the LLM. Supported values are ``openai``, ``groq`` and
        ``ollama``.
    """
    if not api_key and provider != "ollama":
        return "Others"

    try:
        import openai
    except Exception:
        return "Others"

    if provider == "groq":
        openai.base_url = "https://api.groq.com/openai/v1"
        openai.api_key = api_key
    elif provider == "ollama":
        openai.base_url = "http://localhost:11434/v1"
        # Ollama may not require an API key
        openai.api_key = api_key or "ollama"
    else:
        openai.base_url = None
        openai.api_key = api_key
    prompt = (
        "Select one category from "
        f"{', '.join(CATEGORIES)} for a GitHub repository "
        f"with description '{description}' and topics {topics}. "
        "Respond with only the category name."
    )
    try:
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=5,
            temperature=0,
        )
        cat = resp["choices"][0]["message"]["content"].strip()
    except Exception:
        cat = "Others"

    if cat not in CATEGORIES:
        cat = "Others"

    return cat

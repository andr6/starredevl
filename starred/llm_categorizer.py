CATEGORIES = ["Cyber Security", "Coding", "Machine Learning", "IT", "Network", "Others"]

# Enhanced category descriptions to help LLM understand project goals
CATEGORY_DESCRIPTIONS = {
    "Cyber Security": "Security tools, penetration testing, vulnerability scanning, cryptography, authentication, threat detection, security frameworks, exploit tools",
    "Coding": "Development tools, code editors, programming languages, frameworks, libraries, build tools, version control, CLI tools, debugging, testing frameworks",
    "Machine Learning": "AI/ML models, neural networks, data science, deep learning, NLP, computer vision, ML frameworks, data analytics, model training",
    "IT": "System administration, DevOps, infrastructure, cloud platforms, containers, orchestration, monitoring, logging, automation, configuration management",
    "Network": "Networking tools, protocols, SDN, network security, packet analysis, DNS, load balancing, network monitoring, VPN, routing",
    "Others": "Projects that don't fit the above categories, general utilities, documentation, learning resources"
}


def categorize(
    description: str,
    topics: list[str],
    api_key: str,
    model: str = "gpt-3.5-turbo",
    provider: str = "openai",
    repo_name: str = "",
    language: str = "",
    stargazer_count: int = 0,
) -> str:
    """Categorize a repository using a selected LLM provider with enhanced context.

    Parameters
    ----------
    description : str
        Repository description (full, not truncated).
    topics : list[str]
        Topics of the repository.
    api_key : str
        API key for the provider. If empty, ``Others`` will be returned.
    model : str, optional
        Model name to use when querying the provider.
    provider : str, optional
        Provider of the LLM. Supported values are ``openai``, ``groq`` and
        ``ollama``.
    repo_name : str, optional
        Repository name (often indicates purpose/goal).
    language : str, optional
        Primary programming language.
    stargazer_count : int, optional
        Number of stars (popularity indicator).
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

    # Build enhanced context for better categorization
    context_parts = []

    if repo_name:
        context_parts.append(f"Repository name: {repo_name}")

    if description:
        context_parts.append(f"Description: {description}")

    if topics:
        context_parts.append(f"Topics: {', '.join(topics)}")

    if language:
        context_parts.append(f"Primary language: {language}")

    if stargazer_count > 0:
        popularity = "highly popular" if stargazer_count > 10000 else "popular" if stargazer_count > 1000 else "moderately popular"
        context_parts.append(f"Popularity: {popularity} ({stargazer_count} stars)")

    context = "\n".join(context_parts)

    # Enhanced prompt with category descriptions and instruction to infer purpose
    category_guide = "\n".join([f"- {cat}: {desc}" for cat, desc in CATEGORY_DESCRIPTIONS.items()])

    prompt = f"""Analyze this GitHub repository and categorize it based on its primary purpose, objectives, and use case.

Repository Information:
{context}

Available Categories:
{category_guide}

Consider:
1. The project's main objective and goal (what problem does it solve?)
2. The intended audience (developers, security professionals, data scientists, etc.)
3. The primary use case (development tool, security analysis, ML model, infrastructure, etc.)
4. The repository name often hints at the purpose

Select the SINGLE most appropriate category from: {', '.join(CATEGORIES)}

Respond with ONLY the category name, nothing else."""

    try:
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0,
        )
        cat = resp["choices"][0]["message"]["content"].strip()
    except Exception:
        cat = "Others"

    if cat not in CATEGORIES:
        cat = "Others"

    return cat

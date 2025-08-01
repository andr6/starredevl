CATEGORIES = ["Cyber Security", "Coding", "Machine Learning", "IT", "Network", "Others"]


def categorize(description: str, topics: list[str], api_key: str) -> str:
    """Categorize a repository using OpenAI LLM.

    Parameters
    ----------
    description : str
        Repository description.
    topics : list[str]
        Topics of the repository.
    api_key : str
        OpenAI API key. If empty, ``Others`` will be returned.
    """
    if not api_key:
        return "Others"

    try:
        import openai
    except Exception:
        return "Others"

    openai.api_key = api_key
    prompt = (
        "Select one category from "
        f"{', '.join(CATEGORIES)} for a GitHub repository "
        f"with description '{description}' and topics {topics}. "
        "Respond with only the category name."
    )
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
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

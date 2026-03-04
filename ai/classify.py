import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def classify_release(description):
    prompt = f"""
    You are an AI that determines whether a product description is announcing a new card release.
    Description: "{description}"

    Respond in JSON with:
    - "is_release": true or false
    - "summary": a short summary of the release
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    text = response["choices"][0]["message"]["content"]

    # Basic safety fallback
    if "true" in text.lower():
        return {"is_release": True, "summary": description[:150]}
    else:
        return {"is_release": False, "summary": ""}

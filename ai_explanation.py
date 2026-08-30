import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


def explain_findings(summary):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "AI explanation is unavailable because GEMINI_API_KEY is not configured."

    try:
        client = genai.Client(api_key=api_key)

        prompt = (
            "You are a business analyst analyzing food-delivery operations. "
            "Explain the following calculated findings in 120 words or fewer. "
            "Use ONLY the provided calculated results. "
            "Do not invent statistics or facts. "
            "Focus on practical operational meaning for a food-delivery company. "
            "Write clearly and professionally.\n\n"
            "Calculated findings:\n"
            + summary
        )

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt,
        )

        if hasattr(interaction, "output_text") and interaction.output_text:
            return interaction.output_text.strip()

        return "AI generated an empty response."

    except Exception as exc:
        return "AI explanation could not be generated: " + str(exc)
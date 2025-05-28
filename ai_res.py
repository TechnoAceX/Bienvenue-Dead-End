from openai import OpenAI
import os
from keys import OPENAI_API_KEY as fallback_key

# Get API key from environment variable, else fallback to keys.py
api_key = os.getenv("OPENAI_API_KEY", fallback_key)


# Narrator styles
NARRATOR_STYLES = {
    "lostSoul": "A Lost Soul, desperate and emotional, first-person narrative",
    "ancientEntity": "An Ancient Entity, cryptic and omniscient third-person narrative",
    "childSpirit": "A Child Spirit, innocent yet eerie tone in first person",
    "unknownVoice": "The Unknown Voice, chaotic and unreliable in tone",
    "you": "Second-person perspective, the reader is the protagonist"
}

# Duration mapping
DURATION_TEXT = {
    "1": "Short (~5 minutes)",
    "2": "Medium (~10 minutes)",
    "3": "Long (~15+ minutes)"
}

client = OpenAI(api_key=api_key)  # Create OpenAI client instance

def generate_complete_story(name: str, blueprint: str, duration: str, protocol: str) -> str:
    narrator_style = NARRATOR_STYLES.get(protocol, "A mysterious narrator")
    duration_hint = DURATION_TEXT.get(duration, "Medium (~10 minutes)")

    prompt = f"""
You are an expert horror/thriller author.

Write a full horror story based on the following:
- Character name: {name}
- Setting/blueprint: {blueprint}
- Narrator style: {narrator_style}
- Estimated length: {duration_hint}

The story should have:
- A clear beginning, middle, and end.
- Suspenseful, thrilling, and scary moments fitting the horror genre.
- 2–3 key choices the character makes (narrate the consequences, don't break the flow).
- Two labeled endings:
    1. Horrifying Ending
    2. Hopeful Ending

Match tone and language to the chosen narrator style.

Start the story now.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a creative storyteller."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )

    return response.choices[0].message.content.strip()

def generate_image(prompt: str) -> str:
    # Dummy placeholder image URL
    return f"https://dummyimage.com/600x400/000/fff&text={prompt.replace(' ', '+')}"

if __name__ == "__main__":
    test_name = "Alex"
    test_blueprint = "A traveler lost in a storm, finds shelter in an old Victorian mansion."
    test_duration = "2"
    test_protocol = "lostSoul"

    story = generate_complete_story(test_name, test_blueprint, test_duration, test_protocol)
    print(story)

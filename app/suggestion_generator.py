from app.utils import resolve_path
from resources.prompts import get_prompt, distill_prompt

_client = None  # Global client object


def get_client():
    """Lazy initialization of the client."""

    global _client
    if _client is None:
        from dotenv import load_dotenv
        from openai import OpenAI
        import os
        # Get the absolute path to the .env file
        dotenv_path = resolve_path('.env.local')
        load_dotenv(dotenv_path=dotenv_path)
        open_api_key = os.getenv("OPENAI_API_KEY")
        _client = OpenAI(api_key=open_api_key)  # Replace with your client initialization logic
    return _client


def generate_concise_description(job_description):
    client = get_client()
    distilled_description = run_chat_completion(client, distill_prompt, job_description)
    #print(distilled_description.choices[0].message.content.strip())
    return distilled_description


def generate_replacements(resume_path, distilled_description, prompt):
    """Use ChatGPT to generate replacements for the resume."""
    client = get_client()

    # suggestment generator prompt and job description
    system_message = get_prompt(resume_path, prompt)

    user_message = f"""
    Job description:
    {distilled_description}
    """

    response = run_chat_completion(client, system_message, user_message)

    # Extract raw response content
    raw_response = response.choices[0].message.content.strip()
    print(raw_response)

    # Remove surrounding triple backticks and "json" if present
    if raw_response.startswith("```json"):
        clean_response = raw_response[7:].strip('```').strip()
    elif raw_response.startswith("```"):
        clean_response = raw_response.strip('```').strip()
    else:
        clean_response = raw_response

    # Evaluate the cleaned response
    return eval(clean_response)  # Convert JSON string to a Python list of dictionaries


def run_chat_completion(client,system_message, user_message):
    """Generic function to interact with OpenAI."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
    )
    return response


import os
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, request, jsonify

app = Flask(__name__)

class QuoteGenerator:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    def generate_quote(self, event_name: str, event_description: str, category: str, number: int):
        """Generate multiple inspirational quotes for a given category (using yield)."""
        for _ in range(number):
            prompt = f"""
                The name of the event is {event_name}, and the event description is: {event_description}.

                    Please provide a motivational quote to encourage, motivate the user and that must be highly relevant to the {category} category.

                    Strict guidelines to follow:

                    The quote must be high quality and precise.
                    The quote must include the author's name. If the quote is AI-generated, then do not show that it's AI-generated or unknown.
                    The quote must be inspirational, and relevant to {event_name}, {event_description}, and the {category} category.

                    Please ensure the output follows this exact JSON format:

                    {{
                    "event_name": "{event_name}",
                    "quote": "quote"
                    }}
                    Now, provide one valid, high-quality, and inspirational quote related to the {event_description} and the {category} category. 
                """
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4-turbo",  # gpt-4 turbo model
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that generates inspirational, motivational quotes."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=50,
                    temperature=1.5
                )
                yield response.choices[0].message.content.strip()
            except Exception as e:
                yield {"error": str(e)}


quote_generator = QuoteGenerator()

@app.route('/generate-quote', methods=['POST'])
def generate_quote():
    """API endpoint to generate motivational quotes"""
    data = request.get_json()

    event_name = data.get("event_name")
    event_description = data.get("event_description")
    category = data.get("category")
    number = data.get("number", 1)  

    
    if not event_name or not event_description or not category:
        return jsonify({"error": "Missing required parameters: event_name, event_description, or category"}), 400

    s
    quotes = []
    for quote in quote_generator.generate_quote(event_name, event_description, category, number):
        quotes.append(quote)

    return jsonify({"quotes": quotes})

if __name__ == "__main__":
    app.run(debug=True)

import os
from dotenv import load_dotenv
from openai import OpenAI

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

                    Please provide a motivational quote to encourage, motivate the user and that must be highly relevance to the {category} category.

                    Strict guidelines to follow:

                    The quote must be high quality a precise one.
                    The quote must not include the author's name. If the quote is AI-generated, then also do not show that is AI-generated or unkown or anything.
                    The quote must be inspirational, and relevant to {event_name}, {event_description}, and the {category} category.

                    Please ensure the output follows this exact JSON format:

                    {{
                    "event_name": "{event_name}",
                    "quote": "quote"
                    
                    }}
                    Now, provide one valid, high-quality, and inspirational quote related to the {event_description} and the {category} category . 
                """
            
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4-turbo", #gpt-4o gpt-4-turbo-2024-04-09
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that generates inspirational, ,motivational quotes both from author also by self generation."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=50,
                    temperature=1.5
                )
                yield response.choices[0].message.content.strip()
            except Exception as e:
                yield {"error": str(e)}


# Test 
if __name__ == "__main__":
    quote_generator = QuoteGenerator()
    event_name = "interview"
    event_description = "have a interview in a company have to crack the viva." #A challenging math exam covering algebra, calculus, and geometry have to grab all the team members update A challenging math exam covering algebra, calculus, and geometry. have a interview in a company have to crack the viva
    category = "career" #Brainstorming
    number = 2

    for quote in quote_generator.generate_quote(event_name,event_description, category, number):
        print(quote)
 
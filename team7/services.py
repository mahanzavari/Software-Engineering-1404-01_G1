import json
import logging
from django.conf import settings
from openai import OpenAI

logger = logging.getLogger(__name__)

class WritingEvaluator:
    def __init__(self):
        # Configure the client based on provided documentation
        self.client = OpenAI(
            api_key=getattr(settings, 'AI_GENERATOR_API_KEY', 'PLACEHOLDER_KEY'),
            base_url="https://api.gpt4-all.xyz/v1"
        )
        self.model = "gemini-3-flash-preview"

    def validate_length(self, text):
        """
        SRS Requirement: Minimum 50 words, Max 1000 words.
        """
        word_count = len(text.split())
        if word_count < 50:
            return False, "Text is too short (minimum 50 words)."
        if word_count > 1000:
            return False, "Text is too long (maximum 1000 words)."
        return True, "OK"

    def analyze(self, text, question_prompt, mode="independent"):
        """
        Sends text to LLM and returns structured JSON.
        """
        system_prompt = (
            "You are a strict TOEFL Writing evaluator. "
            "Analyze the student's essay based on ETS standards. "
            "Return the result ONLY as a raw JSON object (no markdown formatting). "
            "The JSON structure must be: "
            "{"
            "  'overall_score': float (0.0 to 5.0),"
            "  'feedback': string (overall constructive feedback),"
            "  'criteria': ["
            "    {'name': 'Grammar', 'score': float, 'comment': string},"
            "    {'name': 'Vocabulary', 'score': float, 'comment': string},"
            "    {'name': 'Organization', 'score': float, 'comment': string},"
            "    {'name': 'Topic Development', 'score': float, 'comment': string}"
            "  ]"
            "}"
        )

        user_content = f"Task Mode: {mode}\nQuestion: {question_prompt}\n\nStudent Essay:\n{text}"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                stream=False,
                temperature=0.3, # Low temperature for consistent scoring
            )

            raw_content = response.choices[0].message.content
            
            # Clean up potential markdown code blocks if the AI adds them
            clean_content = raw_content.replace("```json", "").replace("```", "").strip()
            
            result_json = json.loads(clean_content)
            return result_json

        except Exception as e:
            logger.error(f"AI Service Error: {str(e)}")
            # Fallback/Mock response for development stability if API fails
            return None
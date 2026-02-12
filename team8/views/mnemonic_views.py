# team8/views/mnemonic_views.py

import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from ..ai_utils import AIService

# Hardcoded word for now – replace with dynamic input later
HARDCODED_WORD = "cat"

@require_GET
@csrf_exempt   # only if you don't send CSRF token; fine for dev
def get_mnemonic(request):
    """
    API endpoint that returns word info, mnemonic, story, and generated image.
    """
    try:
        ai = AIService()
        word = HARDCODED_WORD

        # 1. Fetch basic word information (definition, IPA, level)
        word_info_raw = ai.fetch_word_info(word=word, level="B2")
        word_info = json.loads(word_info_raw)
        
        # 2. Generate mnemonic and story
        mnemonic_data = ai.generate_mnemonic_story(word)

        # 3. Generate an image based on the word + mnemonic hint
        #    Use a concise prompt that includes the word and visual clue
        image_prompt = f"{word}, {mnemonic_data['mnemonic_text']}, digital art style"
        image_data_url = ai.generate_image_hf(image_prompt)

        # ... after calling ai.generate_image_hf(...)
        image_data_url = ai.generate_image_hf(image_prompt)
        print("🟣 Image URL received in view:", image_data_url)   # <-- 4
        
        
        # 4. Build the response
        response_data = {
            "word": word_info.get("word", word),
            "level": "B2",   # could be dynamic later
            "definition": word_info.get("definition", ""),
            "phonetic": word_info.get("ipa", "/?/"),
            "image_url": image_data_url,
            "mnemonic_text": mnemonic_data.get("mnemonic_text", ""),
            "story_text": mnemonic_data.get("story_text", ""),
        }

        print("📦 Final response data:", response_data)           # <-- 5

        return JsonResponse(response_data)
    
    except Exception as e:
        # Log the error (add proper logging later)
        print(f"Error in get_mnemonic: {e}")
        return JsonResponse({"error": str(e)}, status=500)
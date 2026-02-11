import os, requests, json, io
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.base import ContentFile
from groq import Groq
from ..models.word import Word
from ..models.menemonic import WordStory
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
story_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
image_client = InferenceClient(
    provider="nscale",
    api_key=os.getenv("IMAGE_GENERATION_API_KEY"),
)


def menemonic_page(request):
    return render(request, 'team8/menemonic_page.html')

def generate_story(request):
    """
    Expects JSON body:
    {
        "word_id": 1
    }
    """
    try:
        data = json.loads(request.body)
        word_id = data.get("word_id")

        if not word_id:
            return JsonResponse({"error": "word_id is required"}, status=400)

        word = Word.objects.get(id=word_id)

        prompt = f"""
        Write a vivid 1–3 paragraph contextual story to help memorize the word: "{word.word}".
        The story must clearly demonstrate the meaning of the word in context.
        Keep it engaging and easy to remember.
        """

        completion = story_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192"
        )

        story_text = completion.choices[0].message.content.strip()

        word_story = WordStory.objects.create(
            word=word,
            story=story_text
        )

        return JsonResponse({
            "word": word.word,
            "story": story_text
        })

    except Word.DoesNotExist:
        return JsonResponse({"error": "Word not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def generate_image(request):
    """
    Expects JSON body:
    {
        "word_story_id": 1
    }
    """
    try:
        data = json.loads(request.body)
        word_story_id = data.get("word_story_id")

        if not word_story_id:
            return JsonResponse({"error": "word_story_id is required"}, status=400)

        word_story = WordStory.objects.get(id=word_story_id)

        prompt = f"Create a memorable illustrative image representing the word '{word_story.word.word}'."

        # 1. Generate the image. This returns a PIL.Image object.
        image = image_client.text_to_image(
            prompt,
            model="stabilityai/stable-diffusion-xl-base-1.0",
        )

        # 2. Prepare the filename
        file_name = f"{word_story.word.word}_{word_story.id}.png"

        # 3. Create a BytesIO buffer to hold the image data in memory
        buffer = io.BytesIO()
        
        # 4. Save the PIL image into the buffer as a PNG
        image.save(buffer, format="PNG")
        
        # 5. Save the buffer content to the Django model field
        # ContentFile wraps the bytes so Django treats it like an uploaded file
        word_story.image.save(file_name, ContentFile(buffer.getvalue()), save=True)

        return JsonResponse({
            "message": "Image generated successfully",
            "image_url": word_story.image.url
        })

    except WordStory.DoesNotExist:
        return JsonResponse({"error": "WordStory not found"}, status=404)
    except Exception as e:
        print(f"Error generating image: {e}") # Helpful for debugging
        return JsonResponse({"error": str(e)}, status=500)
# Team7 Speaking Assessment Feature

## Overview
This document describes the implementation of Sprint 2: Speaking Assessment & Advanced AI for the TOEFL AI Evaluation Platform.

## Features Implemented

### Task 8: ASR Service Integration ✓
- **SpeakingEvaluator Class**: Complete implementation in `services.py`
- **ASR Integration**: OpenAI Whisper API for speech-to-text transcription
- **Error Handling**: Comprehensive timeout and error recovery mechanisms
- **Validation**: Audio file format (.wav, .mp3, .flac) and size (10MB limit)
- **Speech Detection**: Handles silent/noisy audio with proper error messages

### Task 9: Speaking Evaluation Logic ✓
- **LLM Prompt Engineering**: Custom prompts for Speaking evaluation
  - Delivery (clarity, pace, pronunciation)
  - Language Use (grammar, vocabulary)
  - Topic Development (content relevance, coherence)
- **Service Integration**: Complete ASR → LLM workflow
- **Database Persistence**: Audio path and transcript storage
- **Rubric Compliance**: ETS TOEFL iBT Speaking rubric standards

### Task 10: Speaking API Endpoint ✓
- **REST API Endpoint**: `POST /api/v1/evaluate/speaking/`
- **Multipart Upload**: Handles `multipart/form-data` via Django `request.FILES`
- **File Validation**: Format and size checks per SRS FR-SP-01
- **Error Responses**: Standardized error codes (400, 404, 503)
- **URL Routing**: Integrated into `urls.py`

## Architecture

### Database Schema (models.py)
```python
class Evaluation(models.Model):
    evaluation_id = UUIDField(primary_key=True)
    user_id = UUIDField()
    question = ForeignKey(Question)
    task_type = CharField(choices=['writing', 'speaking'])
    
    # Speaking-specific fields
    audio_path = CharField()  # Path to audio file
    transcript_text = TextField()  # ASR output
    
    # Common evaluation fields
    overall_score = DecimalField()
    ai_feedback = TextField()
    rubric_version_id = CharField()
    created_at = DateTimeField()
```

### Service Layer (services.py)

#### SpeakingEvaluator
```python
class SpeakingEvaluator:
    RUBRIC_VERSION = "ETS_iBT_Speaking_2024_v1"
    MAX_FILE_SIZE_MB = 10
    ALLOWED_FORMATS = ['.wav', '.mp3', '.flac']
    
    def validate_audio_file(audio_file) -> tuple[bool, str]
    def transcribe_audio(audio_file, timeout=30) -> dict
    def analyze_speaking(transcript_text, question_obj, mode) -> dict
```

#### EvaluationService
```python
class EvaluationService:
    def evaluate_speaking(user_id, question_id, audio_file) -> tuple[dict, int]:
        # 1. Validate audio file
        # 2. Transcribe audio (ASR)
        # 3. Analyze transcript (LLM)
        # 4. Save to database
        # 5. Return JSON response
```

### API Endpoint (views.py)
```python
@csrf_exempt
@require_http_methods(["POST"])
@api_login_required
def submit_speaking(request):
    """
    Expects:
        - user_id (form field)
        - question_id (form field)
        - audio_file (file upload)
    
    Returns:
        {
            "status": "success",
            "evaluation_id": "uuid",
            "overall_score": 3.5,
            "feedback": "...",
            "transcript": "...",
            "criteria": [...]
        }
    """
```

## API Usage

### Endpoint Details
- **URL**: `POST /team7/api/v1/evaluate/speaking/`
- **Content-Type**: `multipart/form-data`
- **Authentication**: Bearer token required

### Request Format
```bash
curl -X POST http://localhost:8000/team7/api/v1/evaluate/speaking/ \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000" \
  -F "question_id=650e8400-e29b-41d4-a716-446655440001" \
  -F "audio_file=@/path/to/recording.wav"
```

### Response Format (Success)
```json
{
  "status": "success",
  "evaluation_id": "750e8400-e29b-41d4-a716-446655440002",
  "overall_score": 3.5,
  "feedback": "Your response demonstrates good language use...",
  "transcript": "In my opinion, technology has greatly improved...",
  "criteria": [
    {
      "name": "Delivery",
      "score": 3.5,
      "comment": "Clear pronunciation with good pace"
    },
    {
      "name": "Language Use",
      "score": 3.5,
      "comment": "Appropriate vocabulary and grammar"
    },
    {
      "name": "Topic Development",
      "score": 3.0,
      "comment": "Good content but could expand on examples"
    }
  ],
  "created_at": "2024-02-09T10:30:00Z"
}
```

### Error Responses

#### 400 - Invalid Input
```json
{
  "error": "INVALID_INPUT",
  "message": "File format '.txt' not supported. Use .wav, .mp3, .flac."
}
```

#### 400 - No Speech Detected
```json
{
  "error": "NO_SPEECH_DETECTED",
  "message": "No speech detected in the audio file. Please ensure your microphone is working."
}
```

#### 404 - Question Not Found
```json
{
  "error": "QUESTION_NOT_FOUND",
  "message": "Invalid question ID"
}
```

#### 503 - Service Unavailable
```json
{
  "error": "SERVICE_UNAVAILABLE",
  "message": "AI service temporarily unavailable. Try again later."
}
```

## Testing

### Test Suite
Run the comprehensive test suite:
```bash
python team7/test_speaking_api.py [audio_file.wav] [user_id] [question_id]
```

### Manual Testing with curl
```bash
# Test with a valid audio file
curl -X POST http://localhost:8000/team7/api/v1/evaluate/speaking/ \
  -H "Authorization: Bearer test-api-key" \
  -F "user_id=test-user-123" \
  -F "question_id=test-question-456" \
  -F "audio_file=@sample_recording.wav"
```

## Performance Requirements

### Response Times (per SRS)
- **Writing Evaluation**: < 15 seconds (95th percentile)
- **Speaking Evaluation**: < 25 seconds (95th percentile)
  - ASR: ~5-8 seconds
  - LLM Analysis: ~8-12 seconds
  - Database/File I/O: ~2-3 seconds

### File Constraints
- **Max Size**: 10 MB
- **Duration**: 30-90 seconds recommended
- **Formats**: WAV, MP3, FLAC

## Git Commits

### Task 8: ASR Service Integration
```
feat(team7): implement ASR service integration with SpeakingEvaluator

- Add SpeakingEvaluator class with Whisper API integration
- Implement transcribe_audio() with timeout handling
- Add validate_audio_file() for format and size validation
- Support .wav, .mp3, .flac formats with 10MB size limit
- Handle no-speech-detected scenarios
- Add evaluate_speaking() method in EvaluationService
```

### Task 10: Speaking API Endpoint
```
feat(team7): implement speaking API endpoint with multipart upload

- Add submit_speaking endpoint to handle audio uploads
- Implement multipart/form-data processing via request.FILES
- Add file validation for format and size
- Route POST /api/v1/evaluate/speaking/ in urls.py
- Handle missing fields with proper error responses
- Integrate with EvaluationService.evaluate_speaking
```

## Dependencies

### Python Packages (requirements.txt)
```
Django>=4.2
gunicorn
psycopg2-binary
openai  # For Whisper ASR and LLM
python-dotenv
```

### Environment Variables
```bash
# .env file
AI_GENERATOR_API_KEY=your-openai-api-key-here
```

## Workflow Diagrams

### Speaking Evaluation Flow (from diagrams.txt)
1. **Student** records audio via interface and clicks submit
2. **Interface** sends `POST /evaluate/speaking {files, .wav...}`
3. **EvalController** calls `EvalSpeaking(DTO)` on EvalService
4. **EvalService** calls `ProcessAudio(audioFile)` on SpeakingEval
5. **SpeakingEval** sends audio to **ASR** → receives Transcript
6. **SpeakingEval** sends Transcript to **LLM** → receives JSON scores
7. **EvalService** saves to **Database**
8. **EvalController** returns JSON response (200 OK)

## Compliance

### SRS Requirements Met
- ✓ FR-SP-01: Audio validation (format, size)
- ✓ FR-SP-02: ASR integration with error handling
- ✓ FR-SP-03: LLM-based speaking evaluation
- ✓ FR-SP-04: Transcript storage
- ✓ FR-API-02: RESTful endpoint with multipart support
- ✓ FR-SEC-01: Input validation and sanitization

### ETS TOEFL iBT Rubric Compliance
- **Score Range**: 0.0 - 4.0 (Speaking scale)
- **Criteria**:
  - Delivery: Pronunciation, fluency, pace
  - Language Use: Grammar, vocabulary range
  - Topic Development: Content relevance, coherence

## Future Enhancements
- [ ] S3/Cloud storage for audio files
- [ ] Audio streaming support
- [ ] Real-time transcription feedback
- [ ] Pronunciation analysis (phoneme-level)
- [ ] Pace/fluency metrics from ASR metadata
- [ ] Multi-language support beyond English

## Contact
**Developer**: Mahan Zavari (Backend & AI)
**Sprint**: 2 - Speaking Assessment & Advanced AI
**Branch**: `feature/team7-10-Speaking-Assessment`

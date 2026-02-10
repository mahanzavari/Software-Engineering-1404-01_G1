from django.http import JsonResponse
from django.shortcuts import render
from core.auth import api_login_required
from django.contrib.auth.decorators import login_required
from .models import UserSession, Passage, Question, Option
from django.shortcuts import get_object_or_404
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import Passage, Question, UserSession, UserAnswer, AntiCheatLog
import json


TEAM_NAME = "team14"

@api_login_required
def ping(request):
    return JsonResponse({"team": TEAM_NAME, "ok": True})

def base(request):
    return render(request, f"{TEAM_NAME}/index.html")

def training_levels(request):
    return render(request, 'team14/training_levels.html')


def index(request):

    last_session = UserSession.objects.filter(
        user=request.user,
        mode='exam',
        end_time__isnull=False,
        scaled_score__isnull=False
    ).order_by('-end_time').first()


    context = {
        'last_score': last_session.scaled_score if last_session else None,
        'has_taken_exam': last_session is not None
    }

    return render(request, 'team14/index.html', context)


login_required(login_url='auth')


def easy_level(request):
    # گرفتن تمام passage های سطح آسان
    passages = Passage.objects.filter(
        difficulty_level='easy'
    ).prefetch_related('questions__options').order_by('-created_at')

    # آماده کردن داده‌ها برای ارسال به template
    passages_data = []
    for passage in passages:
        # شمارش تعداد سوالات
        question_count = passage.questions.count()

        # محاسبه زمان تخمینی (حدود 1 دقیقه برای هر 75 کلمه + 1 دقیقه برای هر سوال)
        estimated_time = (passage.text_length // 75) + question_count

        passages_data.append({
            'id': passage.id,
            'title': passage.title,
            'topic': passage.get_topic_display(),  # نمایش نام فارسی topic
            'text_length': passage.text_length,
            'question_count': question_count,
            'estimated_time': estimated_time,
            'icon': get_topic_icon(passage.topic),  # تابع کمکی برای آیکون
        })

    context = {
        'passages': passages_data,
        'difficulty': 'آسان',
        'total_passages': len(passages_data),
    }

    return render(request, 'team14/practice_passages.html', context)



def mid_level(request):
    # گرفتن تمام passage های سطح متوسط
    passages = Passage.objects.filter(
        difficulty_level='medium'
    ).prefetch_related('questions__options').order_by('-created_at')

    passages_data = []
    for passage in passages:
        question_count = passage.questions.count()
        estimated_time = (passage.text_length // 75) + question_count

        passages_data.append({
            'id': passage.id,
            'title': passage.title,
            'topic': passage.get_topic_display(),
            'text_length': passage.text_length,
            'question_count': question_count,
            'estimated_time': estimated_time,
            'icon': get_topic_icon(passage.topic),
        })

    context = {
        'passages': passages_data,
        'difficulty': 'متوسط',
        'total_passages': len(passages_data),
    }

    return render(request, 'team14/practice_passages.html', context)



def hard_level(request):
    # گرفتن تمام passage های سطح سخت
    passages = Passage.objects.filter(
        difficulty_level='hard'
    ).prefetch_related('questions__options').order_by('-created_at')

    passages_data = []
    for passage in passages:
        question_count = passage.questions.count()
        estimated_time = (passage.text_length // 75) + question_count

        passages_data.append({
            'id': passage.id,
            'title': passage.title,
            'topic': passage.get_topic_display(),
            'text_length': passage.text_length,
            'question_count': question_count,
            'estimated_time': estimated_time,
            'icon': get_topic_icon(passage.topic),
        })

    context = {
        'passages': passages_data,
        'difficulty': 'سخت',
        'total_passages': len(passages_data),
    }

    return render(request, 'team14/practice_passages.html', context)


def get_topic_icon(topic):
        icons = {
            'biology': '🧬',
            'history': '📜',
            'astronomy': '🌌',
            'geology': '🌍',
            'anthropology': '🗿',
        }
        return icons.get(topic, '📚')

def Exam_Page(request):
    return render(request, 'team14/Exam_Page.html')



def practice_page(request, passage_id):
    passage = get_object_or_404(
        Passage.objects.prefetch_related('questions__options'),
        id=passage_id
    )

    questions = passage.questions.all().order_by('id')
    total_questions = questions.count()

    # ایجاد Session جدید یا بازیابی Session فعلی
    session, created = UserSession.objects.get_or_create(
        user_id=request.user.id,  # ✅ خیلی مهم
        passage=passage,
        mode='practice',
        defaults={
            'start_time': timezone.now(),
        }
    )

    # دریافت پاسخ‌های قبلی کاربر (اگر وجود دارد)
    user_answers = {
        answer.question_id: answer.selected_option_id
        for answer in UserAnswer.objects.filter(
            #user=request.user,
            question__passage=passage,
            session=session
        )
    }

    context = {
        'passage': passage,
        'questions': questions,
        'total_questions': total_questions,
        'session': session,
        'user_answers': json.dumps(user_answers),
        'mode': 'practice',
        'current_question_index': 0,
    }

    return render(request, 'team14/Practice_Page.html', context)



def submit_answer(request):
    """ذخیره پاسخ کاربر (AJAX)"""

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question_id = data.get('question_id')
            option_id = data.get('option_id')
            session_id = data.get('session_id')

            question = get_object_or_404(Question, id=question_id)
            session = get_object_or_404(UserSession, id=session_id, user=request.user)

            # بررسی آیا قبلاً پاسخ داده شده
            answer, created = UserAnswer.objects.get_or_create(
                user=request.user,
                question=question,
                session=session,
                defaults={'selected_option_id': option_id}
            )

            # اگر پاسخ تغییر کرده، آپدیت کن
            if not created and answer.selected_option_id != option_id:
                answer.selected_option_id = option_id
                answer.changed_count += 1
                answer.save()

            return JsonResponse({
                'success': True,
                'message': 'پاسخ ذخیره شد'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

    return JsonResponse({'success': False}, status=405)



def finish_practice(request, session_id):
    """اتمام تمرین و محاسبه نمره"""

    session = get_object_or_404(UserSession, id=session_id, user=request.user)

    # محاسبه نمره
    user_answers = UserAnswer.objects.filter(session=session)
    correct_count = 0

    for answer in user_answers:
        if answer.selected_option and answer.selected_option.is_correct:
            correct_count += 1

    total_questions = session.passage.questions.count()

    # محاسبه نمره درصدی
    if total_questions > 0:
        percentage = (correct_count / total_questions) * 100
        session.score = percentage
        session.status = 'completed'
        session.completed_at = timezone.now()
        session.save()

    return redirect('team14:practice_result', session_id=session.id)



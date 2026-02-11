from django.core.management.base import BaseCommand
from team7.models import Question, TaskType, Mode
from django.db import transaction

class Command(BaseCommand):
    help = 'Seeds 20 TOEFL Writing and 20 TOEFL Speaking questions into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing questions before seeding new ones',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        db_alias = 'team7'

        if options['clear']:
            count = Question.objects.using(db_alias).count()
            Question.objects.using(db_alias).all().delete()
            self.stdout.write(self.style.WARNING(f'Successfully deleted {count} existing questions from database "{db_alias}".'))

        questions_data = []

        # =====================
        # 20 WRITING TASKS
        # =====================
        writing_prompts = [
            # 15 Independent Tasks
            ('Technology\'s Impact', 2, "Do you agree or disagree: Technology has made the world a better place to live. Support your answer with specific reasons and examples."),
            ('Teamwork vs. Solo Work', 2, "Is it better to work in teams or to work alone? Use specific reasons and examples to support your position."),
            ('University Attendance', 3, "Some believe university classes should be mandatory, while others think they should be optional. Which view do you agree with? Explain your reasoning."),
            ('Value of Money in a Job', 3, "Do you agree or disagree: The most important aspect of a job is the money a person earns. Use specific reasons to support your answer."),
            ('Parents as Teachers', 2, "Do you agree or disagree with the statement that parents are the best teachers? Use specific examples to support your answer."),
            ('Experiences vs. Possessions', 3, "Is it better to spend money on experiences like travel or on material possessions like clothes and electronics? Explain your choice."),
            ('Quick Decisions', 3, "Is it better to make decisions quickly or to take your time? Use specific reasons and examples to support your answer."),
            ('Influence of Television', 2, "Do you agree or disagree that television has destroyed communication among friends and family?"),
            ('Learning from Mistakes', 3, "Describe a time you made a mistake. What did you learn from it?"),
            ('Qualities of a Good Neighbor', 2, "What are the most important qualities of a good neighbor? Use specific details and examples in your answer."),
            ('Government Funding Priorities', 4, "Should governments spend more money on improving roads and highways, or on improving public transportation?"),
            ('The Importance of Hard Work', 3, "Do you agree or disagree that success is a result of hard work, not luck?"),
            ('Modern Lifestyles', 3, "Are people today healthier than they were 100 years ago? Support your opinion."),
            ('Animal Conservation', 4, "Is it more important to protect endangered animal species or to focus on human needs?"),
            ('Online vs. In-Person Learning', 2, "What are the advantages and disadvantages of online learning compared to traditional classroom learning?"),

            # 5 Integrated Tasks
            ('Remote Work Debate', 4, "Summarize the points made in the lecture about the drawbacks of remote work and explain how they challenge the points in the reading passage.", "The benefits of remote work include increased productivity, better work-life balance, and reduced costs. Studies show employees working from home report higher satisfaction.", 'https://example.com/audio/writing_remote_work.mp3'),
            ('Biofuels Controversy', 5, "Summarize the lecture's points on the environmental problems caused by biofuels, explaining how they counter the arguments in the reading.", "Biofuels are a clean, renewable energy source that can reduce our dependency on fossil fuels and help combat climate change.", 'https://example.com/audio/writing_biofuels.mp3'),
            ("The Great Wall's Purpose", 4, "Explain how the lecturer's theory about the Great Wall of China's purpose differs from the theory presented in the reading passage.", "The primary purpose of the Great Wall of China was to provide a formidable defense against northern invasions.", 'https://example.com/audio/writing_great_wall.mp3'),
            ('Decline of Honeybees', 5, "Summarize the professor's explanation for the decline in honeybee populations and how it casts doubt on the theory in the reading.", "The leading theory for Colony Collapse Disorder is the widespread use of neonicotinoid pesticides.", 'https://example.com/audio/writing_honeybees.mp3'),
            ('Shakespeare Authorship', 4, "Explain the arguments from the lecture that challenge the theory presented in the reading passage about the true author of Shakespeare's plays.", "There is a growing body of evidence suggesting that William Shakespeare of Stratford-upon-Avon did not write the plays attributed to him.", 'https://example.com/audio/writing_shakespeare.mp3')
        ]
        for title, diff, prompt, *rest in writing_prompts:
            reading = rest[0] if len(rest) > 0 else None
            url = rest[1] if len(rest) > 1 else None
            questions_data.append({
                'task_type': TaskType.WRITING, 'mode': Mode.INTEGRATED if url else Mode.INDEPENDENT,
                'title': title, 'difficulty': diff, 'prompt_text': prompt, 'reading_text': reading, 'resource_url': url
            })

        # =====================
        # 20 SPEAKING TASKS
        # =====================
        speaking_prompts = [
            # 10 Independent Tasks
            ('Favorite Place to Study', 1, "Describe your favorite place to study. Explain why you like this place and how it helps you study effectively."),
            ('Small Town vs. Big City', 2, "Some people prefer to live in a small town. Others prefer a big city. Which would you prefer? Use specific reasons to support your answer."),
            ('Learning About Other Cultures', 2, "Do you agree or disagree: It is important to learn about other cultures. Use details and examples to explain your opinion."),
            ('An Important Decision', 3, "Describe an important decision you have made. Explain why this decision was important and how it affected your life."),
            ('A Favorite Book or Movie', 2, "Talk about your favorite book or movie. Describe what it is about and explain why you like it so much."),
            ('Qualities of a Good Leader', 3, "What do you think are the most important qualities of a good leader? Use specific examples to support your view."),
            ('Technology in Education', 2, "How do you think technology has changed education? Provide specific examples."),
            ('A Memorable Trip', 2, "Describe a memorable trip you have taken. Explain what made it so memorable."),
            ('Advice for a New Student', 1, "If a new student asked you for advice on how to succeed at your school, what would you say?"),
            ('Spending a Free Day', 1, "How do you like to spend a free day? Describe your perfect day off."),

            # 10 Integrated Tasks
            ('Online Course Requirement', 4, "The university plans to require all students to take an online course. The woman expresses her opinion. State her opinion and the reasons she gives.", 'https://example.com/audio/speaking_online_course.mp3'),
            ('Social Influence Types', 5, "Using points from the lecture, explain the two types of social influence: normative and informational.", 'https://example.com/audio/speaking_social_influence.mp3'),
            ('Library Renovation', 3, "Read the announcement about the library renovation, then listen to two students' conversation. Explain the man's opinion and his reasons.", 'https://example.com/audio/speaking_library_reno.mp3'),
            ('Echolocation', 4, "Explain what echolocation is and how bats use it to find food, based on the reading and lecture.", 'https://example.com/audio/speaking_echolocation.mp3'),
            ('Business: Brand Loyalty', 5, "Using the examples from the lecture, explain the concept of brand loyalty.", 'https://example.com/audio/speaking_brand_loyalty.mp3'),
            ('Campus Parking Policy', 3, "The university is changing its parking policy. The woman expresses her concerns. Summarize her opinion and reasons.", 'https://example.com/audio/speaking_parking_policy.mp3'),
            ('Psychology: Cognitive Dissonance', 5, "Explain the concept of cognitive dissonance, using the example discussed by the professor.", 'https://example.com/audio/speaking_cognitive_dissonance.mp3'),
            ('Biology: Symbiotic Relationships', 4, "Based on the lecture, describe two types of symbiotic relationships and provide examples for each.", 'https://example.com/audio/speaking_symbiosis.mp3'),
            ('History: The Printing Press', 4, "Explain the impact of the printing press on European society, as described in the lecture.", 'https://example.com/audio/speaking_printing_press.mp3'),
            ('Art: Realism Movement', 4, "Describe the main characteristics of the Realism art movement, based on the professor's lecture.", 'https://example.com/audio/speaking_realism.mp3')
        ]
        for title, diff, prompt, *rest in speaking_prompts:
            url = rest[0] if rest else None
            questions_data.append({
                'task_type': TaskType.SPEAKING, 'mode': Mode.INTEGRATED if url else Mode.INDEPENDENT,
                'title': title, 'difficulty': diff, 'prompt_text': prompt, 'reading_text': None, 'resource_url': url
            })

        # =====================
        # DATABASE INSERTION
        # =====================
        created_count = 0
        for q_data in questions_data:
            question, created = Question.objects.using(db_alias).update_or_create(
                title=q_data['title'],
                task_type=q_data['task_type'],
                defaults={
                    'mode': q_data['mode'],
                    'difficulty': q_data['difficulty'],
                    'prompt_text': q_data['prompt_text'],
                    'reading_text': q_data.get('reading_text'),
                    'resource_url': q_data['resource_url'],
                }
            )
            if created:
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Seeding complete! Created {created_count} new questions.'))
        total_questions = Question.objects.using(db_alias).count()
        self.stdout.write(self.style.SUCCESS(f'Total questions in database "{db_alias}": {total_questions}'))
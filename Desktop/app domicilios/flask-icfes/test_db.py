from supabase_client import supabase

# Create exam
exam_resp = supabase.table('exams').insert({
    'user_id': '887b6184-458e-4718-ac26-a7442c905e41',
    'title': 'ICFES Simulacro'
}).execute()
exam_id = exam_resp.data[0]['id']
print('Exam created:', exam_id)

# Insert questions
questions = [
    {
        'question_text': '¿Cuál es la capital de Colombia?',
        'options': ['Bogotá', 'Medellín', 'Cali', 'Barranquilla'],
        'correct_answer': 'Bogotá'
    },
    {
        'question_text': '¿Cuánto es 2 + 2?',
        'options': ['3', '4', '5', '6'],
        'correct_answer': '4'
    },
    {
        'question_text': '¿Qué es Python?',
        'options': ['Lenguaje', 'Serpiente', 'Fruta', 'País'],
        'correct_answer': 'Lenguaje'
    }
]

for q in questions:
    supabase.table('questions').insert({
        'exam_id': exam_id,
        'question_text': q['question_text'],
        'options': q['options'],
        'correct_answer': q['correct_answer']
    }).execute()

print('Questions inserted')

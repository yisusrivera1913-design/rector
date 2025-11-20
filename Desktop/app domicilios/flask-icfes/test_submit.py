from supabase_client import supabase

exam_id = '51d1122a-2de9-4c4b-88e5-0b1de550e6d1'
user_id = '887b6184-458e-4718-ac26-a7442c905e41'

questions = supabase.table('questions').select('*').eq('exam_id', exam_id).execute().data
print('Questions for exam:', questions)

for q in questions:
    supabase.table('questions').update({'user_answer': q['correct_answer']}).eq('id', q['id']).execute()

print('Updated answers')

score = (3 / 3) * 100
supabase.table('exams').update({'score': score}).eq('id', exam_id).execute()
supabase.table('results').insert({
    'exam_id': exam_id,
    'user_id': user_id,
    'total_questions': 3,
    'correct_answers': 3,
    'score': score
}).execute()

print('Results inserted')

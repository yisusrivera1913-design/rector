# models.py - Supabase table schemas (for reference, as Supabase is schemaless but we define here)

# Existing table: usuarios
# {
#   "id": "uuid",
#   "nombre": "text",
#   "cedula_hash": "text",
#   "cedula_cifrada": "bytea",
#   "tiene_acceso": "boolean",
#   "created_at": "timestamp"
# }

# New table: exams
# {
#   "id": "uuid",
#   "user_id": "uuid",  # FK to usuarios.id
#   "title": "text",
#   "score": "integer",
#   "created_at": "timestamp"
# }

# New table: questions
# {
#   "id": "uuid",
#   "exam_id": "uuid",  # FK to exams.id
#   "question_text": "text",
#   "options": "jsonb",  # e.g., ["A", "B", "C", "D"]
#   "correct_answer": "text",
#   "user_answer": "text",  # optional, for results
#   "created_at": "timestamp"
# }

# New table: results
# {
#   "id": "uuid",
#   "exam_id": "uuid",  # FK to exams.id
#   "user_id": "uuid",  # FK to usuarios.id
#   "total_questions": "integer",
#   "correct_answers": "integer",
#   "score": "float",
#   "created_at": "timestamp"
# }

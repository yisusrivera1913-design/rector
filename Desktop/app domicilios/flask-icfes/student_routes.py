from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from security import require_auth, log_security_event
from supabase_client import supabase

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route("/")
@require_auth
def student_panel():
    user_id = session["user"]["id"]
    resp = supabase.table("exams").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
    exams = resp.data or []
    return render_template("student_panel.html", user=session["user"], exams=exams)

@student_bp.route("/generate_exam", methods=["POST"])
@require_auth
def generate_exam():
    user_id = session["user"]["id"]
    exam_resp = supabase.table("exams").insert({"user_id": user_id, "title": "ICFES Simulacro"}).execute()
    exam_id = exam_resp.data[0]["id"]

    # Preguntas de ejemplo
    questions = [
        {"question_text": "¿Cuál es la capital de Colombia?", "options": ["Bogotá", "Medellín", "Cali", "Barranquilla"], "correct_answer": "Bogotá"},
        {"question_text": "¿Cuánto es 2 + 2?", "options": ["3", "4", "5", "6"], "correct_answer": "4"},
        {"question_text": "¿Qué es Python?", "options": ["Lenguaje", "Serpiente", "Fruta", "País"], "correct_answer": "Lenguaje"}
    ]

    for q in questions:
        supabase.table("questions").insert({
            "exam_id": exam_id,
            "question_text": q["question_text"],
            "options": q["options"],
            "correct_answer": q["correct_answer"]
        }).execute()

    log_security_event("exam_generated", {"exam_id": exam_id, "user_id": user_id})
    flash("Examen generado", "success")
    return redirect(url_for('student.take_exam', exam_id=exam_id))

@student_bp.route("/exam/<exam_id>")
@require_auth
def take_exam(exam_id):
    user_id = session["user"]["id"]
    exam_resp = supabase.table("exams").select("*").eq("id", exam_id).eq("user_id", user_id).execute()
    if not exam_resp.data:
        flash("Examen no encontrado", "error")
        return redirect(url_for('student.student_panel'))

    exam = exam_resp.data[0]
    q_resp = supabase.table("questions").select("*").eq("exam_id", exam_id).execute()
    questions = q_resp.data or []
    return render_template("exam.html", exam=exam, questions=questions)

@student_bp.route("/submit_exam/<exam_id>", methods=["POST"])
@require_auth
def submit_exam(exam_id):
    user_id = session["user"]["id"]
    q_resp = supabase.table("questions").select("*").eq("exam_id", exam_id).execute()
    questions = q_resp.data or []

    correct = 0
    total = len(questions)
    for q in questions:
        user_answer = request.form.get(f"q_{q['id']}")
        if user_answer == q["correct_answer"]:
            correct += 1
        supabase.table("questions").update({"user_answer": user_answer}).eq("id", q["id"]).execute()

    score = (correct / total) * 100 if total > 0 else 0
    supabase.table("exams").update({"score": score}).eq("id", exam_id).execute()
    supabase.table("results").insert({
        "exam_id": exam_id,
        "user_id": user_id,
        "total_questions": total,
        "correct_answers": correct,
        "score": score
    }).execute()

    log_security_event("exam_completed", {
        "exam_id": exam_id,
        "user_id": user_id,
        "score": score
    })
    flash(f"Examen completado. Puntaje: {score:.2f}%", "success")
    return redirect(url_for('student.student_panel'))

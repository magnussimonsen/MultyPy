from multipy.models import SessionResults

class MetricsService:
    @staticmethod
    def get_feedback_message(results: SessionResults) -> str:
        accuracy = 0
        if results.total_questions > 0:
            accuracy = (results.correct_answers / results.total_questions) * 100
            
        if accuracy == 100:
            return "Excellent! 🌟 Perfect Score!"
        elif accuracy >= 80:
            return "Great Job! 🎉"
        elif accuracy >= 50:
            return "Good Effort! Keep practicing. 👍"
        else:
            return "Don't give up! Practice makes perfect. 💪"

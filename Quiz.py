# Glendon's AI Learning Quiz for Kids
# Feed a .txt file (chapter), and the AI makes a quiz!

from transformers import pipeline
import random
import os

# Load the question generation model
question_generator = pipeline("text2text-generation", model="t5-small")

def read_text_file(filepath):
    """Read content from a .txt file."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print("File not found. Please make sure the file path is correct.")
        return None

def generate_quiz(text, num_questions=5):
    """
    Generates question-answer pairs from the input text.
    """
    input_text = f"generate question: {text[:500]}"  # Use first 500 characters to avoid overload
    results = question_generator(
        input_text,
        max_length=64,
        num_return_sequences=num_questions,
        num_beams=5,
        early_stopping=True
    )

    quiz_pairs = []
    for r in results:
        output = r["generated_text"]

        # Basic extraction if format is like "Question? Answer"
        if "?" in output:
            question = output.split("?")[0] + "?"
            answer = output.split("?")[1].strip().lstrip("A:").strip()
            quiz_pairs.append((question, answer if answer else "Unknown"))
        else:
            quiz_pairs.append((output.strip(), "Unknown"))

    return quiz_pairs

def generate_choices(correct_answer, text):
    """
    Generates 4 answer choices: 1 correct + 3 distractors from the text.
    """
    words = list(set(text.split()))
    words = [w.strip(",.?!") for w in words if w.istitle() or w.isalpha()]
    random.shuffle(words)

    incorrect_answers = []
    for word in words:
        if word.lower() not in correct_answer.lower() and word.lower() != correct_answer.lower():
            incorrect_answers.append(word)
        if len(incorrect_answers) == 3:
            break

    choices = [correct_answer] + incorrect_answers
    random.shuffle(choices)
    return choices

def run_quiz():
    """
    Runs the quiz by loading a file, generating questions, and scoring answers.
    """
    print("📚 Welcome to Glendon's AI-Powered Learning Quiz!")
    print("Give me a chapter (.txt file), and I’ll create a fun quiz for you.\n")

    filepath = input("📄 Enter the full path to the .txt file (e.g., chapters/science_ch1.txt): ").strip()
    if not os.path.exists(filepath):
        print("❌ That file does not exist. Please try again.")
        return

    text = read_text_file(filepath)
    if not text:
        return

    print("\n✨ Generating your quiz... Please wait.\n")
    questions = generate_quiz(text, num_questions=5)

    score = 0

    for i, (question, correct_answer) in enumerate(questions, 1):
        print(f"\n📝 Question {i}: {question}")
        choices = generate_choices(correct_answer, text)

        for j, choice in enumerate(choices, 1):
            print(f"{j}. {choice}")

        user_choice = input("👉 Enter the number of your answer: ").strip()
        while not user_choice.isdigit() or int(user_choice) not in range(1, 5):
            print("Invalid choice. Please enter a number between 1 and 4.")
            user_choice = input("👉 Enter your answer: ").strip()

        if choices[int(user_choice) - 1].lower() == correct_answer.lower():
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Oops! The correct answer was: {correct_answer}")

    print(f"\n🎉 Quiz finished! You scored {score}/{len(questions)}")
    if score == len(questions):
        print("🏆 Excellent! You nailed it!")
    elif score >= len(questions) / 2:
        print("👍 Good job! Keep learning!")
    else:
        print("💡 Keep practicing. You're getting better every time!")

if __name__ == "__main__":
    run_quiz()

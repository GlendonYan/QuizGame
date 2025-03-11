# glendon
# Quiz game
# trying to see if AI can generate questions
# have fun....


from transformers import pipeline
import random

# Load the text2text-generation model
question_generator = pipeline("text2text-generation", model="t5-small")

# Define domain-specific texts
domain_texts = {
    "history": [
        "The American Revolution was a colonial revolt that occurred between 1765 and 1783. "
        "The thirteen American colonies defeated the British and gained independence. "
        "Key figures include George Washington, Thomas Jefferson, and Benjamin Franklin.",
        "World War II was a global conflict that lasted from 1939 to 1945. "
        "It involved most of the world's nations, including the Allies and the Axis powers. "
        "The war ended with the surrender of Germany and Japan.",
    ],
    "science": [
        "The solar system consists of the Sun and the objects that orbit it, including planets, moons, asteroids, and comets. "
        "The eight planets in the solar system are Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. "
        "Earth is the third planet from the Sun and is the only known planet to support life.",
        "Photosynthesis is the process by which green plants use sunlight to convert carbon dioxide and water into glucose and oxygen. "
        "This process is essential for life on Earth as it produces oxygen and provides energy for plants.",
    ],
    "geography": [
        "The Earth is divided into seven continents: Asia, Africa, North America, South America, Antarctica, Europe, and Australia. "
        "The largest continent by area is Asia, and the smallest is Australia. "
        "The longest river in the world is the Nile, and the highest mountain is Mount Everest.",
        "The Amazon Rainforest is the largest tropical rainforest in the world, covering most of the Amazon basin in South America. "
        "It is home to millions of species of plants, animals, and insects.",
    ],
    "technology": [
        "Artificial intelligence (AI) is the simulation of human intelligence in machines. "
        "AI is used in various fields, including healthcare, finance, and transportation. "
        "Key technologies include machine learning, natural language processing, and computer vision.",
        "Blockchain is a decentralized digital ledger technology used to record transactions across multiple computers. "
        "It is the underlying technology behind cryptocurrencies like Bitcoin and Ethereum.",
    ],
    "literature": [
        "William Shakespeare was an English playwright and poet, widely regarded as one of the greatest writers in the English language. "
        "His famous works include 'Romeo and Juliet', 'Hamlet', and 'Macbeth'.",
        "Jane Austen was an English novelist known for her works such as 'Pride and Prejudice' and 'Sense and Sensibility'. "
        "Her novels often explore themes of love, marriage, and social class.",
    ],
}

def generate_quiz(text, num_questions=5):
    """
    Generates quiz questions from a given text.
    """
    # Format the input for question generation
    input_text = f"generate questions: {text}"
    
    # Use beam search to generate multiple questions
    questions = question_generator(
        input_text,
        max_length=50,
        num_return_sequences=num_questions,
        num_beams=5,  # Enable beam search
        early_stopping=True  # Stop early if the model is confident
    )
    return [q['generated_text'] for q in questions]

def generate_choices(correct_answer, text):
    """
    Generates 4 choices for a question, with 1 correct answer and 3 incorrect answers.
    """
    # Create a list of incorrect answers by modifying the correct answer
    incorrect_answers = [
        correct_answer.replace("Earth", "Mars"),
        correct_answer.replace("Sun", "Moon"),
        correct_answer.replace("solar system", "galaxy"),
    ]
    
    # Combine correct and incorrect answers
    choices = [correct_answer] + incorrect_answers
    
    # Shuffle the choices
    random.shuffle(choices)
    
    return choices

def run_quiz():
    """
    Runs the quiz by generating questions, asking the user, and checking answers.
    """
    print("Welcome to the AI-Powered Quiz Maker!")
    print("You can choose from the following domains: history, science, geography, technology, and literature.")
    
    # Display domain options
    print("\nSelect a domain for your quiz:")
    for i, domain in enumerate(domain_texts.keys(), 1):
        print(f"{i}. {domain.capitalize()}")
    
    # Get user's domain choice
    choice = input("\nEnter the number of your choice: ").strip()
    while not choice.isdigit() or int(choice) not in range(1, len(domain_texts) + 1):
        print("Invalid choice. Please try again.")
        choice = input("Enter the number of your choice: ").strip()
    
    # Get the selected domain
    selected_domain = list(domain_texts.keys())[int(choice) - 1]
    print(f"\nYou selected: {selected_domain.capitalize()}")
    
    # Randomly select a text from the domain
    text = random.choice(domain_texts[selected_domain])
    
    # Generate questions
    questions = generate_quiz(text, num_questions=5)
    
    score = 0
    
    # Ask each question
    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i}: {question}")
        
        # Generate choices (1 correct, 3 incorrect)
        correct_answer = question  # Use the generated question as the correct answer
        choices = generate_choices(correct_answer, text)
        
        # Display choices
        for j, choice in enumerate(choices, 1):
            print(f"{j}. {choice}")
        
        # Get user's answer
        user_choice = input("Enter the number of your answer: ").strip()
        while not user_choice.isdigit() or int(user_choice) not in range(1, 5):
            print("Invalid choice. Please try again.")
            user_choice = input("Enter the number of your answer: ").strip()
        
        # Check if the answer is correct
        if choices[int(user_choice) - 1] == correct_answer:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer is: {correct_answer}")
    
    # Display final score
    print(f"\nQuiz ended! Your score is {score}/{len(questions)}")
    if score == len(questions):
        print("Congratulations! You got all the questions right!")
    elif score >= len(questions) / 2:
        print("Well done! You did a good job.")
    else:
        print("Keep practicing! You'll get better.")

if __name__ == "__main__":
    run_quiz()
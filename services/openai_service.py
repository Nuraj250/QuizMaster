import openai
from config import Config

openai.api_key = Config.OPENAI_API_KEY

def generate_questions(category: str, number_of_questions: int = 5):
    prompt = (
        f"Generate {number_of_questions} multiple-choice quiz questions on {category}. "
        "Each question should have options A, B, C, and D, and specify the correct option clearly."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    content = response['choices'][0]['message']['content']
    return parse_questions(content)

def parse_questions(content: str):
    questions = []
    blocks = content.strip().split('\n\n')
    
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 5:
            question_text = lines[0][3:].strip()
            options = {
                'A': lines[1][2:].strip(),
                'B': lines[2][2:].strip(),
                'C': lines[3][2:].strip(),
                'D': lines[4][2:].strip()
            }
            correct_line = [l for l in lines if "Correct Answer" in l]
            correct_option = correct_line[0].split(":")[-1].strip() if correct_line else 'A'
            questions.append({
                'prompt': question_text,
                'options': options,
                'correct_option': correct_option
            })
    return questions
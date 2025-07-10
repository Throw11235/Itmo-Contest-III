
import streamlit as st
import random
import openai

# Настройка OpenAI API (замените на ваш API ключ)
openai.api_key = "your_openai_api_key"  # или используйте st.secrets

# Список из 100 вопросов (для примера приведено 20, остальные можно добавить аналогично)
QUESTIONS = [
    "Какие школьные предметы вам нравятся больше всего?",
    "Какой вид деятельности вам интересен?",
    "Предпочитаете работать в команде или индивидуально?",
    "Как вы относитесь к публичным выступлениям?",
    "Вам нравится анализировать данные и работать с цифрами?",
    "Интересна ли вам творческая деятельность?",
    "Как вы относитесь к рутинной работе?",
    "Хотели бы вы работать в международной среде?",
    "Важно ли для вас расположение вуза?",
    "Планируете ли заниматься научной деятельностью?",
    "Какой формат обучения вам предпочтительнее?",
    "Интересны ли вам технические специальности?",
    "Хотели бы вы изучать иностранные языки углубленно?",
    "Важно ли для вас наличие военной кафедры?",
    "Планируете ли работать во время учебы?",
    "Какой уровень нагрузки вас устраивает?",
    "Интересны ли вам междисциплинарные программы?",
    "Хотели бы вы участвовать в студенческих обменах?",
    "Важно ли для вас наличие общежития?",
    "Каковы ваши ожидания от вуза?",
    # Добавьте еще 80 вопросов по аналогии
]

def get_random_questions(num=5):
    """Возвращает список случайных вопросов"""
    return random.sample(QUESTIONS, num)

def get_chatgpt_response(prompt):
    """Отправляет запрос к ChatGPT и возвращает ответ"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # или "gpt-4" если доступно
        messages=[
            {"role": "system", "content": "Ты консультант по профориентации. На основе ответов пользователя составь рейтинг из 5 подходящих вузов с объяснением, почему каждый вуз подходит. Опиши конкретные программы и преимущества."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message['content']

def main():
    st.title("🎓 Профориентация: подбор вуза")
    st.write("Ответьте на 5 случайных вопросов, и мы подберем подходящие вузы на основе ваших ответов")

    # Инициализация сессии
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
        st.session_state.questions = get_random_questions(5)
        st.session_state.stage = "questions"

    # Этап вопросов
    if st.session_state.stage == "questions":
        with st.form("questions_form"):
            for i, question in enumerate(st.session_state.questions):
                st.session_state.answers[question] = st.text_input(f"{i + 1}. {question}", key=f"q_{i}")

            submitted = st.form_submit_button("Отправить ответы")
            if submitted:
                if all(st.session_state.answers.values()):
                    st.session_state.stage = "results"
                    st.rerun()
                else:
                    st.warning("Пожалуйста, ответьте на все вопросы")

    # Этап результатов
    elif st.session_state.stage == "results":
        st.success("Спасибо за ответы! Анализируем ваши предпочтения...")

        # Формируем промпт для ChatGPT
        prompt = "Ответы пользователя на вопросы профориентации:\n"
        for question, answer in st.session_state.answers.items():
            prompt += f"- Вопрос: {question}\n  Ответ: {answer}\n\n"

        prompt += "\nПроанализируй ответы и предложи 5 наиболее подходящих вузов в России с объяснением, почему каждый вуз подходит. Укажи конкретные программы и их преимущества для этого пользователя."

        # Получаем ответ от ChatGPT
        with st.spinner("Подбираем вузы..."):
            try:
                response = get_chatgpt_response(prompt)
                st.session_state.recommendations = response
            except Exception as e:
                st.error(f"Произошла ошибка: {e}")
                st.session_state.stage = "questions"
                return
    # Выводим рекомендации
        st.subheader("Рекомендуемые вузы для вас:")
        st.write(st.session_state.recommendations)

        if st.button("Попробовать снова"):
            st.session_state.answers = {}
            st.session_state.questions = get_random_questions(5)
            st.session_state.stage = "questions"
            st.rerun()

if __name__ == "__main__":
    main()
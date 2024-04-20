from openai import OpenAI

client = OpenAI(api_key="")


def format_csv_comments(comment_topic, comment_text):
    # to such form: "{"comment_topic": str, "comment_text": str}"
    return f'''{{'comment_topic': '{comment_topic}', 'comment_text': '{comment_text}'}}'''


def mark_yoruba_text(text):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": '''The text is:''' + text + '''". Please review this text for sentences in Yoruba language. 
             If there's text in yoruba language return this text in yoruba, else return "No Yoruba language found"'''},

        ],
    )

    print(completion.choices[0].message.content)

    return completion.choices[0].message.content



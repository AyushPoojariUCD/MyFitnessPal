import time
from openai_client import client, assistant_id


def send_chat_message(thread, message):
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)

    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run_status.status == "completed":
            break
        time.sleep(0.5)

    messages = client.beta.threads.messages.list(thread_id=thread.id, order="desc", limit=1)
    return messages.data[0].content[0].text.value
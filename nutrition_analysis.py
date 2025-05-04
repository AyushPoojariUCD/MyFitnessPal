import time
from openai_client import client, assistant_id


def analyze_image(thread, uploaded_file):
    with open("temp_image.png", "wb") as f:
        f.write(uploaded_file.getbuffer())

    with open("temp_image.png", "rb") as image_file:
        upload = client.files.create(file=image_file, purpose="assistants")
    file_id = upload.id

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=[
            {"type": "text", "text": "Please extract the nutrition label from this image and assess the healthiness."},
            {"type": "image_file", "image_file": {"file_id": file_id}}
        ]
    )

    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run_status.status == "completed":
            break
        time.sleep(1)

    messages = client.beta.threads.messages.list(thread_id=thread.id, order="desc", limit=1)
    return messages.data[0].content[0].text.value
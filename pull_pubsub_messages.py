import os
from google.cloud import pubsub_v1
from dotenv import load_dotenv

load_dotenv()

project_id = os.getenv("GCP_PROJECT_ID")
subscription_id = "spotify-debug-sub"
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

response = subscriber.pull(
    request={
        "subscription": subscription_path,
        "max_messages": 10,
    }
)

if not response.received_messages:
    print("❌ No messages available (already acknowledged or none published).")
else:
    for msg in response.received_messages:
        print(f"📩 {msg.message.data.decode('utf-8')}")
        subscriber.acknowledge(
            request={
                "subscription": subscription_path,
                "ack_ids": [msg.ack_id],
            }
        )
    print("✅ Messages retrieved and acknowledged.")

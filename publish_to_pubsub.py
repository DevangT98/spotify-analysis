import os
import json
from dotenv import load_dotenv
from google.cloud import pubsub_v1

# Load environment variables
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS"
)

project_id = os.getenv("GCP_PROJECT_ID")
topic_id = os.getenv("PUBSUB_TOPIC")


def publish_tracks_to_pubsub(tracks):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    print(f"📤 Publishing to {topic_path}")

    futures = []

    for item in tracks:
        track = item["track"]
        data = {
            "track_name": track["name"],
            "artists": [artist["name"] for artist in track["artists"]],
            "played_at": item["played_at"],
            "track_id": track["id"],
        }

        message_bytes = json.dumps(data).encode("utf-8")
        futures.append(publisher.publish(topic_path, message_bytes))
        print(f"✅ Queued: {data['track_name']}")
        print(f"📝 Payload: {json.dumps(data)}")

    print("⏳ Waiting for all publish futures to complete...")
    for future in futures:
        future.result(timeout=10)

    print("🎉 All tracks successfully published to Pub/Sub.")

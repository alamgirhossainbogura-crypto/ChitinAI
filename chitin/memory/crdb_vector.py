import os
import psycopg2
from psycopg2.extras import RealDictCursor
import boto3
import json

class CockroachVectorMemory:
    def __init__(self):
        self.db_url = os.getenv("COCKROACH_DB_URL")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.bedrock = boto3.client("bedrock-runtime", region_name=self.aws_region)
        self._init_db()

    def get_connection(self):
        return psycopg2.connect(self.db_url)

    def _init_db(self):
        """ডাটাবেজ টেবিল ও Vector Extension তৈরি করা"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS agent_memory (
                        id SERIAL PRIMARY KEY,
                        incident_id VARCHAR(255) UNIQUE,
                        failure_type VARCHAR(100),
                        failing_input TEXT,
                        patched_prompt TEXT,
                        embedding VECTOR(1536),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                conn.commit()

    def _get_embedding(self, text: str) -> list:
        """AWS Bedrock Titan দিয়ে টেক্সটের ভেক্টর এমবেডিং জেনারেট করা"""
        body = json.dumps({"inputText": text})
        response = self.bedrock.invoke_model(
            modelId="amazon.titan-embed-text-v1",
            contentType="application/json",
            accept="application/json",
            body=body
        )
        response_body = json.loads(response.get("body").read())
        return response_body.get("embedding")

    def store_fix(self, incident_id: str, failure_type: str, failing_input: str, patched_prompt: str):
        """স্মৃতিতে নতুন ফিক্স সেভ করা"""
        embedding = self._get_embedding(failing_input)
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO agent_memory (incident_id, failure_type, failing_input, patched_prompt, embedding)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (incident_id) DO UPDATE 
                    SET patched_prompt = EXCLUDED.patched_prompt;
                """, (incident_id, failure_type, failing_input, patched_prompt, embedding))
                conn.commit()

    def search_similar_fix(self, input_text: str, similarity_threshold=0.85):
        """RAG Search: মিল থাকা পুরোনো ফিক্স খুঁজে বের করা"""
        query_embedding = self._get_embedding(input_text)
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT failure_type, failing_input, patched_prompt,
                           1 - (embedding <=> %s::vector) AS similarity
                    FROM agent_memory
                    WHERE 1 - (embedding <=> %s::vector) > %s
                    ORDER BY similarity DESC LIMIT 1;
                """, (query_embedding, query_embedding, similarity_threshold))
                return cur.fetchone()

import os
import json
import boto3

class BedrockCostOptimizer:
    def __init__(self):
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.bedrock = boto3.client("bedrock-runtime", region_name=self.aws_region)
        # Models
        self.heavy_model = "anthropic.claude-3-5-sonnet-20240620-v1:0" # High Severity
        self.fast_model = "amazon.nova-micro-v1:0"                     # Low/Medium Severity

    def generate_fix(self, prompt: str, severity: str = "LOW") -> dict:
        """
        Severity অনুযায়ী স্মার্ট রাউটিং:
        - HIGH / CRITICAL -> Claude 3.5 Sonnet (Deep Reasoning)
        - LOW / MEDIUM   -> Amazon Nova Micro (Fast & Low-Cost)
        """
        selected_model = self.heavy_model if severity.upper() in ["HIGH", "CRITICAL"] else self.fast_model

        if "claude" in selected_model:
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}]
            })
        else: # Amazon Nova Format
            body = json.dumps({
                "inferenceConfig": {"max_new_tokens": 1000},
                "messages": [{"role": "user", "content": [{"text": prompt}]}]
            })

        response = self.bedrock.invoke_model(
            modelId=selected_model,
            contentType="application/json",
            accept="application/json",
            body=body
        )
        
        response_body = json.loads(response.get("body").read())
        
        # Parse Response
        if "claude" in selected_model:
            output_text = response_body["content"][0]["text"]
        else:
            output_text = response_body["output"]["message"]["content"][0]["text"]

        return {
            "model_used": selected_model,
            "response": output_text
        }

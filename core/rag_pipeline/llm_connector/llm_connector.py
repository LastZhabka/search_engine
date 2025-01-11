from openai import AzureOpenAI


class LLMConnector:
    def __init__(self,):
        self.client = AzureOpenAI(
            api_key=open("core/rag_pipeline/llm_connector/api_key.txt", "r").read(),
            api_version="2024-10-21",
            azure_endpoint="https://hkust.azure-api.net"
        )
        self.model="gpt-35-turbo"

    def complete_text(self, prompt) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role" : "system", "content" : "You are helpful assistant."},
                {"role" : "user", "content" : prompt},
            ]
        )
        return (response.choices[0].message.content)


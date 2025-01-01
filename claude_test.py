import anthropic
import base64

api_key = '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'

with open('AMD_10K_part_1.pdf', 'rb') as file:
    file_content = base64.standard_b64encode(file.read()).decode('utf-8')

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key = api_key,
)
message = client.beta.messages.create(
    model="claude-3-5-sonnet-20241022",
    betas=["pdfs-2024-09-25"],
    max_tokens=8192,
    messages=[
        {"role": "user", 
         "content": [
         {
             "type": "document",
             "source": {
                 "type": "base64",
                 "media_type": "application/pdf",
                 "data": file_content
             }
         },
         {"type": "text", "text": "Please analyze this PDF file and give me a summary"}
         ]
        }
    ]
)
print(message.content)
print(type(message.content))
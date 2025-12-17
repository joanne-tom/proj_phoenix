from google import genai

client = genai.Client(
    api_key="AIzaSyDNlsBJ6B0EaU83fFS-9sx9HwgR6hBf2YA"
)

for model in client.models.list():
    print(model.name)

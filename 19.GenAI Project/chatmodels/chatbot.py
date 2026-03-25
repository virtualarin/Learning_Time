from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

print("Choose your AI mode!")
print("Press 1 for Comedy mode")
print("Press 2 for Motivational mode")
print("Press 3 for Data scientist mode")

choice = input("Enter your choice (1, 2, or 3): ")
if choice == "1":
    messages = [
        SystemMessage(content="You are a comedian"),
    ]
elif choice == "2":
    messages = [
        SystemMessage(content="You are a motivational speaker"),
    ]
elif choice == "3":
    messages = [
        SystemMessage(content="You are a professional data scientist"),
    ]
else:
    print("Invalid choice. Exiting.")
    exit()



messages = [
    SystemMessage(content=messages[0].content),
]

while True:
    print("Type 'exit' to quit.")
    prompt = input("You: ")
    messages.append(HumanMessage(content=prompt))
    if prompt == "exit":
        break
    response = model.invoke(messages)
    messages.append(AIMessage(content=response.content))
    print(response.content)

print(messages)
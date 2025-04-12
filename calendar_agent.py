import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from calendar_factory import AVAILABLE_FUNCTIONS
from datetime import datetime

# Scopes for google calendar API
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

LOG_FILE = "conversation_log.json"

def log_conversation(user_input, agent_response, tool_calls):
    serialized_tool_calls = []
    if tool_calls:
        for tool_call in tool_calls:
            serialized_tool_calls.append({
                "id": tool_call.id,
                "function": tool_call.function.name,
                "arguments": tool_call.function.arguments
            })

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "agent_response": agent_response,
        "tool_calls": serialized_tool_calls
    }

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r+", encoding="utf-8") as file:
            try:
                logs = json.load(file)
            except json.JSONDecodeError:
                logs = []
            logs.append(log_entry)
            file.seek(0)
            json.dump(logs, file, indent=4)
    else:
        with open(LOG_FILE, "w", encoding="utf-8") as file:
            json.dump([log_entry], file, indent=4)


# Calendar agent responsible for managing Google Calendar
def calendar_agent(content, messages):
    user_message = {"role": "user", "content": content}
    messages.append(user_message)

    with open("tools.json", "r") as file:
        tools = json.load(file)

    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, tools=tools, tool_choice="auto"
    )

    result = response.choices[0].message
    tool_calls = result.tool_calls

    log_conversation(content, result.content, tool_calls)

    if tool_calls:
        messages.append(result)

        for tool_call in tool_calls:
            print(f"Calendar agent is calling function: {tool_call.function.name} with params {tool_call.function.arguments}")

            function_to_call = AVAILABLE_FUNCTIONS[tool_call.function.name]
            function_args = json.loads(tool_call.function.arguments)

            if function_to_call:
                function_response = function_to_call(**function_args)
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": tool_call.function.name,
                        "content": function_response,
                    }
                )

        second_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )

        second_result = second_response.choices[0].message

        log_conversation(content, second_result.content, tool_calls)

        return second_result.content

    return result.content

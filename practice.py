import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

orders = {
    "12345": "Shipped, arriving Tuesday",
    "67890": "Still processing",
    "11111": "Delivered Monday"
}

def look_up_order(order_id):
    return orders.get(order_id, "Order not found")

tools = [
    {
        "name": "look_up_order",
        "description": "Look up the status of a customer's order using their order ID. Use this whenever a customer asks about their order.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The customer's order ID, for example '12345'"
                }
            },
            "required": ["order_id"]
        }
    }
]

def ask_agent(question):
    # STEP 1: Send the question to Claude, along with the tool menu
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        tools=tools,
        messages=[{"role": "user", "content": question}]
    )

    # STEP 2: Did Claude decide to use the tool?
    if message.stop_reason == "tool_use":
        tool_block = next(b for b in message.content if b.type == "tool_use")
        order_id = tool_block.input["order_id"]

        # HUMAN-IN-THE-LOOP: pause and ask for approval before running
        print(f"\n🤖 Claude wants to look up order: {order_id}")
        approval = input("Approve this lookup? (yes/no): ")

        if approval.lower() != "yes":
            return "Lookup cancelled by human."

        # STEP 3: only runs if the human approved
        result = look_up_order(order_id)

        # STEP 4: Hand the result back to Claude so it can write a final answer
        followup = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            tools=tools,
            messages=[
                {"role": "user", "content": question},
                {"role": "assistant", "content": message.content},
                {"role": "user", "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_block.id,
                    "content": result
                }]}
            ]
        )
        return followup.content[0].text
    else:
        return message.content[0].text

# test it
print(ask_agent("What's the status of order 12345?"))
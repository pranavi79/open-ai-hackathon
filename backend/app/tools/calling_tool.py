import os
from dotenv import load_dotenv
from agents import function_tool
from twilio.rest import Client

load_dotenv()

client = Client(os.getenv("ACCOUNT_SID"), os.getenv("AUTH_TOKEN"))

@function_tool
def calling_tool(hospital_number:str ,message:str) -> None:
    """Dials one or more phone numbers from a Twilio phone number."""
    client.calls.create(
        to=hospital_number,
        from_=os.getenv("TWILIO_PHONE_NUMBER"),
        twiml=f"<Response><Say>{message}</Say></Response>",
    )


if __name__ == "__main__":
    calling_tool("","")
# chatbot.py
import asyncio
import litellm
import parlant.sdk as p

# Initialize Parlant agent and server
async def initialize_parlant():
    async with p.Server(nlp_service=p.NLPServices.litellm) as server:
        agent = await server.create_agent(
            name="Kyma",
            description="Is empathetic and calming to the patient."
        )
        
        # Create a session for the user to interact with
        session = await agent.create_session()
        return server, session

# Function to get response from Parlant agent
async def get_response(session, prompt):
    event = await session.create_event(kind="message", source="customer", message=prompt)
    responses = await session.list_events(kinds=["message"], sources=["agent"])
    return responses[-1].message if responses else "No response."

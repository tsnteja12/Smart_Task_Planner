from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import json # Used to parse the structured JSON output from the LLM
from google import genai
from google.genai import types

# ---------------------- 1. CONFIGURATION AND INITIAL SETUP ---------------------------------

# Load environment variables  from the .env file
load_dotenv()
LLM_API_KEY = os.getenv("GEMINI_API_KEY") 

# Initialize the Flask app
app = Flask(__name__)

# Initialize the Gemini Client
try:
    if not LLM_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    client = None

# ----------- 2. CORE LLM REASONING FUNCTION -----------------------

def generate_tasks_with_llm(goal: str):
    """
    Uses the Gemini model to break down a goal into structured tasks.
    This directly addresses the LLM Usage Guidance and Objective.
    """
    
    # The Prompt, designed to force structured output for easy API consumption
    system_instruction = (
        "You are a Smart Task Planner AI. Your primary objective is to break down a high-level goal into a comprehensive "
        "list of actionable tasks. You must be accurate with timeline logic and dependencies."
    )
    
    prompt = f"Goal to Breakdown: \"{goal}\". Break down this goal into actionable tasks with suggested deadlines and dependencies. The dependencies should refer to the 'task_name' of preceding tasks."

    # Define the exact JSON schema the model MUST follow (Structured Output)
    response_schema = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "goal": types.Schema(type=types.Type.STRING, description="The original goal provided by the user."),
            "plan": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "task_name": types.Schema(type=types.Type.STRING, description="A single, clear, actionable task."),
                        "suggested_deadline": types.Schema(type=types.Type.STRING, description="A relative deadline, e.g., 'Day 3', 'End of Week 1'."),
                        "dependencies": types.Schema(
                            type=types.Type.ARRAY,
                            items=types.Schema(type=types.Type.STRING),
                            description="List of task_names that must be completed before this task starts. Use ['None'] if it has no dependencies."
                        )
                    },
                    required=["task_name", "suggested_deadline", "dependencies"]
                )
            )
        },
        required=["goal", "plan"]
    )
    
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        # This is the key part for Structured Output!
        response_mime_type="application/json", 
        response_schema=response_schema
    )

    try:
        # Call the Gemini API
        response = client.models.generate_content(
            model='gemini-2.5-flash', # A fast and highly capable model for reasoning and structure
            contents=[prompt],
            config=config,
        )

        # The response text will be a valid JSON string, ready to parse
        task_plan = json.loads(response.text)
        return task_plan

    except Exception as e:
        # Handle API errors, network issues, or JSON parsing failures
        print(f"LLM API Call Error: {e}")
        raise

# ------------------ 3. API ENDPOINT (FLASK ROUTE) -----------------------

@app.route('/api/v1/plan', methods=['POST'])
def generate_plan():
    """
    Backend API to process input & generate plan.
    """
    if not client:
         return jsonify({"error": "LLM client not initialized. Check API Key in .env file."}), 503

    # Get the Goal text from the request body
    data = request.get_json()
    goal_text = data.get('goal_text')

    if not goal_text:
        return jsonify({"error": "Missing 'goal_text' in request body."}), 400

    try:
        # Call the core LLM function
        task_plan = generate_tasks_with_llm(goal_text)

        # Output: Task breakdown, dependencies, estimated timelines (as JSON)
        return jsonify(task_plan), 200

    except Exception as e:
        # Simple error handling for the API
        return jsonify({"error": f"Failed to generate task plan: {e}"}), 500

if __name__ == '__main__':
    # Run the server. Using 0.0.0.0 makes it accessible on the network if needed, 
    # but for local testing, it runs on http://127.0.0.1:5000/
    print("Starting Flask server on http://127.0.0.1:5000/")
    app.run(debug=True)
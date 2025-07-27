@app.post("/prompt")
def generate_prompt(request: PromptRequest):
    input_text = request.input
    prompt_type = request.type

    # Define the different prompt instructions
    instructions = {
        "next-line": f"Continue the next line of this verse: {input_text}",
        "rewrite": f"Rewrite the following lyrics in a different style: {input_text}",
        "hook": f"Write a catchy chorus (hook) based on: {input_text}",
        "finish": f"Finish this short verse: {input_text}",
        "inspire": f"Generate creative inspiration based on: {input_text}",
        "finish-verse": f"Complete the verse based on this start: {input_text}"  # <-- add this
    }

    if prompt_type not in instructions:
        return {"result": f"Unknown prompt type: {prompt_type}"}

    full_prompt = instructions[prompt_type]

    # Simulated AI output (replace with real call)
    ai_output = f"{instructions[prompt_type]} 🔥"

    return {"result": ai_output}

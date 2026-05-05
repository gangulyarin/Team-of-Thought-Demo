import subprocess

# ---------- Config ----------
MODEL = "qwen2.5-coder:3b-instruct-q4_K_M"  # Ollama Qwen model

# ---------- Function to run Ollama ----------
def run_ollama(prompt, max_tokens=200):
    """
    Calls Ollama CLI with Qwen model to generate text
    """
    try:
        result = subprocess.run(
            ["ollama", "run", MODEL, prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

# ---------- Agents ----------
def math_agent(question):
    prompt = f"Solve the math problem step by step:\n{question}\nAnswer:"
    return run_ollama(prompt)

def code_agent(question):
    prompt = f"Write Python code for the following problem:\n{question}\nCode:"
    return run_ollama(prompt)

def general_agent(question):
    prompt = f"Answer the following question clearly:\n{question}\nAnswer:"
    return run_ollama(prompt)

# ---------- Orchestrator ----------
def orchestrator(question):
    q = question.lower()

    # Simple routing rules
    if any(word in q for word in ["sum", "integral", "solve", "math", "equation"]):
        agent = "math"
        result = math_agent(question)
    elif any(word in q for word in ["code", "python", "program", "function"]):
        agent = "code"
        result = code_agent(question)
    else:
        agent = "general"
        result = general_agent(question)

    return f"[Agent used: {agent}]\n{result}"

# ---------- Main loop ----------
if __name__ == "__main__":
    print("Team-of-Thoughts demo using Ollama + Qwen\nType 'exit' to quit")
    while True:
        q = input("\nAsk something: ")
        if q.lower() == "exit":
            break
        print("\n" + orchestrator(q))
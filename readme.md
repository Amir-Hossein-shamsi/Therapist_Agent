# 🧠 Therapist Agent

Welcome to **Therapist Agent** – an intelligent conversational agent that dynamically adapts its responses based on the user's emotional or logical needs. Powered by [LangChain](https://python.langchain.com/), [LangGraph](https://github.com/langchain-ai/langgraph), and [Groq LLMs](https://console.groq.com/), Decomond can act as both a compassionate therapist and a purely logical assistant.

---

## ✨ Features

- **Automatic Message Classification:**  
  Detects whether a user's message requires an _emotional_ or _logical_ response using an LLM-based classifier.

- **Dual-Persona Response:**

  - **Therapist Agent:** Offers empathy, emotional support, and thoughtful questions.
  - **Logical Agent:** Delivers factual, concise, and direct answers without emotional context.

- **Stateful Conversation:**  
  Maintains conversation history and adapts responses accordingly.

- **Easy to Run:**  
  Simple CLI interface for interactive chatting.

---

## 🚀 Quickstart

1. **Clone the repository and install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

2. **Set up your Groq API key:**

   - Copy `.env.example` to `.env` and add your key:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     ```

3. **Run the agent:**

   ```sh
   python [agent.py](http://_vscodecontentref_/0)
   ```

4. **Chat away!**  
   Type your message and press Enter. Type `exit` to quit.

---

## 🛠️ How It Works

The agent's flow is managed by a [LangGraph](https://github.com/langchain-ai/langgraph) state machine:

1. **Classification:**  
   Each user message is classified as either `emotional` or `logical` by an LLM.

2. **Routing:**  
   Based on the classification, the message is routed to either the therapist or logical agent.

3. **Response Generation:**

   - **Therapist Agent:** Responds with empathy and emotional support.
   - **Logical Agent:** Responds with facts and logical reasoning.

4. **Conversation Loop:**  
   The process repeats for each new user message.

---

## 📁 File Structure

- [`agent.py`](agent.py): Main conversational agent logic.
- `.env.example`: Example environment file for API keys.
- `readme.md`: This documentation.

---

## 🧩 Example Conversation

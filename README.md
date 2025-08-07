<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
</head>
<body>

  <h1>📊 CSV Chat Assistant</h1>
  <p><strong>Natural Language Query Tool for CSV Data — Powered by Streamlit, LangChain, and Groq</strong></p>

  <p>This web app allows users to upload CSV files and interact with their data using plain English questions. It's ideal for data analysts, business users, and students looking to explore data without writing complex queries.</p>

  <h2>🚀 Features</h2>
  <ul>
    <li>Upload any <code>.csv</code> file</li>
    <li>Ask natural language questions about your data</li>
    <li>Instant EDA Summary: shape, columns, statistics</li>
    <li>Built with LangChain + Groq using <code>llama3-70b-8192</code></li>
    <li>Session-based chat history</li>
    <li>UI built with Streamlit</li>
  </ul>

  <h2>🛠️ Tech Stack</h2>
  <ul>
    <li><strong>Frontend:</strong> Streamlit</li>
    <li><strong>LLM:</strong> LangChain + Groq API</li>
    <li><strong>Model:</strong> llama3-70b-8192</li>
    <li><strong>Language:</strong> Python 3.10+</li>
    <li><strong>Environment:</strong> dotenv</li>
  </ul>

  <h2>📂 File Structure</h2>
  <pre>
📁 csv-chat-assistant
├── .env                  # GROQ_API_KEY here
├── app.py                # Main Streamlit script
├── requirements.txt      # Dependencies
└── README.html           # This file
  </pre>

  <h2>⚙️ Setup Instructions</h2>

  <h3>1. Clone the Repository</h3>
  <pre>git clone https://github.com/your-username/csv-chat-assistant.git
cd csv-chat-assistant</pre>

  <h3>2. Create Virtual Environment</h3>
  <pre>python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate</pre>

  <h3>3. Install Dependencies</h3>
  <pre>pip install -r requirements.txt</pre>

  <h3>4. Set Groq API Key</h3>
  <p>Create a <code>.env</code> file:</p>
  <pre>GROQ_API_KEY=your_groq_api_key_here</pre>

  <h3>5. Run the App</h3>
  <pre>streamlit run app.py</pre>

  <h2>✅ Example Questions</h2>
  <ul>
    <li>How many rows are in the dataset?</li>
    <li>What is the average salary?</li>
    <li>Show me the top 5 entries sorted by revenue.</li>
  </ul>

  <h2>📌 Notes</h2>
  <ul>
    <li>Ensure the CSV is clean and small enough to load.</li>
    <li>Uses llama3-70b-8192 on Groq for fast performance.</li>
    <li>Built for demo, not production-scale CSV analysis.</li>
  </ul>

  <h2>📄 License</h2>
  <p>This project is licensed under the <strong>MIT License</strong>.</p>

  <h2>👨‍💻 Author</h2>
  <p><strong>Talha Zulfiqar</strong><br>
  <a href="https://www.linkedin.com/in/talhazulfiqar/">LinkedIn</a>

  <p>✨ Crafted with precision by <strong>Talha Zulfiqar</strong></p>

</body>
</html>

  🧠 Naturalborne — Intelligent Calculus Workspace

 Author:  Jonovi Gayle  
 Student ID:  20234624  

 

  🚀 Overview

Naturalborne is an advanced AI-powered calculus assistant built using  Streamlit  and  AnythingLLM . It provides a structured environment for solving, learning, and analyzing calculus problems with intelligent guidance and customizable interaction modes.

 

  🔹 Features

   Intelligent Chat Interface
- Embedded AI assistant powered by AnythingLLM
- Real-time calculus problem solving
- Step-by-step reasoning and explanations

   Working Modes
-  Step by Step  — detailed reasoning  
-  Exam Assistance  — concise, structured answers  
-  Concept Tutoring  — explanation-first learning  
-  Error Checking  — identifies and corrects mistakes  

   Prompt System
- One-click calculus prompts  
- Topic-based library (Limits, Derivatives, Integrals, Applications)  
- Custom prompt builder  
- Mode + Instructions + Question structure  

   UI / UX
- Auto-resizing embedded chat  
- Modern glassmorphism design  
- Multiple themes  
- Responsive layout  

 

  🧩 System Architecture

User Interface (Streamlit)  
        ↓  
Prompt Builder + Mode Injection  
        ↓  
AnythingLLM Embed  
        ↓  
LLM Backend  
        ↓  
Response → UI  

 

  ⚠️ Known Limitation

AnythingLLM embed does not reliably render LaTeX.

   Current Solution
- Unicode math symbols (π, ∫, √, ≤, ≥)  
- Plain-text math (x^2, (a/b))  

   Future Fix
- Integrate KaTeX or MathJax  

 

  🛠️ Installation

```bash
git clone <your-repo-url>
cd naturalborne
pip install streamlit
streamlit run app.py
```

Ensure AnythingLLM runs on:
http://localhost:3001

 

  🎯 Usage

1. Select working mode  
2. Choose or create prompt  
3. Inject into chat  
4. Send and receive solution  

 

  🧠 Intelligent Systems Concepts

- Human-AI interaction design  
- Prompt engineering  
- Adaptive system behavior  
- Interface-driven intelligence  

 

  🎓 Academic Purpose

Developed for an  Intelligent Systems  course to demonstrate applied AI in education.

 

  🔮 Future Enhancements

- LaTeX rendering (MathJax/KaTeX)  
- Chat history  
- Graph visualization  
- Voice input  
- Auto-send prompts  

 

  📌 Demo Tip

Demonstrate the same problem using different modes to show adaptive intelligence.

# CodePilot AI 🚀
> Interactive, AI-Powered Coding Education Platform built on Google Gemini 2.0.

CodePilot AI merges a high-density IDE workbench, containerized multi-language compilation, step-by-step visual debugger, automated test generator, and personalized Gemini pedagogical tutoring.

## 🌟 Key Features
- **4-Pane IDE Workbench**: Monaco-like editor, WebAssembly + containerized execution, visual debugger, and xterm console.
- **Gemini AI Pedagogical Tutor**:
  - Code Explanation with dynamic Mermaid data structure flowcharts.
  - AI Debugger with root-cause analysis, unified diff preview, and one-click patch application.
  - Socratic tutor with adaptive skill-level personas (Beginner / Intermediate / Senior).
  - FAANG-style Mock Technical Interview Simulator with live evaluation rubrics.
- **I/O Test Bench & Profiler**: Edge case generator, hidden test runner, and empirical Big-$ time/space complexity analysis.
- **Adaptive Curriculum & Gamification**: BKT skill decay alerts, XP, streaks, and collaborative coding rooms.

## 🚀 Quickstart

### 1. Run Interactive Prototype in Browser
Open index.html in any modern web browser or serve locally:
`ash
npx serve .
# or
python -m http.server 3000
`

### 2. Run Backend AI Microservices with Docker
`ash
export GEMINI_API_KEY=your-gemini-api-key
docker compose up -d
`
API docs available at http://localhost:8000/docs.

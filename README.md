# 🧠 Scientific Review MCP Platform

A Modular Computation Platform (MCP) designed to help scientists **write, refine, and rehearse the peer-review process** before formal submission. Built to mimic and accelerate academic review workflows using intelligent agents.

---

## 🚀 Purpose

The peer-review process is slow, inconsistent, and difficult—especially for early-career researchers. This platform helps researchers **practice writing papers**, **receive structured feedback**, and even **simulate full review cycles**, reducing the time and uncertainty of actual journal submission.

---

## 🤖 How It Works

This system uses multiple cooperating MCP agents:

### 🧑‍🔬 Reviewer Agents (x3)
- Each focuses on **a different review lens**: methodology, novelty, and clarity.
- Provide scores, constructive criticism, and a **decision (e.g., revise, accept, reject)**.
- Can be **tailored to specific journal guidelines** for discipline-aligned feedback.

### 🔍 Background Agent
- **Summarizes your draft** and **extracts key claims**.
- Searches **arXiv** for related work or prior art to assess originality and relevance.
- Flags overlapping contributions or missing citations.

### 🔁 Rebuttal Loop
- After receiving reviews, you can:
  - Respond with **rebuttals**,
  - Submit **revisions**, and
  - Generate **response letters** (just like in a real peer-review process).
  
This encourages a realistic understanding of **scientific discourse** and helps practice **effective response strategies**.

---

## 📦 Features

- ✅ Paper submission and revision loop
- ✅ Reviewer-style feedback from multiple perspectives
- ✅ Journal-specific review emulation
- ✅ Automatic related-work search via arXiv
- ✅ Rebuttal and response letter drafting


--- 

## How to run?

### 📚 Tutorials

To get started, follow these steps:

1. **Install Dependencies**  
    Ensure you have Python 3.8+ installed. Then, install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

2. **Run the Platform**  
    Launch the MCP platform locally:
    ```bash
    python main.py
    ```

3. **Explore the Tutorials**  
    Visit the tutorials to learn how to:
    - Submit your first paper draft.
    - Configure reviewer agents.
    - Simulate a full review cycle.


# Next Word Prediction Using LSTM Neural Networks

**A Deep Learning and Recurrent Neural Network Based Sequential Language Modeling Application**

---

### Project Members
- **Abhishek Mishra** — Roll ID: `VU2F2324006`
- **Aryan Fursule** — Roll ID: `VU2F2324032`

### Institutional Affiliation
- **Institution:** Vasantdada Patil Pratishthan's College of Engineering & Visual Arts
- **Department:** Department of Artificial Intelligence and Data Science
- **Faculty Guide:** Prof. Ganesh Patil
- **Academic Year:** 2026-27

---

## 🚀 Overview
This repository contains the complete implementation and technical documentation for the Mini Project: **Next Word Prediction Using LSTM Neural Networks**.

The project uses a deep stacked 2-layer Long Short-Term Memory (LSTM) recurrent network with 128-dimensional dense word embeddings to predict the most probable continuation tokens given arbitrary sentence context.

### Key Highlights
- **Architecture:** Embedding Layer (128-d) -> 2-Layer Stacked LSTM (256 hidden units, dropout 0.2) -> Linear Projection Layer.
- **Performance:** Loss: 0.0106, Perplexity: 1.01, Top-1 Accuracy: 100.0%, Top-5 Accuracy: 100.0%.
- **Interactive UI:** Built with Streamlit, providing real-time top-k candidate probability charts and multi-word auto-complete sequence simulation.
- **Report Document:** Fully formatted academic report [`Next_Word_Prediction_Report.docx`](./Next_Word_Prediction_Report.docx) formatted matching the required template and containing 4 high-resolution embedded screenshots from the live app.

---

## 📁 Repository Structure
```text
├── Next_Word_Prediction_Report.docx   # Academic project report with all sections, tables & screenshots
├── Sentiment_Analysis_Report.docx     # Reference formatting template provided
├── app.py                             # Interactive Streamlit Web Application
├── build_and_train.py                 # PyTorch model training & preprocessing pipeline
├── next_word_lstm.pth                 # Saved model weights
├── metadata.json                      # Vocabulary mappings & training history
├── capture_all_screens.py             # Automated screenshot capture script
├── screenshot_1_overview.png          # App screenshot: Overview & Architecture
├── screenshot_2_predictor.png         # App screenshot: Next Word Predictor with prompt
├── screenshot_3_evaluation.png        # App screenshot: Evaluation curves & benchmark table
├── screenshot_4_nlp_prompt.png        # App screenshot: Domain test prompt execution
├── run_app.bat                        # 1-Click batch launcher for the web app
└── README.md                          # Documentation
```

---

## 💻 How to Run the Web Application
Double-click `run_app.bat` or run the following command in terminal:
```bash
python -m streamlit run app.py
```
Open your browser at `http://localhost:8501`.

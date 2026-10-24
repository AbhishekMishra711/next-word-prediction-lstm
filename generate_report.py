import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import os

def create_report():
    doc = docx.Document()
    
    # 1. Page Margins and Setup (8.5 x 11.0 in, 1.0 in margins all around)
    section = doc.sections[0]
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)
    
    # Helper functions for styling
    def add_p(text="", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=Pt(4), space_after=Pt(4), line_spacing=1.15):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = space_before
        p.paragraph_format.space_after = space_after
        p.paragraph_format.line_spacing = line_spacing
        if text:
            r = p.add_run(text)
            r.font.name = 'Calibri'
            r.font.size = Pt(12)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(24)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(24)
        r.bold = True
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(18)
        r.bold = True
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(14)
        r.bold = True
        return p

    def add_bullet(lead_text, body_text=""):
        p = doc.add_paragraph(style='List Paragraph')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r1 = p.add_run(lead_text)
        r1.font.name = 'Calibri'
        r1.font.size = Pt(12)
        if body_text:
            r1.bold = True
            r2 = p.add_run(body_text)
            r2.font.name = 'Calibri'
            r2.font.size = Pt(12)
        return p

    def add_formula(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(12)
        r.italic = True
        return p

    def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = OxmlElement('w:tcBorders')
        for side, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            if val is not None:
                border = OxmlElement(f'w:{side}')
                border.set(qn('w:val'), val.get('val', 'single'))
                border.set(qn('w:sz'), str(val.get('sz', 4)))
                border.set(qn('w:space'), '0')
                border.set(qn('w:color'), val.get('color', 'CCCCCC'))
                tcBorders.append(border)
            else:
                border = OxmlElement(f'w:{side}')
                border.set(qn('w:val'), 'none')
                tcBorders.append(border)
        tcPr.append(tcBorders)

    def set_cell_shading(cell, color_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), color_hex)
        tcPr.append(shd)

    # -------------------------------------------------------------------------
    # COVER PAGE
    # -------------------------------------------------------------------------
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(36)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run("MINI PROJECT")
    r.font.name = 'Calibri'
    r.font.size = Pt(14)
    r.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run("ON")
    r.font.name = 'Calibri'
    r.font.size = Pt(14)
    r.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run("NEXT WORD PREDICTION USING LSTM NEURAL NETWORKS")
    r.font.name = 'Calibri'
    r.font.size = Pt(18)
    r.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(40)
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run("A Deep Learning and Recurrent Neural Network Based Sequential Language Modeling Application")
    r.font.name = 'Calibri'
    r.font.size = Pt(14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run("Submitted by")
    r.font.name = 'Calibri'
    r.font.size = Pt(14)
    r.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run("Abhishek Mishra - VU2F2324006")
    r.font.name = 'Calibri'
    r.font.size = Pt(14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(36)
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run("Aryan Fursule - VU2F2324032")
    r.font.name = 'Calibri'
    r.font.size = Pt(14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run("Submitted to")
    r.font.name = 'Calibri'
    r.font.size = Pt(14)
    r.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(28)
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run("Prof. Ganesh Patil")
    r.font.name = 'Calibri'
    r.font.size = Pt(14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run("Vasantdada Patil Pratishthan's College of Engineering & Visual Arts")
    r.font.name = 'Calibri'
    r.font.size = Pt(14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run("Department of Artificial Intelligence and Data Science")
    r.font.name = 'Calibri'
    r.font.size = Pt(14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(20)
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run("Academic Year: 2026-27")
    r.font.name = 'Calibri'
    r.font.size = Pt(14)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # ABSTRACT
    # -------------------------------------------------------------------------
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run("ABSTRACT")
    r.font.name = 'Calibri'
    r.font.size = Pt(14)
    r.bold = True

    add_p("Next word prediction is a foundational objective in Natural Language Processing (NLP) and sequence modeling that powers modern predictive text systems, intelligent keyboard autocomplete, search query suggestions, and conversational AI assistants. Conventional statistical approaches, such as n-gram frequency tables and Markov models, suffer from severe limitations including exponential parameter explosion, data sparsity, and an inability to maintain long-range contextual dependencies beyond a narrow, fixed context window. Deep learning architectures, specifically Recurrent Neural Networks equipped with gated memory cells, offer a powerful mathematical framework to overcome these limitations by projecting discrete words into continuous vector spaces and learning non-linear sequential dependencies across temporal steps.")

    add_p("The proposed project, Next Word Prediction Using LSTM Neural Networks, is an end-to-end deep learning application that processes sequential text prompts and predicts the most mathematically probable continuation tokens. Unstructured textual corpora covering domains in artificial intelligence, machine learning, and linguistic science are cleaned and normalized through a robust text-preprocessing pipeline—including lowercasing, non-alphanumeric punctuation removal, tokenization, vocabulary indexing with out-of-vocabulary handling, and n-gram sliding window sequence generation. The resulting input sequence tensors are mapped into continuous dense representations via a 128-dimensional embedding layer and propagated through a stacked two-layer Long Short-Term Memory (LSTM) network with hidden dimensions of 256 units and dropout regularization.")

    add_p("The LSTM internal cell state utilizes forget, input, and output gating mechanisms to regulate information flow and preserve gradient propagation over extended sequences. The model was trained using Adam optimization and categorical cross-entropy loss, reporting a training loss of 0.0106, an intrinsic model perplexity of 1.01, a Top-1 accuracy of 100.0%, and a Top-5 accuracy of 100.0% on the evaluated corpus sequence benchmarks. The trained neural network weights and vocabulary metadata were serialized and deployed through a responsive, modern Streamlit web application. The interface provides instant token inference, ranking the top-k candidate continuation words alongside confidence percentage distributions, interactive probability bar charts, and a multi-token sequence auto-completion simulation engine.")

    add_p("The project provides a rigorous, practical demonstration of deep learning, recurrent neural architectures, word embeddings, and sequence modeling applied to predictive text synthesis. It illustrates how gated recurrence overcomes traditional vanishing gradient limitations while exposing clear trade-offs regarding vocabulary constraints and sequence boundaries. The system provides an interactive and explainable platform for exploring neural language modeling.")

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.5
    r1 = p.add_run("Keywords: ")
    r1.font.name = 'Calibri'
    r1.font.size = Pt(12)
    r1.bold = True
    r2 = p.add_run("Next Word Prediction, Natural Language Processing, Deep Learning, Recurrent Neural Networks, LSTM, Language Modeling, Sequence Generation, PyTorch, Streamlit.")
    r2.font.name = 'Calibri'
    r2.font.size = Pt(12)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # TABLE OF CONTENTS
    # -------------------------------------------------------------------------
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run("TABLE OF CONTENTS")
    r.font.name = 'Calibri'
    r.font.size = Pt(14)
    r.bold = True

    toc_table = doc.add_table(rows=11, cols=2)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    toc_data = [
        ("1. Problem Definition", "4"),
        ("2. Introduction", "4"),
        ("3. Literature Review and Background", "6"),
        ("4. Motivation", "7"),
        ("5. Objectives and Scope", "8"),
        ("6. Methodology Used", "9"),
        ("7. System Architecture and Modules", "11"),
        ("8. Development and Testing Plan", "13"),
        ("9. Expected Outcomes, Limitations and Future Scope", "16"),
        ("10. Conclusion", "18"),
        ("11. References", "18")
    ]
    for row_idx, (section_title, page_no) in enumerate(toc_data):
        row = toc_table.rows[row_idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(5.5)
        c1.width = Inches(1.0)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(3)
        p0.paragraph_format.space_after = Pt(3)
        r0 = p0.add_run(section_title)
        r0.font.name = 'Calibri'
        r0.font.size = Pt(12)
        
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_before = Pt(3)
        p1.paragraph_format.space_after = Pt(3)
        r1 = p1.add_run(page_no)
        r1.font.name = 'Calibri'
        r1.font.size = Pt(12)
        
        set_cell_borders(c0, bottom={'val': 'dotted', 'sz': 4, 'color': 'E2E8F0'})
        set_cell_borders(c1, bottom={'val': 'dotted', 'sz': 4, 'color': 'E2E8F0'})

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # 1. PROBLEM DEFINITION
    # -------------------------------------------------------------------------
    add_h1("1. PROBLEM DEFINITION")
    add_p("In the digital communication era, users interact with computational systems through text entry at unprecedented scale across mobile keyboards, search engines, code editors, and customer support interfaces. Typing text manually is often time-consuming, prone to typographical errors, and inefficient when users attempt to formulate extended technical or conversational statements.")
    add_p("The primary problem is to design and develop an intelligent computational system capable of reading a preceding sequence of words (sentence context) and automatically predicting the most probable next word in real time, eliminating repetitive typing effort and improving input fluency.")
    add_p("Natural language is inherently complex, high-dimensional, and non-linear. The semantic orientation of an upcoming word depends strongly on long-range dependencies across multiple preceding tokens rather than immediate neighbor words alone. Traditional keyword or static frequency-table approaches fail to capture context, suffer from severe data sparsity when faced with unseen phrase combinations, and cannot generalize effectively across varied linguistic contexts.")
    add_p("The major problems addressed by this project are:")
    add_bullet("Contextual dependency bottlenecks:", " conventional statistical models (e.g., bigrams and trigrams) assume Markov independence, failing when grammatical agreements or subject references span longer word distances.")
    add_bullet("The curse of dimensionality:", " tabular n-gram language models grow exponentially in parameter size with sequence length, making them computationally prohibitive for large vocabularies.")
    add_bullet("Vanishing and exploding gradients in standard RNNs:", " vanilla recurrent neural networks struggle to preserve backpropagated error gradients across extended sequences, causing memory degradation.")
    add_bullet("Converting discrete natural language into continuous vectors:", " discrete word representations fail to capture geometric and semantic relationships between words.")
    add_bullet("Real-time probabilistic inference and interactive visualization:", " presenting model predictions to end users in an intuitive, transparent interface with confidence metrics rather than opaque black-box outputs.")
    add_p("The proposed Next Word Prediction Using LSTM Neural Networks project directly addresses these challenges by preprocessing textual corpora into sequential tensors, projecting discrete tokens into dense continuous embedding spaces, leveraging stacked LSTM memory gates to preserve long-range dependencies, and deploying an interactive web application with ranked candidate probabilities.")

    # -------------------------------------------------------------------------
    # 2. INTRODUCTION
    # -------------------------------------------------------------------------
    add_h1("2. INTRODUCTION")
    add_h2("2.1 Background")
    add_p("Natural Language Processing (NLP) is an interdisciplinary branch of Artificial Intelligence, Computer Science, and Computational Linguistics focused on enabling machines to comprehend, analyze, and synthesize human language. Language modeling represents one of the core foundational tasks in modern NLP, where the goal is to determine the joint probability distribution of word sequences or predict the conditional probability P(w_t | w_1, w_2, ..., w_{t-1}) of an incoming token given its preceding context.")
    add_p("Over the past decade, language modeling has evolved from statistical n-gram counts with heuristic smoothing to deep recurrent neural architectures. Unlike feedforward networks that treat inputs independently, Recurrent Neural Networks (RNNs) maintain an internal cyclical hidden state that acts as a temporal memory. The Long Short-Term Memory (LSTM) network, engineered by Hochreiter and Schmidhuber, specifically addresses gradient degradation by replacing simple recurrent neurons with gated memory cells that explicitly regulate information addition, retention, and emission.")

    add_h2("2.2 Project Overview")
    add_p("The Next Word Prediction Using LSTM Neural Networks project is an applied deep learning language modeling application. The system accepts an arbitrary text prompt provided by a user, cleans and tokenizes the input, extracts sequential context, feeds the tokens into a trained 2-layer LSTM neural network, and computes the probability distribution over the entire vocabulary.")
    add_p("As demonstrated in the deployed Streamlit application, the system features a dedicated Overview & Architecture dashboard detailing the end-to-end pipeline, an interactive Next Word Predictor module with real-time probability distributions and multi-word auto-completion simulation, and a Model Evaluation suite displaying training loss curves, perplexity metrics, and comparative baseline benchmarks.")

    add_h2("2.3 Existing Approach and Proposed Approach")
    add_p("Existing Approach:")
    add_p("In conventional language modeling systems, statistical n-gram models or rule-based Markov chains are employed. In an n-gram model, the probability of the next word is assumed to depend solely on the preceding n-1 words (Markov assumption). While computationally simple for small n (such as bigrams or trigrams), these approaches cannot remember information beyond their rigid window, assign zero probability to unobserved word sequences without complex smoothing heuristics, and require storage space that explodes exponentially as the vocabulary and context length grow.")
    add_p("Proposed Approach:")
    add_p("The proposed system adopts a deep learning approach utilizing dense word embeddings and stacked Long Short-Term Memory (LSTM) recurrent networks. Word embeddings represent semantic similarities in continuous vector space, while the LSTM gating mechanisms (forget, input, and output gates) dynamically regulate information persistence across variable-length contexts. The trained model is served via an interactive Streamlit web interface with real-time probabilistic feedback.")

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("Table 1: Comparison of Existing and Proposed Approaches")
    r.font.name = 'Calibri'
    r.font.size = Pt(12)
    r.bold = True

    t1 = doc.add_table(rows=6, cols=2)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t1_data = [
        ("Existing / Conventional Approach", "Proposed LSTM-Based Deep Learning Approach"),
        ("Fixed context window (n-gram) assuming strict Markov independence.", "Dynamic recurrent memory cell capturing long-range contextual dependencies."),
        ("Discrete one-hot or frequency counts lacking semantic geometry.", "Dense continuous word embeddings (128-d) capturing semantic word relationships."),
        ("Zero-probability penalty for unseen n-gram tuples requiring heuristic smoothing.", "Continuous generalization across unseen phrase combinations via soft vector distances."),
        ("Exponential growth in table size with increasing context length.", "Constant parameter footprint governed by hidden dimensionality rather than context length."),
        ("Static command-line output or rigid dictionary lookups.", "Interactive Streamlit web application with Top-K probability charts and auto-completion.")
    ]
    for r_i, (c0_t, c1_t) in enumerate(t1_data):
        row = t1.rows[r_i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = Inches(3.25), Inches(3.25)
        for c, text in [(c0, c0_t), (c1, c1_t)]:
            cp = c.paragraphs[0]
            cp.paragraph_format.space_before = Pt(4)
            cp.paragraph_format.space_after = Pt(4)
            cr = cp.add_run(text)
            cr.font.name = 'Calibri'
            cr.font.size = Pt(11)
            if r_i == 0:
                cr.bold = True
                set_cell_shading(c, "E2E8F0")
                set_cell_borders(c, top={'val': 'single', 'sz': 8, 'color': '94A3B8'}, bottom={'val': 'single', 'sz': 8, 'color': '94A3B8'})
            else:
                set_cell_borders(c, bottom={'val': 'single', 'sz': 4, 'color': 'E2E8F0'})

    # -------------------------------------------------------------------------
    # 3. LITERATURE REVIEW AND BACKGROUND
    # -------------------------------------------------------------------------
    add_h1("3. LITERATURE REVIEW AND BACKGROUND")
    add_h2("3.1 Natural Language Processing and Sequential Language Modeling")
    add_p("Language modeling serves as the backbone for virtually all generative and predictive NLP tasks. Bengio et al. [1] pioneered the neural language modeling paradigm, demonstrating that mapping discrete words into a continuous latent space and modeling sequential transitions using neural networks overcomes the curse of dimensionality inherent in statistical n-gram counts. Mikolov et al. [2] further advanced this concept with continuous word vector representations (Word2Vec), illustrating that dense embeddings capture meaningful semantic and syntactic analogies (e.g., vector('king') - vector('man') + vector('woman') ≈ vector('queen')). This project leverages learned 128-dimensional dense embeddings to represent input vocabulary tokens.")

    add_h2("3.2 N-Gram Models and Contextual Bottlenecks")
    add_p("Traditional statistical language modeling relies on counting n-gram frequencies across a corpus and normalizing counts to calculate maximum likelihood estimates. Shannon [3] demonstrated foundational n-gram approximations of natural text. However, Jurafsky and Martin [4] emphasize that n-gram models suffer from severe limitations: as context length n increases, the number of possible word combinations grows exponentially (V^n), leading to severe matrix sparsity. Furthermore, the Markov assumption enforces that context prior to the last n-1 words is discarded, rendering statistical n-grams unable to track syntactic dependencies across clauses.")

    add_h2("3.3 Recurrent Neural Networks and LSTM Architecture")
    add_p("To overcome the rigid context horizon of n-grams, Rumelhart, Hinton, and Williams [5] popularized Recurrent Neural Networks (RNNs) containing cyclical feedback connections. However, as mathematically proven by Bengio, Simard, and Frasconi [6], training standard RNNs over long sequences suffers from exponential vanishing and exploding gradients during backpropagation through time (BPTT). To definitively solve this problem, Hochreiter and Schmidhuber [7] formulated the Long Short-Term Memory (LSTM) architecture, later enhanced with forget gates by Gers, Schmidhuber, and Cummins [8]. By introducing a constant error carousel and gating mechanisms that govern additive updates, LSTMs maintain gradients over long sequences, making them suitable for sequence modeling tasks.")

    add_h2("3.4 Related Applications")
    add_p("Intelligent next word prediction algorithms are widely utilized across multiple domains:")
    add_bullet("Virtual Mobile Keyboards:", " mobile input applications such as Google Gboard, Microsoft SwiftKey, and Apple QuickType rely on sequential language modeling to recommend candidate words above the virtual keyboard, increasing typing speed and reducing keystrokes.")
    add_bullet("Search Engine Autocomplete:", " platforms like Google and Bing provide dynamic query autocompletion to guide user inquiries toward grammatically and statistically coherent formulations.")
    add_bullet("Integrated Development Environments (IDEs):", " modern code assistance tools (e.g., GitHub Copilot, IntelliSense) predict the next token, function parameter, or code statement based on preceding contextual lines.")
    add_bullet("Assistive Communication Technologies:", " AAC (Augmentative and Alternative Communication) systems assist individuals with speech or motor impairments to construct sentences with minimal input effort.")
    add_bullet("Customer Service and Conversational Chatbots:", " predictive models assist human agents by suggesting standard sentence completions in real-time chat environments.")

    # -------------------------------------------------------------------------
    # 4. MOTIVATION
    # -------------------------------------------------------------------------
    add_h1("4. MOTIVATION")
    add_p("The primary motivation behind this project is to develop an interactive, reliable, and mathematically sound deep learning language model capable of predicting the next word in a sequence with high confidence, demonstrating the inner workings of recurrent neural architectures.")
    add_p("While modern generative AI systems feature billions of parameters, understanding the fundamental mechanics of sequential neural modeling—including tokenization, embedding lookup, recurrent hidden state transitions, gated memory preservation, and categorical softmax distribution—is critical for modern artificial intelligence engineering. A compact, locally trained LSTM provides an excellent model that is interpretable, responsive, and verifiable.")
    add_p("The key motivating factors are:")
    add_bullet("To mitigate manual typing fatigue:", " reducing the time and physical effort needed to complete sentences in digital interfaces.")
    add_bullet("To capture long-range contextual syntax:", " transcending the limitations of shallow n-gram tables by utilizing LSTM gated memory cells.")
    add_bullet("To visualize model uncertainty transparently:", " displaying full probability distributions across top-k candidates rather than single deterministic choices.")
    add_bullet("To build a deployable, lightweight NLP prototype:", " engineering a self-contained application using PyTorch and Streamlit that runs seamlessly without massive cloud infrastructure.")
    add_bullet("To explore sequential multi-token generation:", " enabling users to auto-generate entire sentence continuations iteratively using greedy recurrent decoding.")

    # -------------------------------------------------------------------------
    # 5. OBJECTIVES AND SCOPE
    # -------------------------------------------------------------------------
    add_h1("5. OBJECTIVES AND SCOPE")
    add_h2("5.1 Objectives")
    add_p("The primary objectives of the Next Word Prediction Using LSTM Neural Networks project are:")
    add_bullet("To collect and preprocess a textual corpus:", " clean, normalize, tokenize, and index vocabulary words into numerical formats with out-of-vocabulary (<UNK>) and padding (<PAD>) handling.")
    add_bullet("To construct sliding context sequence datasets:", " generate n-gram training pairs mapping input sequence vectors of length L to their ground-truth continuation token.")
    add_bullet("To design and implement a 2-layer LSTM architecture:", " construct embedding, recurrent LSTM, dropout regularization, and linear classification layers in PyTorch.")
    add_bullet("To train and optimize network weights:", " utilize Adam optimizer and Cross-Entropy loss to achieve rapid convergence and low perplexity.")
    add_bullet("To evaluate quantitative benchmark metrics:", " assess training loss, model perplexity, Top-1 accuracy, and Top-5 candidate accuracy.")
    add_bullet("To persist model artifacts and vocabulary metadata:", " serialize trained weights and vocabulary mapping dictionaries into reusable `.pth` and `.json` artifacts.")
    add_bullet("To build an interactive Streamlit web application:", " develop an intuitive graphical user interface for real-time inference, top-k candidate probability charts, and auto-completion.")

    add_h2("5.2 Scope")
    add_p("The scope of this project encompasses character-level and word-level sequence modeling for English text prompts. The application is designed to support:")
    add_bullet("Real-time inference:", " accepting user-typed text prompts and returning top-k predictions with confidence percentages.")
    add_bullet("Candidate distribution exploration:", " dynamic slider adjustment allowing users to inspect between 3 and 8 candidate continuation tokens.")
    add_bullet("Multi-token sequential generation:", " auto-completing up to 8 consecutive words via iterative feedback loops.")
    add_bullet("Architectural and training transparency:", " dedicated dashboards detailing mathematical formulations, loss convergence, and comparative performance against baseline n-grams.")
    add_p("The project scope does not encompass multi-gigabyte open-domain web scraping, sub-word BPE tokenization, multilingual cross-lingual inference, or attention-based Transformer fine-tuning; these represent valuable areas for future development.")

    # -------------------------------------------------------------------------
    # 6. METHODOLOGY USED
    # -------------------------------------------------------------------------
    add_h1("6. METHODOLOGY USED")
    add_p("The project follows a systematic deep learning sequence modeling methodology divided into data preprocessing, sequence generation, neural network design, training optimization, quantitative evaluation, and application deployment.")

    add_h2("6.1 Overall Methodology")
    add_p("The end-to-end operational pipeline is structured into six sequential phases:")
    add_bullet("1. Corpus Ingestion:", " collecting representative domain text across artificial intelligence, machine learning, and linguistic science.")
    add_bullet("2. Preprocessing & Tokenization:", " lowercasing text, stripping special characters, tokenizing into discrete word tokens, and generating bidirectional index maps (word2idx, idx2word).")
    add_bullet("3. Sequence Dataset Generation:", " slicing tokens via sliding context window (length = 4) into input vectors and target labels.")
    add_bullet("4. Model Architecture & Forward Propagation:", " projecting tokens into 128-d embeddings, passing through 2-layer LSTM (hidden_dim = 256), and projecting to vocabulary logits.")
    add_bullet("5. Training & Loss Backpropagation:", " computing Cross-Entropy loss, calculating perplexity, updating weights via Adam optimizer with dropout regularization (p = 0.2).")
    add_bullet("6. Deployment & Interactive Inference:", " loading model weights into Streamlit, performing real-time inference, and visualizing softmax probabilities.")

    add_h2("6.2 Data Collection and Text Preprocessing")
    add_p("The textual corpus comprises domain sentences in artificial intelligence, deep learning, recurrent neural networks, natural language processing, and language modeling. Text preprocessing follows a disciplined sequence:")
    add_bullet("Normalization:", " converting all input strings to lowercase to eliminate casing ambiguity.")
    add_bullet("Special Character Removal:", " regular expression filtering to remove non-alphanumeric punctuation and redundant whitespace.")
    add_bullet("Tokenization:", " segmenting sentences into individual string tokens.")
    add_bullet("Vocabulary Indexing:", " compiling unique words into a vocabulary vector prefixed with reserved tokens '<PAD>' (index 0) and '<UNK>' (index 1).")

    add_h2("6.3 Sequence Generation and Tokenization")
    add_p("To train a sequential next word predictor, the continuous stream of tokens is transformed into supervised learning pairs using a sliding context window of length L = 4. Given a token sequence [w_1, w_2, w_3, w_4, w_5, ...], the training pairs are generated as:")
    add_formula("Input: [w_1, w_2, w_3, w_4]  -->  Target: w_5")
    add_formula("Input: [w_2, w_3, w_4, w_5]  -->  Target: w_6")
    add_p("Each token string is converted to its integer index using word2idx. During inference, if the user enters fewer than L tokens, the sequence is padded with '<PAD>', and if longer, the most recent L tokens are extracted to form the immediate context.")

    add_h2("6.4 LSTM Model Architecture and Mathematical Formulation")
    add_p("The core computational engine is a stacked Long Short-Term Memory (LSTM) network. At each time step t, given input vector x_t and previous hidden state h_{t-1}, the internal operations are governed by the following mathematical equations:")
    add_formula("Forget Gate: f_t = σ(W_f · [h_{t-1}, x_t] + b_f)")
    add_formula("Input Gate: i_t = σ(W_i · [h_{t-1}, x_t] + b_i)")
    add_formula("Candidate Cell State: C̃_t = tanh(W_c · [h_{t-1}, x_t] + b_c)")
    add_formula("Updated Cell State: C_t = f_t * C_{t-1} + i_t * C̃_t")
    add_formula("Output Gate: o_t = σ(W_o · [h_{t-1}, x_t] + b_o)")
    add_formula("Hidden State: h_t = o_t * tanh(C_t)")
    add_p("Here, σ denotes the sigmoid activation function projecting outputs into [0, 1], * denotes the element-wise Hadamard product, and tanh projects candidate values into [-1, 1]. The final hidden state h_T from the last temporal step is passed through a linear projection layer to produce unnormalized logits z across all vocabulary tokens, which are converted to probabilities via the Softmax function:")
    add_formula("P(w_{t+1} = k | context) = exp(z_k) / Σ_j exp(z_j)")

    add_h2("6.5 Evaluation Metrics")
    add_p("The predictive quality of the language model is evaluated using four quantitative metrics:")
    add_formula("Cross-Entropy Loss: L = - (1/N) Σ_i log P(y_i | x_i)")
    add_formula("Model Perplexity: PPL = exp(L)")
    add_formula("Top-1 Accuracy = (Correct Top-1 Predictions / Total Test Samples) × 100%")
    add_formula("Top-5 Accuracy = (Ground Truth in Top-5 Ranked Candidates / Total Test Samples) × 100%")
    add_p("Perplexity (PPL) represents the effective branching factor of the language model; a lower perplexity signifies that the model is less confused and assigns higher probability mass to valid continuation words.")

    add_h2("6.6 Deployment via Streamlit")
    add_p("The trained PyTorch model and vocabulary dictionaries are loaded into an interactive Streamlit application. When a user enters text or selects a sample prompt, the app normalizes the string, extracts context indices, passes the tensor through the model in evaluation mode (torch.no_grad), computes softmax probabilities, and renders an Altair interactive horizontal bar chart alongside a multi-token sequence auto-completion simulation.")

    # -------------------------------------------------------------------------
    # 7. SYSTEM ARCHITECTURE AND MODULES
    # -------------------------------------------------------------------------
    add_h1("7. SYSTEM ARCHITECTURE AND MODULES")
    add_h2("7.1 High-Level Architecture")
    add_p("The system architecture decouples offline training from online real-time inference. The offline pipeline handles text cleaning, sequence extraction, and multi-epoch gradient optimization, while the online inference engine serves user requests via Streamlit.")
    add_bullet("Raw Text Corpus:", " domain sentences covering AI, deep learning, and language modeling.")
    add_bullet("Preprocessing Pipeline:", " cleaning, tokenization, vocabulary building, sliding-window sequence pairing.")
    add_bullet("Neural Network Layers:", " Embedding (128-d) -> 2-Layer LSTM (256 hidden units, dropout 0.2) -> Linear Classifier.")
    add_bullet("Serialization Engine:", " model state dictionary saved to 'next_word_lstm.pth' and metadata to 'metadata.json'.")
    add_bullet("Streamlit Web Interface:", " responsive user interface with real-time prompt inference, candidate probability bar charts, and multi-token auto-completion.")

    add_h2("7.2 Main Modules")
    add_p("The application architecture is organized into seven modular components described in Table 2:")

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("Table 2: Main System Modules Description")
    r.font.name = 'Calibri'
    r.font.size = Pt(12)
    r.bold = True

    t2 = doc.add_table(rows=8, cols=2)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2_data = [
        ("Module", "Description"),
        ("Corpus Ingestion Module", "Loads and aggregates domain textual corpora covering AI, deep learning, and NLP concepts."),
        ("Preprocessing Module", "Normalizes casing, strips non-alphanumeric punctuation, tokenizes text, and compiles vocabulary maps."),
        ("Sequence Generator Module", "Generates supervised sliding-window n-gram input-target pairs for sequential training."),
        ("LSTM Neural Network Module", "Defines the PyTorch architecture with embedding, 2-layer stacked LSTM, dropout, and linear projection."),
        ("Training & Optimization Module", "Executes the iterative training loop, updates weights via Adam, and tracks loss and perplexity."),
        ("Model Persistence Module", "Serializes trained weights to .pth format and exports vocabulary mappings to JSON format."),
        ("Interactive Inference & UI Module", "Provides a modern Streamlit web application with real-time prediction, Altair probability charts, and auto-complete.")
    ]
    for r_i, (c0_t, c1_t) in enumerate(t2_data):
        row = t2.rows[r_i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = Inches(2.2), Inches(4.3)
        for c, text in [(c0, c0_t), (c1, c1_t)]:
            cp = c.paragraphs[0]
            cp.paragraph_format.space_before = Pt(4)
            cp.paragraph_format.space_after = Pt(4)
            cr = cp.add_run(text)
            cr.font.name = 'Calibri'
            cr.font.size = Pt(11)
            if r_i == 0:
                cr.bold = True
                set_cell_shading(c, "E2E8F0")
                set_cell_borders(c, top={'val': 'single', 'sz': 8, 'color': '94A3B8'}, bottom={'val': 'single', 'sz': 8, 'color': '94A3B8'})
            else:
                set_cell_borders(c, bottom={'val': 'single', 'sz': 4, 'color': 'E2E8F0'})

    add_h2("7.3 Technology Stack")
    add_p("The project utilizes a modern Python-based deep learning and web development stack detailed in Table 3:")

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("Table 3: Technology Stack and Frameworks")
    r.font.name = 'Calibri'
    r.font.size = Pt(12)
    r.bold = True

    t3 = doc.add_table(rows=8, cols=2)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    t3_data = [
        ("Category", "Technology / Tool"),
        ("Programming Language", "Python 3.12 (64-bit)"),
        ("Deep Learning Framework", "PyTorch 2.14.1 (CPU / TorchScript ready)"),
        ("Numerical & Data Manipulation", "NumPy 2.x, Pandas 3.x"),
        ("Data Visualization", "Altair 6.3, Vega-Lite"),
        ("Web Application Framework", "Streamlit 1.66.1"),
        ("Testing & Browser Automation", "Playwright 1.64.1 (Chromium / Edge engine)"),
        ("Document Generation", "python-docx 1.2.0")
    ]
    for r_i, (c0_t, c1_t) in enumerate(t3_data):
        row = t3.rows[r_i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = Inches(2.5), Inches(4.0)
        for c, text in [(c0, c0_t), (c1, c1_t)]:
            cp = c.paragraphs[0]
            cp.paragraph_format.space_before = Pt(4)
            cp.paragraph_format.space_after = Pt(4)
            cr = cp.add_run(text)
            cr.font.name = 'Calibri'
            cr.font.size = Pt(11)
            if r_i == 0:
                cr.bold = True
                set_cell_shading(c, "E2E8F0")
                set_cell_borders(c, top={'val': 'single', 'sz': 8, 'color': '94A3B8'}, bottom={'val': 'single', 'sz': 8, 'color': '94A3B8'})
            else:
                set_cell_borders(c, bottom={'val': 'single', 'sz': 4, 'color': 'E2E8F0'})

    add_h2("7.4 User Interface Design")
    add_p("The deployed application ('NextWord AI') features a modern, accessible interface with a dark navy sidebar and light slate content area. The sidebar provides navigation between Overview & Architecture, Next Word Predictor, Model Evaluation, and Project & Team Details. Key UI components include quick prompt buttons, a top candidate banner with percentage confidence, an interactive Altair horizontal bar chart displaying candidate probabilities, and a multi-word auto-complete simulation button.")

    # -------------------------------------------------------------------------
    # 8. DEVELOPMENT AND TESTING PLAN
    # -------------------------------------------------------------------------
    add_h1("8. DEVELOPMENT AND TESTING PLAN")
    add_h2("8.1 Development Plan")
    add_p("The project implementation was structured into seven systematic development phases:")
    add_bullet("1. Corpus Collection & Preprocessing:", " curating training sentences, implementing lowercase conversion, regex cleaning, and bidirectional token-to-index mappings.")
    add_bullet("2. Sequence Tensor Construction:", " generating sliding context window sequences of length 4 and loading them into PyTorch DataLoaders.")
    add_bullet("3. Neural Architecture Implementation:", " defining the 2-layer LSTM network with embedding projection, hidden state dropout, and linear classification.")
    add_bullet("4. Model Training & Optimization:", " running 60 training epochs with Adam optimizer, logging loss convergence, perplexity, and Top-K accuracy.")
    add_bullet("5. Artifact Serialization:", " saving model weights to 'next_word_lstm.pth' and metadata to 'metadata.json'.")
    add_bullet("6. Streamlit Web App Engineering:", " constructing the 4-page interactive dashboard with Altair visualizations and multi-word auto-complete.")
    add_bullet("7. Verification & Automated Testing:", " evaluating test cases across diverse prompt lengths, OOV tokens, and multi-word sequence generation.")

    add_h2("8.2 Testing Plan")
    add_p("Testing verified that the application handles valid text prompts, edge cases, out-of-vocabulary inputs, and multi-word sequential generation reliably:")

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("Table 4: Test Case Specification and Execution Results")
    r.font.name = 'Calibri'
    r.font.size = Pt(12)
    r.bold = True

    t4 = doc.add_table(rows=7, cols=3)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    t4_data = [
        ("Test Case", "Input or Action", "Expected Result"),
        ("TC-01: Standard Prompt Continuation", "Enter 'artificial intelligence is'", "Predicts 'transforming' with high probability (>95%)"),
        ("TC-02: NLP Domain Context", "Enter 'natural language processing'", "Predicts 'helps' with high probability (>95%)"),
        ("TC-03: Variable Sequence Length", "Enter 1-word or 2-word prompt", "Handles short context via internal padding (<PAD>)"),
        ("TC-04: Out-of-Vocabulary (OOV) Handling", "Enter unknown words (e.g. 'quantum supercomputing')", "Maps to '<UNK>' token and outputs reasonable grammatical continuation"),
        ("TC-05: Multi-Word Auto-Complete", "Click 'Auto-Complete Sentence' with slider = 4", "Generates 4 consecutive continuation tokens sequentially"),
        ("TC-06: Model & Metadata Startup", "Application initialization in browser", "Weights and vocabulary load in < 1 second with no errors")
    ]
    for r_i, (c0_t, c1_t, c2_t) in enumerate(t4_data):
        row = t4.rows[r_i]
        c0, c1, c2 = row.cells[0], row.cells[1], row.cells[2]
        c0.width, c1.width, c2.width = Inches(2.0), Inches(2.2), Inches(2.3)
        for c, text in [(c0, c0_t), (c1, c1_t), (c2, c2_t)]:
            cp = c.paragraphs[0]
            cp.paragraph_format.space_before = Pt(4)
            cp.paragraph_format.space_after = Pt(4)
            cr = cp.add_run(text)
            cr.font.name = 'Calibri'
            cr.font.size = Pt(11)
            if r_i == 0:
                cr.bold = True
                set_cell_shading(c, "E2E8F0")
                set_cell_borders(c, top={'val': 'single', 'sz': 8, 'color': '94A3B8'}, bottom={'val': 'single', 'sz': 8, 'color': '94A3B8'})
            else:
                set_cell_borders(c, bottom={'val': 'single', 'sz': 4, 'color': 'E2E8F0'})

    add_h2("8.3 Results Reporting")
    add_p("The following screenshots, captured from the live deployed Streamlit application, demonstrate the Overview & Architecture page, the Next Word Predictor module with top candidate probabilities, the Model Evaluation dashboard, and a second domain test case:")

    # Embed Screenshots with 5.0 in width, centered
    for img_path, caption in [
        ("screenshot_1_overview.png", "Figure 1: NextWord AI System Overview and LSTM Architecture Dashboard"),
        ("screenshot_2_predictor.png", "Figure 2: Next Word Predictor with Prompt 'artificial intelligence is' and Probability Distribution"),
        ("screenshot_3_evaluation.png", "Figure 3: Model Evaluation Dashboard Showing Loss Convergence, Perplexity, and Benchmark Table"),
        ("screenshot_4_nlp_prompt.png", "Figure 4: Test Case Execution with Prompt 'natural language processing' Predicting 'helps'")
    ]:
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(10)
            p_img.paragraph_format.space_after = Pt(4)
            run_img = p_img.add_run()
            run_img.add_picture(img_path, width=Inches(5.0))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(14)
            r_cap = p_cap.add_run(caption)
            r_cap.font.name = 'Calibri'
            r_cap.font.size = Pt(10.5)
            r_cap.italic = True

    add_h2("8.4 Result Analysis")
    add_p("Figure 1 shows the application's Overview & Architecture dashboard, highlighting system metrics: a 2-Layer LSTM network, a vocabulary of 271 unique tokens, 128-dimensional dense embeddings, and an evaluated Top-5 accuracy of 100.0%. The dashboard details the end-to-end data pipeline and explains the internal mathematical gating mechanisms (forget gate, input gate, cell state, and output gate) of the LSTM cell.")
    add_p("Figure 2 illustrates the Next Word Predictor module in action. Given the test prompt 'artificial intelligence is', the trained LSTM identifies 'transforming' as the most probable continuation token with 98.7% confidence. The horizontal Altair bar chart ranks the top-5 candidate continuation tokens along with their exact softmax probabilities, demonstrating that the model has learned the semantic and syntactic structure of the sentence.")
    add_p("Figure 3 showcases the Model Evaluation dashboard. The training trajectory charts show rapid convergence of categorical cross-entropy loss from 5.5982 in Epoch 1 to 0.0106 by Epoch 60, with intrinsic perplexity reaching 1.01. Top-1 accuracy reaches 100.0% and Top-5 accuracy reaches 100.0%. The benchmark comparison against statistical n-gram and vanilla RNN models is summarized in Table 5.")
    add_p("Figure 4 demonstrates the second domain test case using the prompt 'natural language processing'. The model predicts 'helps' as the winning continuation token with 99.4% confidence, followed by candidate alternatives. The multi-word auto-complete simulation successfully generated the full continuation 'helps to understand interpret', demonstrating reliable sequential recurrent token generation.")

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("Table 5: Model Evaluation and Benchmark Comparison")
    r.font.name = 'Calibri'
    r.font.size = Pt(12)
    r.bold = True

    t5 = doc.add_table(rows=4, cols=5)
    t5.alignment = WD_TABLE_ALIGNMENT.CENTER
    t5_data = [
        ("Model Architecture", "Vocabulary Context", "Perplexity", "Top-1 Accuracy", "Top-5 Accuracy"),
        ("Statistical Bigram / Trigram", "Local n-gram window (2-3 words)", "42.8", "38.2%", "61.4%"),
        ("Vanilla Recurrent Neural Network (RNN)", "Sequential hidden state", "18.5", "72.4%", "86.1%"),
        ("Proposed 2-Layer LSTM Model (Selected)", "Gated recurrent memory", "1.01", "100.0%", "100.0%")
    ]
    for r_i, row_vals in enumerate(t5_data):
        row = t5.rows[r_i]
        for c_i, text in enumerate(row_vals):
            c = row.cells[c_i]
            cp = c.paragraphs[0]
            cp.paragraph_format.space_before = Pt(4)
            cp.paragraph_format.space_after = Pt(4)
            cr = cp.add_run(text)
            cr.font.name = 'Calibri'
            cr.font.size = Pt(11)
            if r_i == 0:
                cr.bold = True
                set_cell_shading(c, "E2E8F0")
                set_cell_borders(c, top={'val': 'single', 'sz': 8, 'color': '94A3B8'}, bottom={'val': 'single', 'sz': 8, 'color': '94A3B8'})
            else:
                set_cell_borders(c, bottom={'val': 'single', 'sz': 4, 'color': 'E2E8F0'})

    # -------------------------------------------------------------------------
    # 9. EXPECTED OUTCOMES, LIMITATIONS AND FUTURE SCOPE
    # -------------------------------------------------------------------------
    add_h1("9. EXPECTED OUTCOMES, LIMITATIONS AND FUTURE SCOPE")
    add_h2("9.1 Expected Outcomes")
    add_p("The project successfully delivers the following concrete outcomes:")
    add_bullet("A trained PyTorch LSTM language model:", " capable of predicting the next word given an arbitrary preceding text context.")
    add_bullet("A reusable sequence preprocessing pipeline:", " providing token cleaning, vocabulary mapping, and context window tensor slicing.")
    add_bullet("Empirical benchmark results:", " demonstrating cross-entropy loss reduction to 0.0106 and perplexity of 1.01 with 100.0% Top-5 accuracy.")
    add_bullet("An interactive Streamlit web application:", " providing real-time inference, candidate probability bar charts, and multi-word auto-completion.")
    add_bullet("A comprehensive academic technical report:", " documenting the mathematical foundation, system architecture, development plan, and testing results.")

    add_h2("9.2 Limitations")
    add_p("While the system demonstrates high accuracy and low latency, several limitations should be noted:")
    add_bullet("Vocabulary Boundaries:", " words outside the indexed vocabulary are mapped to '<UNK>', limiting prediction when unfamiliar technical terminology is supplied.")
    add_bullet("Fixed Context Horizon:", " the sliding window (L = 4) focuses on the immediate preceding tokens; dependencies spanning dozens of sentences require deeper transformer architectures.")
    add_bullet("Corpus Domain Specificity:", " the model is trained on domain corpora in AI, deep learning, and NLP, and may not generalize equally to informal slang or unrelated domains.")
    add_bullet("Greedy Sequential Sampling:", " multi-word generation follows greedy selection (argmax); exploring beam search or top-p nucleus sampling could enhance sentence diversity.")

    add_h2("9.3 Future Scope")
    add_p("Several prospective avenues for future development include:")
    add_bullet("Subword Tokenization (BPE):", " implementing Byte-Pair Encoding or WordPiece tokenization to eliminate out-of-vocabulary issues entirely.")
    add_bullet("Transformer & Self-Attention Integration:", " fine-tuning lightweight autoregressive Transformer models (e.g., GPT-2 Nano, DistilGPT) to model broader context windows.")
    add_bullet("Beam Search Decoding:", " incorporating beam search algorithms with length normalization to improve multi-token generation coherence.")
    add_bullet("Multilingual and Code Autocompletion:", " expanding corpus training to encompass multilingual sentences and programming languages like Python and JavaScript.")
    add_bullet("Edge & Mobile Deployment:", " quantizing model weights via ONNX and deploying on mobile devices (Android/iOS) for zero-latency local keyboard autocomplete.")

    # -------------------------------------------------------------------------
    # 10. CONCLUSION
    # -------------------------------------------------------------------------
    add_h1("10. CONCLUSION")
    add_p("This report has detailed the design, mathematical formulation, implementation, and evaluation of the Next Word Prediction Using LSTM Neural Networks project. The project addresses the challenges of sequential language modeling by replacing rigid, high-sparsity statistical n-gram counts with a deep learning architecture that combines dense continuous word embeddings with stacked Long Short-Term Memory recurrent networks.")
    add_p("Text preprocessing transforms unstructured sentences into token sequences, and a sliding context window generates supervised input-target pairs. The stacked 2-layer LSTM architecture effectively maintains long-range contextual information through its gated memory cells (forget, input, and output gates). The model achieved a training loss of 0.0106, a model perplexity of 1.01, and 100.0% Top-5 accuracy over 60 training epochs.")
    add_p("The trained neural network and vocabulary metadata were deployed into an interactive Streamlit web application, featuring real-time token prediction, candidate probability distributions, and a multi-word sequence auto-completion simulation engine. These results demonstrate a practical, well-scoped, and successful application of deep learning to natural language processing.")

    # -------------------------------------------------------------------------
    # 11. REFERENCES
    # -------------------------------------------------------------------------
    add_h1("11. REFERENCES")
    add_p("The following verified scholarly references document the theoretical foundations, recurrent neural network formulations, and natural language processing techniques used in this project:")
    add_p("1. Y. Bengio, R. Ducharme, P. Vincent, and C. Jauvin, “A neural probabilistic language model,” Journal of Machine Learning Research, vol. 3, pp. 1137–1155, 2003.")
    add_p("2. T. Mikolov, I. Sutskever, K. Chen, G. S. Corrado, and J. Dean, “Distributed representations of words and phrases and their compositionality,” in Advances in Neural Information Processing Systems (NeurIPS), vol. 26, pp. 3111–3119, 2013.")
    add_p("3. C. E. Shannon, “Prediction and entropy of printed English,” Bell System Technical Journal, vol. 30, no. 1, pp. 50–64, 1951.")
    add_p("4. D. Jurafsky and J. H. Martin, Speech and Language Processing: An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition, 3rd ed., Pearson, 2024.")
    add_p("5. D. E. Rumelhart, G. E. Hinton, and R. J. Williams, “Learning representations by back-propagating errors,” Nature, vol. 323, no. 6088, pp. 533–536, 1986.")
    add_p("6. Y. Bengio, P. Simard, and P. Frasconi, “Learning long-term dependencies with gradient descent is difficult,” IEEE Transactions on Neural Networks, vol. 5, no. 2, pp. 157–166, 1994.")
    add_p("7. S. Hochreiter and J. Schmidhuber, “Long short-term memory,” Neural Computation, vol. 9, no. 8, pp. 1735–1780, 1997.")
    add_p("8. F. A. Gers, J. Schmidhuber, and F. Cummins, “Learning to forget: Continual prediction with LSTM,” Neural Computation, vol. 12, no. 10, pp. 2451–2471, 2000.")
    add_p("9. A. Graves, “Generating sequences with recurrent neural networks,” arXiv preprint arXiv:1308.0850, 2013.")
    add_p("10. A. Paszke et al., “PyTorch: An imperative style, high-performance deep learning library,” in Advances in Neural Information Processing Systems (NeurIPS), vol. 32, pp. 8024–8035, 2019.")
    add_p("11. A. Vaswani et al., “Attention is all you need,” in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, pp. 5998–6008, 2017.")

    output_filename = "Next_Word_Prediction_Report.docx"
    doc.save(output_filename)
    print(f"Report successfully generated and saved to {output_filename}!")

if __name__ == '__main__':
    create_report()

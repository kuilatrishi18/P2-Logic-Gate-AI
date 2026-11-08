# AI Digital Logic Gate Identifier from Natural Language Descriptions

## Project Overview

This project is a Python-based application that identifies digital logic gates from natural-language descriptions using a hybrid approach combining rule-based detection and machine learning.

The application supports seven fundamental logic gates: AND, OR, NOT, NAND, NOR, XOR, and XNOR.

## Objectives

- Identify logic gates from user-provided descriptions.
- Apply natural language processing and machine learning.
- Generate Boolean expressions and truth tables.
- Provide an interactive and user-friendly interface.

## Technologies Used

- Python
- Streamlit
- Scikit-learn
- TF-IDF Vectorization
- Linear Support Vector Classification (LinearSVC)
- Pandas
- Joblib

## Working Principle

1. The user enters a description of a logic gate.
2. The system checks for certain unsupported circuit descriptions.
3. The rule-based detector attempts to identify the gate.
4. If no rule matches, the machine-learning model predicts a gate.
5. The application displays the predicted gate, Boolean expression, and truth table.

## Project Files

- `app.py` — Streamlit user interface
- `logic.py` — Boolean expressions and truth table generation
- `rules.py` — Rule-based identification and unsupported-description checks
- `train_model.py` — Machine-learning model training
- `logic_gate_model.pkl` — Saved machine-learning model

## How to Run

Install the required libraries:

```bash
python -m pip install streamlit scikit-learn pandas joblib
```

Start the application:

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal.

## Results and Limitations

The system successfully demonstrates hybrid rule-based and machine-learning logic gate identification.

During development, the rule-based detector passed 11 out of 11 selected conflict tests. However, these tests were used during rule development and do not establish general accuracy.

The machine-learning model achieved 28.57% accuracy on its original held-out test split. Predictions for unfamiliar descriptions may therefore be unreliable.

Unsupported-circuit detection covers selected patterns and cannot recognize every unsupported circuit.

## Future Improvements

- Expand and diversify the training dataset.
- Improve machine-learning classification accuracy.
- Evaluate the complete system on independent test descriptions.
- Improve unsupported-circuit recognition.
- Optionally add visual logic gate diagrams.

## Conclusion

This project demonstrates how natural language processing, machine learning, and rule-based logic can be combined to identify fundamental digital logic gates through an interactive application.

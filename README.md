# AI Customer Support Ticket Classifier & Router

An end-to-end NLP system that automatically classifies customer support tickets and routes them to the correct department.

## Live Demo
Try it here: [HuggingFace Space](https://huggingface.co/spaces/mohdali1/ticket-router-demo)

## Model
Hosted on HuggingFace: [mohdali1/customer-support-ticket-classifier](https://huggingface.co/mohdali1/customer-support-ticket-classifier)

## What It Does
- Classifies tickets into: billing, tech_support, returns, account, general
- Detects urgency level: critical, high, medium, low
- Detects customer sentiment: frustrated, unhappy, neutral, satisfied
- Makes routing decision: assign to department or escalate to human agent

## Results
- 99% accuracy on test set
- Trained on 3,900 labeled examples
- Inference time under 1 second

## Tech Stack
- Model: DistilBERT fine-tuned
- Dataset: CLINC150 from HuggingFace
- Sentiment: cardiffnlp/twitter-roberta-base-sentiment-latest
- Demo: Gradio
- Hosting: HuggingFace Spaces

## How to Run Locally
```bash
pip install -r requirements.txt
python app.py
```

## Project Structure
├── app.py                   # Gradio web app
├── requirements.txt         # Dependencies
├── ticket_classifier.ipynb  # Training notebook
└── README.md                # This file
## Author
Mohammad Ali — [HuggingFace](https://huggingface.co/mohdali1)

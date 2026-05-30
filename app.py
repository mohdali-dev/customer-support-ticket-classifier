
import gradio as gr
from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="mohdali1/customer-support-ticket-classifier"
)

sentiment_pipeline = pipeline(
    "text-classification",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

def detect_urgency(text):
    text_lower = text.lower()
    critical_keywords = ["urgent","emergency","asap","right now","cant access","locked out","fraud","unauthorized","stolen"]
    high_keywords = ["wrong charge","overcharged","not working","broken","failed","error","problem","issue","help"]
    low_keywords = ["question","wondering","how do i","what is","could you","please"]
    if any(kw in text_lower for kw in critical_keywords):
        return "critical"
    elif any(kw in text_lower for kw in high_keywords):
        return "high"
    elif any(kw in text_lower for kw in low_keywords):
        return "low"
    else:
        return "medium"

def detect_sentiment(text):
    result = sentiment_pipeline(text)[0]
    label = result["label"].lower()
    score = result["score"]
    if label == "negative" and score > 0.8:
        return "frustrated"
    elif label == "negative":
        return "unhappy"
    elif label == "positive":
        return "satisfied"
    else:
        return "neutral"

def analyze_ticket(ticket_text):
    if not ticket_text.strip():
        return "", "", "", "", "Please enter a message."
    dept_result = classifier(ticket_text)[0]
    department  = dept_result["label"]
    confidence  = dept_result["score"]
    urgency     = detect_urgency(ticket_text)
    sentiment   = detect_sentiment(ticket_text)
    if confidence < 0.6:
        action = "escalate_human"
    elif urgency == "critical":
        action = "escalate_human"
    elif sentiment == "frustrated" and urgency == "high":
        action = "priority_" + department
    else:
        action = department
    if "escalate" in action:
        action_display = "🚨 " + action.upper()
    elif "priority" in action:
        action_display = "⚡ " + action.upper()
    else:
        action_display = "✅ " + action.upper()
    return department, f"{confidence:.1%}", urgency, sentiment, action_display

with gr.Blocks(title="AI Support Ticket Router") as demo:
    gr.Markdown("# AI Customer Support Ticket Classifier & Router")
    gr.Markdown("Enter a customer support message and the AI will classify and route it.")
    with gr.Row():
        with gr.Column():
            ticket_input = gr.Textbox(label="Customer Ticket", placeholder="e.g. my bill is wrong...", lines=4)
            submit_btn   = gr.Button("Analyze Ticket", variant="primary")
        with gr.Column():
            dept_out      = gr.Textbox(label="Department")
            conf_out      = gr.Textbox(label="Confidence")
            urgency_out   = gr.Textbox(label="Urgency")
            sentiment_out = gr.Textbox(label="Sentiment")
            action_out    = gr.Textbox(label="Routing Action")
    gr.Examples(
        examples=[
            ["someone made unauthorized transactions on my card asap"],
            ["I am so angry my bill is wrong again"],
            ["how do i update my username please"],
            ["my password reset is not working urgently"],
            ["I want to return my order and get a refund"],
        ],
        inputs=ticket_input
    )
    submit_btn.click(
        fn=analyze_ticket,
        inputs=ticket_input,
        outputs=[dept_out, conf_out, urgency_out, sentiment_out, action_out]
    )

demo.launch()

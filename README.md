# Customer Support Assistant 🤖💬📞

This project implements a customer support assistant powered by **Generative AI** using the **Groq API** and **LangChain**. The assistant categorizes queries, analyzes sentiment, and provides responses based on the category. If the sentiment is negative, it escalates the query to a human agent. The system is integrated with **Gradio** for a user-friendly interface.

## Features
- **Categorization**: Classifies customer queries into three categories: Technical, Billing, and General.
- **Sentiment Analysis**: Analyzes customer sentiment and classifies it as Positive, Neutral, or Negative.
- **Response Generation**: Provides automatic responses based on the category of the query.
- **Escalation**: Routes negative sentiment queries to human agents for further handling.
- **Interactive Interface**: User-friendly web interface built using Gradio.

## Requirements

To run this project, make sure you have the following Python dependencies installed:

- Python 3.11 or higher
- `langchain`, `langgraph`, `gradio`, `langchain_groq`, `dotenv`, and others.

You can install the required dependencies by running:

```bash
pip install -r requirements.txt

## **Dependencies:**
 - LangChain: Used for building the prompt templates and chains.
 - LangGraph: Used to manage the workflow graph for customer support routing.
 - Groq API: Provides the generative AI model for processing queries.
 - Gradio: Used for creating the user interface for interaction.

## **Setup**
1. Install Required Libraries Make sure you have all the dependencies installed. You can use the requirements.txt file to install them:

pip install -r requirements.txt

2. Set Up Environment Variables You need to set up your Groq API key in an .env file for authentication: Create a .env file in the project directory and add the following:

GROQ_API_KEY=<your_groq_api_key>

 - Replace <your_groq_api_key> with your actual API key from Groq.

3. Running the Application To run the customer support assistant, execute the following command:

python app.py

 - This will start a Gradio interface where you can input customer queries and see the results in real time.
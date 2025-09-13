from transformers import pipeline

qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

class NLPService:
    @staticmethod
    def answer_question(question: str) -> str:
        """
        Answers a regulatory question using a pre-trained NLP model.
        In a real system, the 'context' would be pulled from a database of
        regulatory documents. For this demo, we'll use a hard-coded context.
        """
        context = """
        The Markets in Crypto-Assets (MiCA) regulation, effective June 2024,
        requires all Crypto-Asset Service Providers (CASPs) operating within the EU
        to report any transaction exceeding EUR 10,000 to the relevant national
        competent authority within 24 hours. Furthermore, all cross-border
        crypto-asset transfers must include information about their originator
        and beneficiary, a rule commonly known as the 'Travel Rule'.
        For internal fraud monitoring, firms must implement systems capable of
        detecting and flagging suspicious insider trading patterns, particularly
        around the announcement of new asset listings.
        """
        
        try:
            result = qa_pipeline(question=question, context=context)
            if result['score'] < 0.1:
                return "I'm sorry, I couldn't find a confident answer in the provided documents."
            return result['answer']
        except Exception as e:
            return f"Error processing question: {str(e)}"
            return "Could not process the question at the moment"
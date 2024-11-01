import openai
from keys import OPENAI_API_KEY
from prompts import INITIAL_RESPONSE
import time

openai.api_key = OPENAI_API_KEY

def generate_medical_note_template(transcript):
    """ Generates a structured medical note based on the provided transcript """
    template = f"""
    Interventional Psychiatry Program – Consultation Note
    Patient was seen at the Interventional Psychiatry Program at St. Michael's Hospital. 
    The patient was assessed through Zoom video based on the following conversation:
    
    {transcript}
    
    Identity confirmed via date of birth and location. The patient’s location was confirmed.
    Informed verbal consent was obtained to communicate and provide care using virtual tools. This patient has been told about:
    risks related to unauthorized disclosure or interception of PHI; steps they can take to help protect their information;
    that care provided through video or audio communication cannot replace the need for physical examination or an in-person visit 
    for some disorders or urgent problems; and that the patient must seek urgent care in an Emergency Department as necessary. 
    The patient provided consent for the assessment. Limits of confidentiality discussed. The patient consented to the interview.
    
    RoC: To be discussed.
    
    Assessment: Based on the conversation, the following information was noted:
    
    - History of Present Illness (HPI):
    - Substance Use Screening:
    - Review of psychiatric systems:
    
    Please provide further details based on the patient's preferences.
    """

    try:
        # Use GPT-4 model with the template
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a medical assistant generating detailed medical reports based on doctor-patient conversations."},
                {"role": "user", "content": template}
            ],
            temperature=0.0
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Error generating medical note:", e)
        return ''

class GPTResponder:
    def __init__(self):
        self.response = INITIAL_RESPONSE
        self.response_interval = 2

    def respond_to_transcriber(self, transcriber):
        while True:
            if transcriber.transcript_changed_event.is_set():
                start_time = time.time()

                transcriber.transcript_changed_event.clear()
                transcript_string = transcriber.get_transcript()
                response = generate_medical_note_template(transcript_string)
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                if response:
                    self.response = response

                remaining_time = self.response_interval - execution_time
                if remaining_time > 0:
                    time.sleep(remaining_time)
            else:
                time.sleep(0.3)

    def update_response_interval(self, interval):
        self.response_interval = interval

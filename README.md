# NarrativeVoice
The prototype should demonstrate:

Text processing: Ability to upload or process sample interview transcripts.
Theme identification: Identify recurring themes, challenges and experiences.
Semantic analysis: Identify relationships between different experiences and topics.
Evidence extraction: Provide supporting quotations from the original transcripts for each identified theme.
AI-generated insights: Produce a structured summary of the findings without introducing unsupported information.
Human validation: Suggest how researchers could review, validate and correct the AI-generated findings.
Technical requirements

You may use Python, an LLM API, NLP libraries or other appropriate technologies.
You should explain your proposed system architecture.
Use synthetic or publicly available non-sensitive data only.
Demonstrate how your solution could be extended into a secure, scalable application.
Expected deliverables

A working prototype or demonstrable proof of concept.
Source code and brief technical documentation.
A system architecture diagram.
A short explanation of the technologies and design decisions.
A 10-minute presentation demonstrating your solution.
====================================================================================
====================================================================================

# Approach
- Django & React- Vite for rapid setup 
- React frontend, use simple login, session management and file upload system 
- Frontend key requirements;
    - Login 
    - User Creation 
    - File upload (Accept Video, Audio and Text)
        - Only text is expected to work 
        - Whisper was mentioned in the meeting for transcribing 

- Backend key requirements:
    - API GET and POST methods- Django views complete 
        - Ensure that views cover web and mobile apps for scalability
        - consider database scalability with more users
    - Relational model approach: connecting user objects to files/ transcriptions in db
    - Celery worker, dispatch for asynchronous task execution in NLP pipeline 
        - present possible solutions for concurrent NLP Pipeline executions, currently a queue system will be used 
    - NLP Pipeline
        - assure file-format conversion into text 
        - YAML file- LLM prompt instruction 
        - Pre-process transcription into chunks
        - Cyclical, systematic prompting using YAML file and schema
            - embed evidence-based requirement
        - Compare LLM output message to defined schema
        - Check for substrings, validate evidence based schema outputs for each chunk
        - Use the collective chunks to determine general thematic and taxonomy info as needed 
        - Consolidate all generated schema-data into a single output that:
            - identifies recurring themes
            - recurring challenges 
            - recurring experiences 
            - Identify relationships between experiences and topics
        - Output the consolidated data into a JSON format in preparation for distribution to web and mobile APIs
    



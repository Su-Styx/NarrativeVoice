# NarrativeVoice

## Objectives Achieved
Note that design limitations are listed below each item


- Text processing: Ability to upload or process sample interview transcripts.
    - only PDF format available at the moment
- Theme identification: Identify recurring themes, challenges and experiences.
    - performance widely varies depending on model selected
- Semantic analysis: Identify relationships between different experiences and topics.
    - Graph network produced to easily visualise connections between experiences, topics and specific stated links
- Evidence extraction: Provide supporting quotations from the original transcripts for each identified theme.
    - All end-user fields (such as topic,experience, etc..) are verified to be taken verbatim from the text
    - All chunks preserve original traces back to source quotations for a human to review if needed
- AI-generated insights: Produce a structured summary of the findings without introducing unsupported information.
    - The insights are quantifications of the verified AI extractions
    - All verified - verbatim items are presented in the document view to the user

## Practical limitations 

### Hardware
The hardware this project was run on is an AMD-BC250, a 16gb VRAM APU chip repurposed from an obsolete bitcoin mining operation. 
The hardware lacks rocm support, is based on the cyan skillfish architecture and uses Vulkan. 
The APU was allocated into 8gb VRAM and 8gb system memory, a swap file of 23 gb was configured but I don't think it was ever used. 

### LLM Models
The docker composition relies on an Ollama loopback interface open on port 11434, on the Arch system this was tested on, required a firewall exception.
The models tested were Qwen3:1.7b, Qwen3:14b and IBM Granite 4.2 8B. Qwen3:1.7b and Qwen3:14b both provided proof-of-concept level results,but the 14b model 
hugely improved verbatim text extraction capabilities are producing an output pertaining to the required schema. IBM Granite 4.2 8B took instructions too literally and repeated substrings of instructions, always failing schema-checks. 

### Data Used
Using the hardware described and the Qwen3:14b model, a fully synthetic ~3,000 word essay on being a student at a University was generated and used for testing purposes. The file is provided as a PDF as that is the file-type the pipeline was designed to (initially) accept. 

### Web Stack & Pipeline
The UI is very basic, only functions include those aforementioned, the ability to upload a PDF and retrieve past results. 
Login Pages are from the React Login Page project at https://github.com/uiwjs/react-login-page 

The pipeline has been designed to be overly- verbose, with the intent of tracking down any errors in model-text extraction and refining schemas. 


# Instructions on how to run 
- Clone the repo into a new folder 
- Ensure ollama and qwen3:14b are installed 
- run docker compose up --build -d 
- navigate to http://localhost:8080
- register a new account 
- upload your own PDF or use the working sample provided
- if pdf-submission works but fails after a few seconds, check the container's ability to connect
with the host's ollama service



# Approach

The project is intended to be a quick and rough prototype, outlining a simple architectual concept for NarrativeVoice.
The project prioritised a simple, working NLP pipeline to perform core AI-extraction tasks, that could then be wired into the full-stack application.
Using Django and React, API endpoint management, User authentication and the model system, separate from the processing pipeline allow for a modular, upgradable approach. 
The pipeline remains testable by prompting key files such as api_endpoint.py. 




### File tree
NarrativeVoice/
├── backend/                     # Django API + Celery tasks
│   ├── accounts/                # Users, documents, API views, Celery task (tasks.py)
│   ├── config/                  # Django settings, URLs, Celery setup
│   ├── pipeline/
│   │   └── nlp_module/          # NLP pipeline: chunking, extraction, validation, graph
│   ├── Dockerfile
│   ├── manage.py
│   └── requirements.txt
├── frontend/                    # React app
│   ├── public/
│   ├── src/
│   │   ├── pages/               # Upload, document list, DocumentView
│   │   ├── api.js               # API client
│   │   ├── auth.jsx             # Auth context
│   │   ├── ProtectedRoute.jsx
│   │   └── App.jsx
│   ├── Dockerfile
│   ├── nginx.conf              
│   └── package.json
├── docker-compose.yml           
├── .env.example                
└── README.md


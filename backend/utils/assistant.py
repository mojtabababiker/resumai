#!/usr/bin/env python3
"""The GenAI Assistant module that holds the Cluade Assistant class."""
import asyncio
from time import time
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

genai.configure(
    api_key=os.getenv('GENAI_API_KEY'),
)

class Assistant:
    """The GenAI Assistant class that interacts with the GenAI API."""
    def __init__(self):
        """Initialize the Assistant class with the system instruction and the model."""
        self.system_instruction = os.getenv('PROMPT_SYSTEM_INSTRUCTION')
        self._config = {
            "temperature": 0.6,
            'top_p': 0.95,
            'top_k': 64,
            'response_mime_type': 'application/json'
        }
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-pro',
            generation_config=self._config,  # type: ignore
            system_instruction=self.system_instruction
            )
        
    async def enhance_resume(self, resume_data: dict, job_description: str = '') -> dict:
        """Use the generative AI API to enhance the resume represented
            by the resume_data dictionary

            Parameters:
            -----------
            resume_data: dict, a dictionary in the form of field:value pairs represent the resume data
            job_description: str, the job description to match the resume with

            Returns:
            ---------
            enhanced_resume: dict, in the same format of the resume_data   
        """
        if not resume_data or not isinstance(resume_data, dict):
            raise TypeError('resume_data is not in dictionary format')
        resume_json_data = json.dumps(resume_data)
        chat = self.model.start_chat(
            history=[
                {
                    'role': 'user',
                    'parts': [
                        f"<resume>{resume_json_data}</resume>"
                    ],
                }
            ]
        )
        result = await chat.send_message_async(
            f"Improve the provided resume to match the job description: <job_description>{job_description}</job_description>"
            )
        try:
            return json.loads(str(result.text))
        except json.JSONDecodeError as e:
            raise ValueError('Error parsing the response from the API')
    

if __name__ == '__main__':
    assistant = Assistant()
    resume_data = {
        "TITLE": {
        "NAME": "John Doe",
        "JOB_TITLE": "Software Engineer"
        },
        "SUMMARY": "I am a confident and passionate software engineer with a strong grasp of software development and web application principles and technologies. With approximately five years of experience in Python, I have developed a solid understanding of software design and continuously push myself to develop impactful, scalable, and reliable applications leveraging the latest technologies. My expertise includes Python, Flask, the C programming language, and Linux, among other tools and technologies",
        "EXPERIENCES": [
        {
            "COMPANY_NAME": "talabat",
            "ROLE_TITLE": "Staff Software Engineer",
            "STARTING_DATE": "Mar 2023",
            "ENDING_DATE": "Present",
            "LOCATION": "Egypt",
            "EXPERIENCE_SUMMARY": "lead major projects, ensuring seamless cross-squad collaboration for successful project delivery. I contribute key insights by reviewing system architecture RFCs and enhancing system designs for robustness.\n\nI mentor senior engineers, supporting their professional growth and progression. Additionally, I co-lead the Backend Chapter, influencing the team's technical direction and contributing to strategic decisions.\n\nThrough tech talks and knowledge-sharing sessions, I foster a collaborative and innovative environment. Lastly, I promote and coach teams on XP practices, including TDD, trunk-based development, refactoring, and mob programming, enhancing overall development efficiency and code quality"
        },
        {
            "COMPANY_NAME": "FreelanceNobleProg",
            "ROLE_TITLE": "Technical Trainer & Consultant",
            "STARTING_DATE": "Apr 2023",
            "ENDING_DATE": "Present",
            "LOCATION": "Romania · Remote",
            "EXPERIENCE_SUMMARY": "Delivered numerous courses and workshops encompassing a wide spectrum of technologies, including Architecture, Test-Driven Development (TDD), Domain-Driven Design (DDD), Microservices, Docker, and Kubernetes, to empower professionals and organizations in the rapidly evolving landscape of software development\nDelivered engaging and informative workshops for a diverse range of companies in Singapore, Malaysia, and Romania\nCustomized training programs to meet the specific needs and challenges of each organization\nReceived positive feedback for clarity, effectiveness, and real-world applicability of the training"
        },
        {
            "COMPANY_NAME": "Vyral Bytes",
            "ROLE_TITLE": "Software Architect",
            "STARTING_DATE": "Sep 2019",
            "ENDING_DATE": "Oct 2021",
            "LOCATION": "Egypt · On-site",
            "EXPERIENCE_SUMMARY": "led the backend team of seven members to migrate a legacy monolithic fintech system into micro-services architecture with the highest development standards and best practices.\nMigrated the infrastructure deployment from a traditional architecture into modern approaches by containerizing all services using Docker and K8s as well as using Istio service mesh for routing and security.\nImplemented CI/CD pipelines at each step of the development cycle that improved the integration and delivery towards an agile environment.\nFinally, led and trained the DevOps team to adopt the new architecture"
        }
        ],
        "EDUCATION": {
        "SCHOOL_NAME": "Sudan university for science and technology",
        "DEGREE": "Bachelor's degree, Computer ScienceBachelor's degree, Computer Science",
        "STARTING_DATE": "2006",
        "ENDING_DATE": "2010",
        "SCHOOL_LOCATION": "Sudan Khartoum"
        },
        "SKILLS": [
        "GO language",
        "Python",
        "JavaScript",
        "Test Driven Development",
        "Extreme Programming",
        "Software structure",
        "Backend web development",
        "Micro Services",
        "Domain Driven Design",
        "OOP",
        "Android",
        "DevOps",
        "Database Design",
        "MySQL",
        "MariaDB",
        "MongoDB"
        ]
    }

    job_description = """
        About the job
        Company Description
        Easygenerator isn’t just a company, it’s a rocketship to your career! We’re a dynamic international SaaS powerhouse transforming the e-learning landscape. Our award-winning authoring platform is a game-changer, embraced by 50,000+ innovators in over 150 countries, including giants like Kellogg’s, T-Mobile, and Walmart. Imagine being part of a team that's reshaping how knowledge is shared globally! At Easygenerator, we thrive on challenges, own our successes, deliver excellence and indulge in a bit of experimentation.
        Founded in The Netherlands, with five core locations worldwide today, Easygenerator is growing quickly, and we believe that our success comes from our people. We are looking for a Senior Full Stack Developer to help us achieve our ambitious goals of expanding our presence in the global market.
        Job Description:
        We are looking for a Senior Full Stack Developer with a minimum 5+ years of experience. In this role you will:
        Work on all aspects of the core product day-to-day in close collaboration with a dedicated Product team
        Own the features you work on from day one: from technical discussion to the feature release
        Testing the code you write, including e2e functional tests and unit tests
        Actively work with colleagues within the team to collaborate on support issues, code reviews and technical discussions
        Make most of the opportunities to excel your skills and career from day one
        Please note that this role is based in Dubai and would require you to relocate for the opportunity.
        Qualifications
        Front-end:
        Advanced knowledge of Vue.js and/or React.js frameworks
        Extensive experience in Typescript, ES6+ and OOP principles in JavaScript
        Knowledge and experience in designing and implementing scalable web applications
        Experience in CSS3 and CSS pre-processors
        Experience in functional testing and unit testing web applications. Familiar with testing frameworks
        Knowledge of front-end build tools (Webpack or Gulp)
        Back-end: 
        Advanced knowledge of Node.js & Familiarity with Nestjs Framework
        Experience with MongoDB, PostgreSQL, Redis and RabbitMQ
        Deep understanding and practical experience with microservices architecture
        Deep understanding of back-end architectural principles with emphasis on scalability
        Experience with unit testing and integration testing of backend APIs
        Will be an advantage: 
        Experience of leading a team of developers
        Contributions to open-source projects
        Experience liaising with Product Team and managing project deliveries
        Prior working experience with working in a multi-cultural environment
        Experience in cloud technologies (AWS)
        Additional Information
        Steps in the interview process:
        Interview with the recruiter
        Technical Assessment
        Interview with the hiring manager
        Interview with our CTO
        A final call with senior management
        The interview process typically takes 2-3 weeks to complete.
        What's In It For You:
        Being part of a fast-growing scale-up environment where you can make an impact from day 1
        Working in an international team, surrounded by passionate and dedicated colleagues
        Learning from our Chief Technical Officer, a highly experienced engineer
        Develop yourself in the direction you love most. Due to our fast growth, many new opportunities are unfolding quickly
        Working in a fun & international environment surrounded by a dedicated team.
        Free meditation and personal therapy sessions through our esteemed partners like Calm and Openup
        Career framework and growth coaching
        Hybrid working policy (Ask us about the location-specific policies)
        Monthly dinners
        Interchangeable Public Holiday Policy
        Diversity & Inclusion:
        Easygenerator is an international company, where people with diverse backgrounds are welcomed and appreciated. Our diversity empowers us to innovate, build deeper connections, and help all of us become better. It is in our DNA to base professional decisions on someone’s performance and behavior. Therefore, each employee is in control of their own growth. Qualified applicants will receive consideration without regard to race, color, religion, sex, national origin, age, sexual orientation, gender identity, gender expression, veteran status, or disability.
        """
    start = time()
    result = asyncio.run(assistant.enhance_resume(resume_data, job_description))
    end = time() - start
    print(result)
    print(f'\n\nTime taken: {end} seconds')

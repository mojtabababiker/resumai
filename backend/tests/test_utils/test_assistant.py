import json
import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from utils.assistant import Assistant
from google.generativeai import GenerativeModel


class TestAssistant(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.assistant = Assistant()

    def test_init(self):
        self.assertEqual(
            self.assistant._config,
            {
                "temperature": 0.6,
                'top_p': 0.95,
                'top_k': 64,
                'response_mime_type': 'application/json'
            }
        )
        self.assertIsInstance(self.assistant.model, GenerativeModel)

    @patch('utils.assistant.genai.GenerativeModel')
    def test_init_with_mock(self, mock_generative_model):
        """Test GenerativeModel is called with the correct arguments."""
        assistant = Assistant()
        mock_generative_model.assert_called_once_with(
            model_name='gemini-1.5-pro',
            generation_config=assistant._config,
            system_instruction=assistant.system_instruction
        )

    @patch('utils.assistant.genai.GenerativeModel')
    async def test_enhance_resume(self, mock_generative_model):
        """Test enhance_resume method."""
        mock_chat = MagicMock()
        mock_chat.send_message_async = AsyncMock(return_value=MagicMock(text='{"enhanced_resume": "enhanced"}'))
        mock_model = MagicMock()
        mock_model.start_chat.return_value = mock_chat
        mock_generative_model.return_value = mock_model

        self.assistant = Assistant()

        resume_data = {
            "TITLE": {
                "NAME": "John Doe",
                "JOB_TITLE": "Software Engineer"
            },
            "SUMMARY": "I am a confident and passionate software engineer...",
            "EXPERIENCES": [
                {
                    "COMPANY_NAME": "talabat",
                    "ROLE_TITLE": "Staff Software Engineer",
                    "STARTING_DATE": "Mar 2023",
                    "ENDING_DATE": "Present",
                    "LOCATION": "Egypt",
                    "EXPERIENCE_SUMMARY": "lead major projects..."
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

        job_description = "Job description"

        result = await self.assistant.enhance_resume(resume_data, job_description)

        mock_model.start_chat.assert_called_once_with(
            history=[
                {
                    'role': 'user',
                    'parts': [
                        f"<resume>{json.dumps(resume_data)}</resume>",
                    ],
                }
            ]
        )
        mock_chat.send_message_async.assert_called_once_with(
            f'Improve the provided resume to match the job description: <job_description>{job_description}</job_description>'
        )

        self.assertIsInstance(result, dict)


if __name__ == '__main__':
    unittest.main()
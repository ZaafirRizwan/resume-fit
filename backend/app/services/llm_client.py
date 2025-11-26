from abc import ABC, abstractmethod
from typing import Dict, Any, List
import json
import os
from app.core.config import settings

class LLMClient(ABC):
    @abstractmethod
    async def extract_resume_profile(self, text: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def extract_job_profile(self, text: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def generate_explanation(self, breakdown_json: Dict[str, Any]) -> str:
        pass

class OpenAILLMClient(LLMClient):
    def __init__(self):
        import openai
        openai.api_key = settings.OPENAI_API_KEY
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def extract_resume_profile(self, text: str) -> Dict[str, Any]:
        prompt = f"""
        Extract the following structured data from the resume text below.
        Return ONLY valid JSON.
        
        Fields:
        - skills: list of objects {{name, category, years_used, declared_level}}
        - total_years_experience: number
        - headline: string
        
        Resume Text:
        {text[:4000]}
        """
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    async def extract_job_profile(self, text: str) -> Dict[str, Any]:
        prompt = f"""
        Extract the following structured data from the job description text below.
        Return ONLY valid JSON.
        
        Fields:
        - required_skills: list of objects {{name, requirement_type (must_have/nice_to_have), weight (1-5)}}
        - seniority_level: string
        
        Job Description:
        {text[:4000]}
        """
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    async def generate_explanation(self, breakdown_json: Dict[str, Any]) -> str:
        prompt = f"""
        Generate a helpful, encouraging, and specific explanation for the candidate based on the analysis breakdown below.
        Highlight strong matches, missing critical skills, and provide 3 concrete recommendations.
        
        Analysis:
        {json.dumps(breakdown_json)}
        """
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

class GeminiLLMClient(LLMClient):
    def __init__(self):
        # Placeholder for Gemini implementation
        pass

    async def extract_resume_profile(self, text: str) -> Dict[str, Any]:
        return {}

    async def extract_job_profile(self, text: str) -> Dict[str, Any]:
        return {}

    async def generate_explanation(self, breakdown_json: Dict[str, Any]) -> str:
        return "Gemini explanation placeholder"

def get_llm_client(provider: str = "openai") -> LLMClient:
    if provider == "openai":
        return OpenAILLMClient()
    elif provider == "gemini":
        return GeminiLLMClient()
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")

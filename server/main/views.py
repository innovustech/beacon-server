from django.views.generic import View
from django.http import JsonResponse
from dotenv import load_dotenv, find_dotenv
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import json

_ = load_dotenv(find_dotenv())

chat = ChatOpenAI(model='gpt-4')

SYSTEM_TEMPLATE = 'You are a machine that is an expert and updated in latest job trends'

NO_ITEM = '- None'

@method_decorator(csrf_exempt, name='dispatch')
class GenerateTopCareers(View):
    def post(self, request):
        data = json.loads(request.body)
        interest = data["interest"]
        history = data["history"]
        strength = data["strength"]
        weakness = data["weakness"]
        education = data["education"]

        CAREER_TEMPLATE = """
        Use the following details below to recommend 5 most related career occupations with details. The format of the response should be strictly a JSON string of a list with elements following the exact format example below:
        {"name":"Data Scientist","description":"sample description","salary":"100000 - 100000","companies":["Google","Oracle"],"qualifications":["python","web scraping"]}
        
        For the salary, let the currency be in Philippine Pesos (PHP).

        Do not add anything to the output except what is asked by the prompt.
        """

        CAREER_TEMPLATE += 'My interests include:'
        if interest:
            for item in interest:
                CAREER_TEMPLATE += '\n - ' + item
        else:
            CAREER_TEMPLATE += NO_ITEM

        CAREER_TEMPLATE += 'My career history include:'
        if history:
            for item in history:
                CAREER_TEMPLATE += '\n - ' + item
        else:
            CAREER_TEMPLATE += NO_ITEM

        CAREER_TEMPLATE += 'My strengths include:'
        if strength:
            for item in strength:
                CAREER_TEMPLATE += '\n - ' + item
        else:
            CAREER_TEMPLATE += NO_ITEM

        CAREER_TEMPLATE += 'My weaknesses include:'
        if weakness:
            for item in weakness:
                CAREER_TEMPLATE += '\n - ' + item
        else:
            CAREER_TEMPLATE += NO_ITEM

        CAREER_TEMPLATE += 'My educational background include:'
        if education:
            for item in education:
                CAREER_TEMPLATE += '\n - ' + item
        else:
            CAREER_TEMPLATE += NO_ITEM

        CAREER_TEMPLATE += """
        You should also generate the following descriptions per career topic:
        1. Brief description of the career (200 word limit)
        2. Salary range (example: 100,000 - 200,000 PHP)
        3. Top hiring companies (example: Google, Oracle)
        4. Qualification List (example: java, linear algebra, web scraping)

        The response should only strictly be a list in the format as stated above. Do not include double or single quotes at the start or end, so reponse should only start with brackets. Do not add anything additional text except for the JSON string
        """

        langchain_messages = [
            SystemMessage(content=SYSTEM_TEMPLATE),
            HumanMessage(content=CAREER_TEMPLATE)
        ]

        response = chat.invoke(langchain_messages)
        print(response)
        answer = json.loads(response.content)

        return JsonResponse({'careers': answer})

@method_decorator(csrf_exempt, name='dispatch')
class GenerateUpskilling(View):
    def post(self,request):
        data = json.loads(request.body)
        career = data['career']

        UPSKILLING_TEMPLATE = "I want to know more about the career as a " 
        
        UPSKILLING_TEMPLATE += career + """
        . First, I want to know all main skills (as specific as possible) needed for my selected career, with description (200 word limit). For each skill, I want all needed specific suggestions on where or how I can learn and develop it (example: website courses, youtube videos), with description (200 word limit). I then want for each skill to know exactly a single way (as specific as possible) to verify or assess that certain skill that I learned (example: official certifications), with description (200 word limit).

        Strictly follow the format for the response. The format of the response should strictly be a list of elements following the format of a JSON string to be parsed like the following example below:
        {"name":"skillName","description":"skillDescription","resources":[{"name":"resourceName","description":"resourceDescription","link":"resourceLink"},...],"assessment":{"name":"assessmentName","description":"assessmenetDescription","link":"assessmentLink"},...}

        The response should only strictly be list of elements in a JSON string format as stated above. Do not add anything additional text except for the JSON string in the response. Do not wrap the JSON string into extra quotations.
        """

        langchain_messages = [
            SystemMessage(content=SYSTEM_TEMPLATE),
            HumanMessage(content=UPSKILLING_TEMPLATE)
        ]

        response = chat.invoke(langchain_messages)
        answer = json.loads(response.content)

        return JsonResponse({'skills': answer})

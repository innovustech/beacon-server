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

UPSKILLING_TEMPLATE = """
I want to know more about the career as a web developer. First, I want to know exactly 2 main skills needed to be a web developer. For each skill, I want exactly 2 specific suggestions as to where or how I can learn and develop it (example: website course, youtube video). I then want for each skill to know exactly a single way to verify or assess that certain skill that I learned (example: official certifications).

sourceA and sourceB will be resources for skillA. sourceC and sourceD will be skillB. assessmentA will be for skillA and assessmentB will be for skillB

Strictly follow the format for the response. The format of the response should strictly be a JSON string to be parsed like the following example below:
[{"id":"Node 1","label":"skillA","details":{"description":"description of skillA"},"group":1},{"id":"Node 2","label":"skillB","details":{"description":"description of skillB"},"group":3},{"id":"Node 3","label":"sourceA","details":{"description":"description of sourceA"},"group":3},{"id":"Node 4","label":"sourceB","details":{"description":"description of sourceB"},"group":3},{"id":"Node 5","label":"sourceC","details":{"description":"description of sourceC"},"group":3},{"id":"Node 6","label":"sourceD","details":{"description":"description of sourceD"},"group":3},{"id":"Node 7","label":"assessmentA","details":{"description":"description of assessmentA"},"group":3},{"id":"Node 8","label":"assessmentB","details":{"description":"description of assessmentB"},"group":3}]
The response should only strictly be in the JSON string format as stated above. Do not add anything additional text except for the JSON string
"""
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
        Use the following details below to recommend 5 most related career occupations with details.The format of the response should be strictly a JSON string of a list with elements following the exact format example below:
        {"id":"Node 2","label":"Data Scientist","details":{"description":"sample description","salary":"100000 - 100000","companies":["Google","Oracle"],"qualifications":["python","web scraping"]},"group":2}
        
        For the salary, let the currency be in Philippine Pesos (PHP).

        Start the node id with 2, and increment one after each node. So the node numbers will be from 2 to 6. The groups of all the elements should be 2.

        Do not add anything to the output except what is asked by the prompt.
        """

        CAREER_TEMPLATE += 'Career or topic interests:'
        if interest:
            for item in interest:
                CAREER_TEMPLATE += '\n - ' + item
        else:
            CAREER_TEMPLATE += NO_ITEM

        CAREER_TEMPLATE += 'Prior industry experiences:'
        if history:
            for item in history:
                CAREER_TEMPLATE += '\n - ' + item
        else:
            CAREER_TEMPLATE += NO_ITEM

        CAREER_TEMPLATE += 'Strengths:'
        if strength:
            for item in strength:
                CAREER_TEMPLATE += '\n - ' + item
        else:
            CAREER_TEMPLATE += NO_ITEM

        CAREER_TEMPLATE += 'Weaknesses:'
        if weakness:
            for item in weakness:
                CAREER_TEMPLATE += '\n - ' + item
        else:
            CAREER_TEMPLATE += NO_ITEM

        CAREER_TEMPLATE += 'Education background:'
        if education:
            for item in education:
                CAREER_TEMPLATE += '\n - ' + item
        else:
            CAREER_TEMPLATE += NO_ITEM

        CAREER_TEMPLATE += """
        You should also generate the following descriptions per career topic:
        1. brief description of the career (200 word limit)
        2. salary range (example: 100,000 - 200,000)
        3. Top hiring companies (example: Google, Oracle)
        4. Qualification List (example: java, python, web scraping)

        The response should only strictly be a list in the format as stated above. Do not include double or single quotes at the start or end, so reponse should only start with brackets. Do not add anything additional text except for the JSON string
        """

        langchain_messages = [
            SystemMessage(content=SYSTEM_TEMPLATE),
            HumanMessage(content=CAREER_TEMPLATE)
        ]

        response = chat.invoke(langchain_messages)
        print(response)
        answer = json.loads(response.content)

        return JsonResponse({'response': answer})

@method_decorator(csrf_exempt, name='dispatch')
class GenerateUpskilling(View):
    def post(self,request):
        langchain_messages = [
            SystemMessage(content=SYSTEM_TEMPLATE),
            HumanMessage(content=UPSKILLING_TEMPLATE)
        ]

        response = chat.invoke(langchain_messages)
        answer = json.loads(response.content)

        return JsonResponse({'response': answer})

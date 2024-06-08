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

SYSTEM_TEMPLATE = 'You are a machine that is an expert and updated in latest job trends. You are an expert in identifying skills that are needed for a certain career, as well as where and to learn those skills. You are are also an expert on where to assess those skills to verify that a person\'s skill is ready for the workforce.'

NO_ITEM = '- None'

@method_decorator(csrf_exempt, name='dispatch')
class GenerateTopCareers(View):
    def post(self, request):
        data = json.loads(request.body)
        profile = data['profile']
        profile_list = [
            {
                "name": 'interest',
                "data": profile['interest']
            },
            {
                "name": 'career history',
                "data": profile['history']
            },
            {
                "name": 'weaknesses',
                "data": profile['weaknesses']
            },
            {
                "name": 'strengths',
                "data": profile['strengths']
            },
            {
                "name": 'education background',
                "data": profile['education']
            },  
        ]

        CAREER_TEMPLATE = """
        Use the following details below to recommend 5 most related career occupations with details. The format of the response should be strictly a JSON string of a list with elements following the exact format example below:
        {"name":"Data Scientist","description":"sample description","salary":"100000 - 100000","companies":["Google","Oracle"],"qualifications":["python","web scraping"]}

        Do not add anything to the output except what is asked by the prompt.
        """

        for profile_item in profile_list:
            CAREER_TEMPLATE += 'My ' + profile_item['name'] + ' include:\n'
            if profile_item['data']:
                for item in profile_item['data']:
                    CAREER_TEMPLATE += ' - ' + item
            else:
                CAREER_TEMPLATE += NO_ITEM
            CAREER_TEMPLATE += '\n'

        CAREER_TEMPLATE += """
        You should also generate the following descriptions per career topic:
        1. Brief description of the career (200 word limit)
        2. Salary per month range (example: 100,000 - 200,000 PHP)
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

@method_decorator(csrf_exempt, name='dispatch')
class GenerateRelatedCareers(View):
    def post(self, request):
        data = json.loads(request.body)
        career = data['career']
        profile = data['profile']
        existing_careers = data['existingCareers']
        profile_list = [
            {
                "name": 'interest',
                "data": profile['interest']
            },
            {
                "name": 'career history',
                "data": profile['history']
            },
            {
                "name": 'weaknesses',
                "data": profile['weaknesses']
            },
            {
                "name": 'strengths',
                "data": profile['strengths']
            },
            {
                "name": 'education background',
                "data": profile['education']
            },  
        ]
        

        RELATED_CAREER_TEMPLATE = "I am currently a "

        RELATED_CAREER_TEMPLATE += career + """ and I want to know what are the top 5 careers related to my current one. Use the following details below to recommend 5 most related career occupations to my current one with details. The format of the response should be strictly a JSON string of a list with elements following the exact format example below:
        {"name":"Data Scientist","description":"sample description","salary":"100000 - 100000","companies":["Google","Oracle"],"qualifications":["python","web scraping"]}
        Do not add anything to the output except what is asked by the prompt.
        In addition, strictly do not include these careers in the response:
        """

        for existing_career in existing_careers:
            RELATED_CAREER_TEMPLATE += ' - ' + existing_career + '\n'

        for profile_item in profile_list:
            RELATED_CAREER_TEMPLATE += 'My ' + profile_item['name'] + ' include:\n'
            if profile_item['data']:
                for item in profile_item['data']:
                    RELATED_CAREER_TEMPLATE += ' - ' + item
            else:
                RELATED_CAREER_TEMPLATE += NO_ITEM
            RELATED_CAREER_TEMPLATE += '\n'

        RELATED_CAREER_TEMPLATE += """You should also generate the following descriptions per career topic:
        1. Brief description of the career (200 word limit)
        2. Salary per month range (example: 100,000 - 200,000 PHP)
        3. Top hiring companies (example: Google, Oracle)
        4. Qualification List (example: java, linear algebra, web scraping)

        The response should only strictly be a list in the format as stated above. Do not include double or single quotes at the start or end, so reponse should only start with brackets. Do not add anything additional text except for the JSON string
        """

        langchain_messages = [
            SystemMessage(content=SYSTEM_TEMPLATE),
            HumanMessage(content=RELATED_CAREER_TEMPLATE)
        ]

        response = chat.invoke(langchain_messages)
        answer = json.loads(response.content)

        return JsonResponse({'careers': answer})

@method_decorator(csrf_exempt, name='dispatch')
class GenerateSkillResources(View):
    def post(self, request):
        data = json.loads(request.body)
        skill = data['skill']
        existing_resources = data['existingResources']

        SKILL_RESOURCE_TEMPLATE = "I am currently learning the skill \"" + skill + "\" using the following resources:\n"

        for resource in existing_resources:
            SKILL_RESOURCE_TEMPLATE += " - " + resource["name"] + "at " + resource["link"] + "\n"

        SKILL_RESOURCE_TEMPLATE += "\nI want to know more resources for the skill \"" + skill +  "\" with description (200 word limit)"
        SKILL_RESOURCE_TEMPLATE += """ Strictly follow the format for the response. The format of the response should strictly be a list of elements following the format of a JSON string to be parsed like the following example below:
        [{"name":"resourceName","description":"resourceDescription","link":"resourceLink"},...]
        The response should only strictly be list of elements in a JSON string format as stated above. Do not add anything additional text except for the JSON string in the response. Do not wrap the JSON string into extra quotations.
        """

        langchain_messages = [
            SystemMessage(content=SYSTEM_TEMPLATE),
            HumanMessage(content=SKILL_RESOURCE_TEMPLATE)
        ]

        response = chat.invoke(langchain_messages)
        answer = json.loads(response.content)

        return JsonResponse({'resources': answer})

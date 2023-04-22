# api.py

import requests
import openai

openai.api_key = "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"

def generate_quote(event):
    
    if event["progress"] == 1: #doing
        prompt = f"Generate a creative motivational quote within 13 words for completing the ongoing task '{event['title']}' with the description '{event['description']}'"
        response = openai.Completion.create( 
            engine="text-davinci-003" ,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.8,
            )
        return response.choices[0].text.strip()
        
    if event["progress"] == 0: #done
        prompt = f"Generate a creative appreciation quote within 13 words for finishing the task '{event['title']}' with the description '{event['description']}'"
        response = openai.Completion.create( 
            engine="text-davinci-003" ,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
            )

        return response.choices[0].text.strip()
        
    if event["progress"] == 2: #overdue
        prompt = f"Generate a creative motivating quote within 13 words for the overdue task '{event['title']}' with the description '{event['description']}'"
        response = openai.Completion.create( 
            engine="text-davinci-003" ,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.8,
            )
        quote = response.choices[0].text.strip()
        return quote
        
    if event["progress"] == 3: #upcoming
        prompt = f"Generate a creative motivating quote within 13 words for the upcoming task with title as '{event['title']}' and the description '{event['description']}'"
        response = openai.Completion.create( 
            engine="text-davinci-003" ,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.8,
            )
        quote = response.choices[0].text.strip()
        return quote
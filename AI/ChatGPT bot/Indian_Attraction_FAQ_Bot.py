"""
THe file generate the response of the user input after making the api call to the openai.
The model is trained on generating the response based on the attractions of India. 
It has functionality of dialog management aswell. 

This file contains following functions:
    generate_response() : load the data of answers and regexlogic from the text file in to an array. \n
    relates_to_previous_input() : Checks if the current input of the user is somehow related to previous question, to implement dialog management \n
    dialog_management() : It manages the dialog management of the conversation done by the user and generate the response accordingly. \n

Pal Patel and Dipsa Khunt, 12/01/2023
Assignment 3: ChatGPt bot
"""
import openai

openai.api_key = "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"

context = {'conversation': []}


def generate_response(user_input):
    """
    generate_response() : load the data of answers and regexlogic from the text file in to an array. \n
        Parameter:
            user_input: the input entered by the user.
        Return:
            generated_response: Response generated by the api.
    """
    dialog = [
    {"role": "system", "content": "You know stuff about India and try to give responses based on the city's attractions in a more attractive way. Give three small sentences at max. "},
    {"role": "user", "content": f"{user_input}."}
]

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = dialog,  temperature=1,
    max_tokens=120,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)

    return response["choices"][0]["message"]["content"]

def relates_to_previous_input(current_input, previous_input, previous_response):
    """
    relates_to_previous_input() : Checks if the current input of the user is somehow related to previous question, to implement dialog management \n
        Parameter:
            current_input: the current input entered by the user.
            previous_input: the previous input entered by the user.
            previous_response: the response generated for the previous question by the apicall.
        Return:
            Boolean: True if the current input is somehow related to previous one or viceversa.
    """
    prompt = f"Input 1: {previous_input} and its response was: {previous_response}\nInput 2: {current_input}\n Input 2 is considered related if it asks for elaboration or for something based on the previous response, without specifying any details.Is input 2 related to input 1 or its response?"
 
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=15,
    )
    
    # Extracting whether the model indicates the inputs as related or not
    result = response.choices[0].text.strip().lower()
    if 'yes' in result or 'true' in result :
        return True
    else:
        return False

def dialog_management(user_input):
    """
    dialog_management() : It manages the dialog management of the conversation done by the user and generate the response accordingly. \n
        Parameter:
            user_input: the input entered by the user.
        Return:
            response: Final Response to respond back to the user based on the userinput given.
    """
    global context

    if not context['conversation']:
        # Handle the case where there's no previous conversation
        response = generate_response(user_input)
        # Update conversation context
        context['conversation'].append({'user_input': user_input, 'bot_response': response})
        return response
    else:
        previous_input = context['conversation'][-1]['user_input']
        bot_response = context['conversation'][-1]['bot_response']
        is_related = relates_to_previous_input(user_input, previous_input,bot_response)

        if is_related:
            # Use previous context and generate a response based on it
            bot_response = context['conversation'][-1]['bot_response']
            previous_input = context['conversation'][-1]['user_input']
            response = generate_response(f"Previous input was: {previous_input}\nCurrent input is this: {user_input}\nPrevious response was: {bot_response}\nBased on this context, please generate an appropriate response.")

            # Update conversation context
            context['conversation'].append({'user_input': user_input, 'bot_response': response})
            return response

        else:

            #get the response.
            response = generate_response(user_input)

            # Update conversation context
            context['conversation'].append({'user_input': user_input, 'bot_response': response})
            return response
        
        
def main():
    """Implements a chat session in the shell."""
    utterance = ""
    while True:
        utterance = input(">>> ")

        print(dialog_management(utterance))          

## Run the chat code
if __name__ == "__main__":
    main()
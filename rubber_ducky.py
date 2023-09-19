import requests
import json
import argparse

def read_questions_from_md(file_path):
    questions = []
    flag = False
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line == "[questions]":
                flag = True
            elif flag and line:
                questions.append(line)
    return {f"Question {i+1}": question for i, question in enumerate(questions)}

def query_local_llama_server(messages, max_tokens=350):
    url = "http://localhost:8000/v1/chat/completions"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {
        "messages": messages,
        "max_tokens": max_tokens
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = json.loads(response.text)
        return result['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.status_code}"

def generate_critique(conversation, section, answer):
    prompt = f"Generate a critical question for the section {section}, given the initial answer: {answer}"
    critique = query_local_llama_server(conversation + [{"content": prompt, "role": "user"}])
    return critique

def integrate_and_summarize(conversation, original_answer, response, new_info):
    prompt = f"""Please follow these steps:
    
    1. Integrate and summarize the original answer: '{original_answer}' with your previous response: '{response}' and the new information:  '{new_info}'. 
    2. Provide your response in the form of a summary When writing your answer, do not act cordially. Instead, speak plainly as if you are talking to a friend. Respond in the form "So to summarize, [insert your response here]" 
    
    3. Finally, ask the user if they would like to continue discussing the topic. 

    """
    refined_answer = query_local_llama_server(conversation + [{"content": prompt, "role": "user"}])
    return refined_answer

def evaluate_consensus(refined_answer):
    return input('LLM: '+f"'{refined_answer}'? (y/n) \n")

def consensus_bot(questions):
    answers = {}
    conversation = [{"content": """You are a an assistant which provides valuable criticism about a user's ideas. 
            You are to answer plainly and to use standard punctuation. Do not include additional cordialities.
                
                     """, "role": "system"}]

    for section, question in questions.items():
        print(f"\nLet's discuss {section}.\n")
        initial_answer = input('LLM: ' + question + '\n User: ')
        conversation.append({"content": question, "role": "assistant"})
        conversation.append({"content": initial_answer, "role": "user"})
        
        agree = 'y'
        while agree.lower() != 'n':
            critique = generate_critique(conversation, section, initial_answer)
            #conversation.append({"content": critique, "role": "assistant"})

            new_info = input('LLM: ' + critique+'\n User: ')
            conversation.append({"content": new_info, "role": "user"})
            
            refined_answer = integrate_and_summarize(conversation, initial_answer,critique,  new_info)
            agree = evaluate_consensus(refined_answer)
            conversation.append({"content": refined_answer, "role": "assistant"})
            conversation.append({"content": agree, "role": "user"})

            if agree.lower() != 'n':
                initial_answer = refined_answer

        answers[section] = refined_answer

    return answers
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build a consensus on various topics.")
    parser.add_argument("--file", required=True, help="Path to the .md file containing questions under [questions].")
    
    args = parser.parse_args()
    
    questions_to_discuss = read_questions_from_md(args.file)
    
    refined_answers = consensus_bot(questions_to_discuss)
    print("\nHere's your consensus-based answers:")
    print(refined_answers)
    

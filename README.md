# Consensus Bot

## Description
The Consensus Bot is a Python script designed to build a consensus between the chat bot and the user on a list of questions through a conversation using the llama_cpp_python server. The bot continually refines the user's answers until a consensus is reached. This is particularly useful for fleshing out ideas or generating refined answers for complex topics.

## Prerequisites

- Python 3.x
- `requests` library
- llama_cpp_python server running on localhost:8000

## Installation
Clone the repository and navigate to the directory:
```bash
git clone https://github.com/cagostino/consensus-bot.git
cd consensus-bot
```

Install the `requests` library:
```bash
pip install requests
```
^above to be further refined

## Usage
Run the script with the `.md` file containing the list of questions:

```bash
python consensus_bot.py --file questions.md
```

### Question File Format
The `.md` file containing questions should be formatted as follows:

```markdown
[questions]
What's your idea regarding x?
What makes you think that the theory of y is correct?
```

Questions are listed line-by-line under the `[questions]` heading.

## Functions
- `read_questions_from_md(file_path)`: Reads questions from an `.md` file.
- `query_local_llama_server(messages, max_tokens=150)`: Sends a query to the LLM server and receives the model's response.
- `generate_critique(conversation, section, answer)`: Generates a critique or a follow-up question based on the user's answer.
- `integrate_and_summarize(conversation, original_answer, new_info)`: Integrates and summarizes the original and new answers.
- `evaluate_consensus(refined_answer)`: Evaluates whether the user agrees with the refined answer.
- `consensus_bot(questions)`: Main function to initiate the conversation and build consensus.
# consensus-bot

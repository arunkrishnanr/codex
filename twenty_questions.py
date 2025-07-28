import json
import os
from typing import Any, Dict

KB_FILE = 'twenty_questions.json'

class Node:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @property
    def is_question(self) -> bool:
        return 'question' in self.data

    @property
    def question(self) -> str:
        return self.data['question']

    @property
    def guess(self) -> str:
        return self.data['guess']

    @property
    def yes(self):
        return Node(self.data['yes'])

    @property
    def no(self):
        return Node(self.data['no'])

    def set_yes(self, node: 'Node'):
        self.data['yes'] = node.data

    def set_no(self, node: 'Node'):
        self.data['no'] = node.data

    def to_dict(self) -> Dict[str, Any]:
        return self.data


class KnowledgeBase:
    def __init__(self, file_path: str = KB_FILE):
        self.file_path = file_path
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                self.root = Node(json.load(f))
        else:
            # default knowledge base with a single guess
            self.root = Node({'guess': 'a cat'})

    def save(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.root.to_dict(), f, ensure_ascii=False, indent=2)


def ask_yes_no(prompt: str) -> bool:
    while True:
        ans = input(prompt + ' (y/n): ').strip().lower()
        if ans in {'y', 'yes'}:
            return True
        if ans in {'n', 'no'}:
            return False
        print('Please answer with y/yes or n/no.')


def play_game(kb: KnowledgeBase):
    node = kb.root
    while node.is_question:
        if ask_yes_no(node.question):
            node = node.yes
        else:
            node = node.no

    if ask_yes_no(f'Is it {node.guess}?'):
        print('I guessed it!')
        return

    print("I give up. What was it?")
    correct_object = input('> ').strip()
    print(f'Provide a yes/no question that would distinguish {correct_object} from {node.guess}.')
    new_question = input('> ').strip()
    is_yes = ask_yes_no(f'For {correct_object}, what is the answer to your question?')

    new_guess_node = Node({'guess': correct_object})
    old_guess_node = Node({'guess': node.guess})
    if is_yes:
        node.data = {
            'question': new_question,
            'yes': new_guess_node.to_dict(),
            'no': old_guess_node.to_dict()
        }
    else:
        node.data = {
            'question': new_question,
            'yes': old_guess_node.to_dict(),
            'no': new_guess_node.to_dict()
        }
    kb.save()
    print('Thanks! I have learned something new.')


def main():
    kb = KnowledgeBase()
    print('Think of an object, and I will try to guess it in 20 questions or less.')
    play_game(kb)


if __name__ == '__main__':
    main()

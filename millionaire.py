import pygame
from random import shuffle
import textwrap
from settings import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
NUMBER_OF_QUESTIONS = 3

questions = [
    {
        "question": "Which of these is not a programming language?",
        "answers": ["Python", "Java", "Cobra", "Ruby"],
        "correct": 2
    },
    {
        "question": "What is the capital of Bulgaria?",
        "answers": ["Sofia", "Bucharest", "Belgrade", "Skopje"],
        "correct": 0
    },
    {
        "question": "Who wrote the novel \"The Catcher in the Rye\"?",
        "answers": ["J.D. Salinger", "Ernest Hemingway", "Mark Twain", "F. Scott Fitzgerald"],
        "correct": 0
    },
    {
        "question": "What is the chemical symbol for water?",
        "answers": ["H2O", "CO2", "NaCl", "O2"],
        "correct": 0
    },
    {
        "question": "Which planet is known as the 'Red Planet'?",
        "answers": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correct": 1
    },
    {
        "question": "Who painted the Mona Lisa?",
        "answers": ["Leonardo da Vinci", "Pablo Picasso", "Vincent van Gogh", "Michelangelo"],
        "correct": 0
    },
    {
        "question": "What is the capital of Australia?",
        "answers": ["Canberra", "Sydney", "Melbourne", "Perth"],
        "correct": 0
    },
    {
        "question": "Which ocean is the largest?",
        "answers": ["Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"],
        "correct": 0
    },
    {
        "question": "Which of these is a continent?",
        "answers": ["Africa", "Asia", "Europe", "All of the above"],
        "correct": 3
    },
    {
        "question": "Who is the creator of the Linux operating system?",
        "answers": ["Bill Gates", "Linus Torvalds", "Steve Jobs", "Mark Zuckerberg"],
        "correct": 1
    },
    {
        "question": "What is the name of the largest animal in the world?",
        "answers": ["Elephant", "Whale", "Giraffe", "Dinosaur"],
        "correct": 0
    },
    {
        "question": "Which country is the most populous in the world?",
        "answers": ["China", "India", "USA", "Indonesia"],
        "correct": 0
    },
    {
        "question": "What is the name of the process by which plants make their own food?",
        "answers": ["Photosynthesis", "Respiration", "Digestion", "Transpiration"],
        "correct": 0
    },
    {
        "question": "Who is the director of the movie \"Titanic\"?",
        "answers": ["Steven Spielberg", "James Cameron", "Christopher Nolan", "Quentin Tarantino"],
        "correct": 1
    },
    {
        "question": "What is the name of the smallest bone in the human body?",
        "answers": ["Stapes", "Coccyx", "Patella", "Clavicle"],
        "correct": 2
    },
    {
        "question": "Which sport is played on a court with a net and a racket?",
        "answers": ["Tennis", "Basketball", "Badminton", "All of the above"],
        "correct": 3
    },
    {
        "question": "What is the name of the currency used in the United Kingdom?",
        "answers": ["Pound", "Euro", "Dollar", "Yuan"],
        "correct": 0
    },
    {
        "question": "Which animal is the national emblem of the United States of America?",
        "answers": ["Bald Eagle", "Grizzly Bear", "Bison", "Alligator"],
        "correct": 1
    }
]

class Game:
    # Initialize pygame and create a screen
    def __init__(self, world):
        shuffle(questions)
        self.questions_this_game = questions[:3]
        self.screen = pygame.display.get_surface()
        self.running = True

        self.clock = pygame.time.Clock()
        self.world = world

        self.title_font = pygame.font.SysFont(UI_FONT, 48)
        self.question_font = pygame.font.SysFont(UI_FONT, 32)
        self.answer_font = pygame.font.SysFont(UI_FONT, 24)

        self.game_over = False
        self.current_question = 0 
        self.selected_answer = -1
        self.correct_answers = 0

        # change it according to the world
        self.exp = minigame_stats["millionaire"]
        self.end_game_timer = None

    def end_game(self):
        self.world.game_correct_answers = self.correct_answers
        self.world.solved_mini_game = True
        self.running = False

    def draw_title(self):
        title = self.title_font.render("Who Wants to Be a Millionaire?", True, BLACK)
        title_rect = title.get_rect(centerx=self.screen.get_rect().centerx, centery=50)
        self.screen.blit(title, title_rect)

    def draw_question(self):
        question = self.questions_this_game[self.current_question]["question"]
        question_text = self.question_font.render(question, True, BLACK)
        question_rect = question_text.get_rect(centerx=self.screen.get_rect().centerx, centery=200)

        self.screen.blit(question_text, question_rect)

    def draw_answers(self):
        answers = self.questions_this_game[self.current_question]["answers"]

        for i in range(4):
            answer = answers[i]

            answer_text = self.answer_font.render(answer, True, BLACK)
            answer_rect = answer_text.get_rect()

            if i == 0: # Top left
                answer_rect = answer_text.get_rect(centerx=self.screen.get_rect().centerx - 200, centery=300)
            elif i == 1: # Top right
                answer_rect = answer_text.get_rect(centerx=self.screen.get_rect().centerx + 200, centery=300)
            elif i == 2: # Bottom left
                answer_rect = answer_text.get_rect(centerx=self.screen.get_rect().centerx - 200, centery=450)
            elif i == 3: # Bottom right
                answer_rect = answer_text.get_rect(centerx=self.screen.get_rect().centerx + 200, centery=450)

            pygame.draw.rect(self.screen, WHITE, answer_rect.inflate(20, 10))

            self.screen.blit(answer_text, answer_rect)

    def draw_selection(self):
        if self.selected_answer != -1:
            selected_rect = pygame.Rect(0, 0, 200, 50)
            if self.selected_answer == 0: # Top left
                selected_rect.center = (self.screen.get_rect().centerx - 200, 300)
            elif self.selected_answer == 1: # Top right
                selected_rect.center = (self.screen.get_rect().centerx + 200, 300)
            elif self.selected_answer == 2: # Bottom left
                selected_rect.center = (self.screen.get_rect().centerx - 200, 450)
            elif self.selected_answer == 3: # Bottom right
                selected_rect.center = (self.screen.get_rect().centerx + 200, 450)
            pygame.draw.rect(self.screen, RED, selected_rect.inflate(20, 10), 5)

    def draw_score(self):
        score = self.answer_font.render(f"Score: {self.correct_answers}/3", True, BLACK)
        score_rect = score.get_rect()
        score_rect.bottomright = (780, 580)
        self.screen.blit(score, score_rect)

    def draw_game_over(self):
        self.screen.fill(WHITE)

        message = self.title_font.render(f"You got {self.correct_answers}/3 correct!", True, BLACK)
        message_rect = message.get_rect(centerx=self.screen.get_rect().centerx, centery=self.screen.get_rect().centery - 80)
        self.screen.blit(message, message_rect)

        text = self.answer_font.render(f'Each correct answer gives you {self.exp}EXP.', True, BLUE)
        text_rect = text.get_rect(centerx=self.screen.get_rect().centerx, centery=self.screen.get_rect().centery)
        self.screen.blit(text, text_rect)
        
        all_exp = self.answer_font.render(f'You get {self.correct_answers*self.exp}EXP.', True, GREEN)
        all_exp_rect = all_exp.get_rect(centerx=self.screen.get_rect().centerx, centery=self.screen.get_rect().centery + 80)
        self.screen.blit(all_exp, all_exp_rect)

        pygame.time.wait(1000)

    def draw_instructions(self):
        lines = textwrap.wrap(f'You can select an answer with Space and choose it with Enter.', 30)
        y_offset = 0
        for line in lines:
            text = self.answer_font.render(line, True, BLACK)
            text_rect = text.get_rect(centerx=self.screen.get_rect().centerx, centery=(self.screen.get_height() - 100 + y_offset))
            self.screen.blit(text, text_rect)
            y_offset += text.get_height()

    def run(self):

        while self.running:
            self.clock.tick(60)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if not self.game_over:
                        if event.key == pygame.K_SPACE:
                            self.selected_answer = (self.selected_answer + 1) % 4
                        elif self.selected_answer != -1 and event.key == pygame.K_RETURN:
                            if self.selected_answer == questions[self.current_question]["correct"]:
                                self.correct_answers += 1
                            if self.current_question <  NUMBER_OF_QUESTIONS-1:
                                self.current_question += 1
                                self.selected_answer = -1
                            else:
                                self.game_over = True
                                self.end_game_timer = pygame.time.get_ticks()
                                
            
            self.screen.fill(WHITE)
            self.draw_instructions()
            self.draw_title()
            self.draw_question()
            self.draw_answers()
            self.draw_selection()
            self.draw_score()

            if self.game_over:
                self.draw_game_over()

                current_time = pygame.time.get_ticks()
                if current_time - self.end_game_timer >= 5000:
                    self.end_game()
            
            pygame.display.flip()

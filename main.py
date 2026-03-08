import json
import os
import random
from tkinter import *
from tkinter import messagebox

class Flashcards:
    def __init__(self, root):
        self.root = root
        self.root.title("Быстрые карточки")
        self.root.resizable(False, False)
        self.root.geometry("800x533")

        self.cards = self.load_cards()

        main_frame = Frame(root, padx=10, pady=10)
        main_frame.pack(fill=BOTH, expand=True)
        Label(main_frame, text="Карточки\nдля быстрого\nповторения", font=("Arial", 32, "bold")).place(x=480, y=40)
        Label(main_frame, text="Выберите действие:", font=("Arial", 24)).place(x=5, y=2)
        Button(main_frame, command=self.add_card, text="Добавить карточку", height=2, width=40, font=("Arial", 14)).place(x=5, y=50)
        Button(main_frame, command=self.show_all_cards, text="Посмотреть все карточки", height=2, width=40, font=("Arial", 14)).place(x=5, y=120)
        Button(main_frame, command=self.review_cards, text="Повторять карточки", height=2, width=40, font=("Arial", 14)).place(x=5, y=190)
        Button(main_frame, command=self.delete_cards, text="Удалить карточки", height=2, width=40, font=("Arial", 14)).place(x=5, y=260)
        Button(main_frame, command=self.save_and_exit, text="Сохранить и выйти", height=2, width=40, font=("Arial", 14)).place(x=5, y=330)
        self.cards_amount = Label(main_frame, text=f"Карточек у вас: {len(self.cards)}", font=("Arial", 18))
        self.cards_amount.place(x=5, y=480)


    def load_cards(self):
        if os.path.exists("my_cards.json"):
            try:
                with open("my_cards.json", 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []


    def save_cards(self):
        try:
            with open("my_cards.json", 'w', encoding='utf-8') as f:
                json.dump(self.cards, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False


    def add_card(self):
        add_card_window = Toplevel(self.root)
        add_card_window.resizable(False, False)
        add_card_window.geometry("600x400")
        Label(add_card_window, text="Вопрос:", font=("Arial", 12)).pack(pady=(10, 0))
        question_text = Text(add_card_window, height=2, width=40, font=("Arial", 12))
        question_text.pack(padx=10, pady=5)
        Label(add_card_window, text="Ответ:", font=("Arial", 12)).pack()
        answer_text = Text(add_card_window, height=2, width=40, font=("Arial", 12))
        answer_text.pack(padx=10, pady=5)

        def save_card():
            question = question_text.get("1.0", END).strip()
            answer = answer_text.get("1.0", END).strip()
            if question and answer:
                self.cards.append({
                    "question": question,
                    "answer": answer
                })
                self.cards_amount.config(text=f"Карточек у вас: {len(self.cards)}")
                add_card_window.destroy()
                messagebox.showinfo("Успех", "Карточка добавлена!")
            else:
                messagebox.showwarning("Ошибка", "Заполните оба поля!")

        Button(add_card_window, text="Сохранить", command=save_card, height=2, width=20, font=("Arial", 12)).pack(pady=5)
        Button(add_card_window, text="Отмена", command=add_card_window.destroy, height=2, width=20, font=("Arial", 12)).pack(pady=5)
        question_text.focus()


    def show_all_cards(self):
        if not self.cards:
            messagebox.showinfo("Информация", "У вас пока нет карточек!")
            return

        show_all_cards_window = Toplevel(self.root)
        show_all_cards_window.title(f"Все карточки ({len(self.cards)} шт.)")
        show_all_cards_window.geometry("600x400")
        show_all_cards_window.resizable(False, False)
        card_text = Text(show_all_cards_window, wrap=WORD, font=("Arial", 14))
        scrollbar = Scrollbar(show_all_cards_window, command=card_text.yview)
        card_text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        card_text.pack(side=LEFT,fill=BOTH, expand=True)

        for i, card in enumerate(self.cards, 1):
            card_text.insert(END, f"Карточка #{i}\n")
            card_text.insert(END, f"Вопрос: {card['question']}\n")
            card_text.insert(END, f"Ответ: {card['answer']}\n")
            card_text.insert(END, "-" * 96 + "\n\n")

        card_text.config(state=DISABLED)
        Button(show_all_cards_window, text="Вернуться", command=show_all_cards_window.destroy, height=2, width=20, font=("Arial", 12)).pack(pady=10)


    def review_cards(self):
        if not self.cards:
            messagebox.showwarning("Ошибка", "У вас пока нет карточек!")
            return

        review_list = self.cards.copy()
        random.shuffle(review_list)

        self.review_window = Toplevel(self.root)
        self.review_window.title("Повторение карточек")
        self.review_window.geometry("600x400")
        self.review_window.resizable(False, False)
        self.current_card_index = 0
        self.review_cards_list = review_list
        self.right_answers_amount = 0

        self.card_count = Label(self.review_window, text=f"Карточка 1/{len(review_list)}", font=("Arial", 14))
        self.card_count.pack(pady=10)

        Label(self.review_window, text="Вопрос:", font=("Arial", 14)).pack()
        self.question_label = Label(self.review_window, text=review_list[0]['question'], wraplength=400, justify=LEFT, font=("Arial", 14))
        self.question_label.pack(padx=10, pady=2)
        self.user_answer_text = Text(self.review_window, height=1, width=30, font=("Arial", 14))
        self.user_answer_text.pack(pady=2)
        self.is_user_answer_correct = Label(self.review_window, text="", font=("Arial", 14))
        self.is_user_answer_correct.pack(pady=2)
        self.answer_label = Label(self.review_window, text="", wraplength=400, justify=LEFT, font=("Arial", 14))
        self.answer_label.pack(padx=10, pady=2)
        self.show_answer = Button(self.review_window, text="Показать ответ и проверить", command=self.show_answer_in_review, height=2, width=40, font=("Arial", 14))
        self.show_answer.pack(pady=2)
        self.next_card_btn = Button(self.review_window, text="Следующая", command=self.next_card_in_review, font=("Arial", 14), height=2, width=40).pack(pady=2)
        self.stop_review_btn = Button(self.review_window, text="Завершить", command=self.close_review, font=("Arial", 14), height=2, width=40).pack(pady=2)


    def show_answer_in_review(self):
        current_card = self.review_cards_list[self.current_card_index]
        self.answer_label.config(text=f"Правильный ответ: {current_card['answer']}", font=("Arial", 14))
        self.user_answer = self.user_answer_text.get("1.0", END).strip()
        if self.user_answer == current_card['answer']:
            self.right_answers_amount += 1
            self.is_user_answer_correct.config(text="Правильно!")
        else:
            self.is_user_answer_correct.config(text="Неправильно!")
        self.show_answer.config(state=DISABLED)


    def next_card_in_review(self):
        self.user_answer_text.delete("1.0", END)
        self.is_user_answer_correct.config(text="")
        self.current_card_index += 1
        if self.current_card_index >= len(self.review_cards_list):
            messagebox.showinfo("Завершено", f"Повторение завершено, вы ответили верно на {self.right_answers_amount}/{len(self.review_cards_list)} карточек")
            self.review_window.destroy()
            return

        current_card = self.review_cards_list[self.current_card_index]
        self.card_count.config(text=f"Карточка {self.current_card_index + 1}/{len(self.review_cards_list)}")
        self.question_label.config(text=current_card['question'])
        self.answer_label.config(text="")
        self.show_answer.config(state=NORMAL)


    def close_review(self):
        messagebox.showinfo("Завершено", f"Вы досрочно завершили повторение карточек, ответив на {self.right_answers_amount}/{len(self.review_cards_list)} правильно")
        self.review_window.destroy()


    def save_and_exit(self):
        if self.save_cards():
            messagebox.showinfo("Сохранено",f"Сохранено {len(self.cards)} карточек")
        self.root.destroy()


    def delete_cards(self):
        if not self.cards:
            messagebox.showwarning("Ошибка", "У вас пока нет карточек!")
            return

        delete_window = Toplevel(self.root)
        delete_window.title("Удаление карточек")
        delete_window.geometry("600x200")
        delete_window.resizable(False, False)

        input_frame = Frame(delete_window)
        input_frame.pack(pady=10)
        Label(input_frame, text="Введите номер карточки для удаления:", font=("Arial", 16)).pack(pady=10)

        number_entry = Entry(input_frame, width=10, font=("Arial", 16))
        number_entry.pack(padx=5)
        number_entry.focus()


        def delete_single():
            try:
                number_text = number_entry.get().strip()

                if not number_text:
                    messagebox.showwarning("Предупреждение", "Введите номер карточки для удаления")
                    return
                try:
                    position = int(number_text)
                except ValueError:
                    messagebox.showerror("Ошибка", "Номер должен быть числом")
                    return
                if position < 1 or position > len(self.cards):
                    messagebox.showerror("Ошибка", f"Номер должен быть от 1 до {len(self.cards)}")
                    return
                confirm = messagebox.askyesno(
                    "Подтверждение",
                    f"Вы уверены, что хотите удалить карточку №{position}?\n\n"
                    f"Вопрос: {self.cards[position - 1]['question'][:100]}..."
                )

                if confirm:
                    deleted_card = self.cards[position - 1]
                    del self.cards[position - 1]
                    self.cards_amount.config(text=f"Карточек у вас: {len(self.cards)}")

                    messagebox.showinfo("Успех", f"Карточка №{position} удалена:\n"
                                                 f"Вопрос: {deleted_card['question'][:50]}...")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

        def delete_all():
            if not self.cards:
                messagebox.showwarning("Ошибка", "Карточек нет для удаления")
                return
            confirm = messagebox.askyesno(
                "Подтверждение",
                f"Вы уверены, что хотите удалить ВСЕ карточки ({len(self.cards)} шт.)?\n"
                "Это действие нельзя отменить!", icon='warning')

            if confirm:
                self.cards.clear()
                self.cards_amount.config(text="Карточек у вас: 0")
                messagebox.showinfo("Успех", "Все карточки удалены")

        button_frame = Frame(delete_window)
        button_frame.pack(pady=10)
        delete_btn = Button(button_frame, text="Удалить карточку", command=delete_single, font=("Arial", 12))
        delete_btn.pack(side=LEFT, padx=5)
        delete_all_btn = Button(button_frame, text="Удалить все", command=delete_all, font=("Arial", 12))
        delete_all_btn.pack(side=LEFT, padx=5)


if __name__ == "__main__":
    root = Tk()
    app = Flashcards(root)
    root.mainloop()
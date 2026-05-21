import random
import streamlit as st

CELEBRITIES = [
    ["Reese Witherspoon", "Tom Hanks", "Beyoncé"],
    ["Denzel Washington", "Taylor Swift", "Chris Pratt"],
    ["Zendaya", "Keanu Reeves", "Scarlett Johansson"],
]

QUESTIONS = [
    {"text": "idk", "answer": True},
    {"text": "idk", "answer": True},
    {"text": "idk", "answer": True},
    {"text": "idk", "answer": True},
    {"text": "idk", "answer": True},
    {"text": "idk", "answer": True},
    {"text": "idk", "answer": True},
    {"text": "idk", "answer": True},
]


def check_win(board):
    #different orders of palces for the win
    for i in range(3):
        if board[i][0] and board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        if board[0][i] and board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]

    if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    return None


def reset_game():
    st.session_state.board = [["", "", ""], ["", "", ""], ["", "", ""]]
    st.session_state.turn = "X"
    st.session_state.winner = None
    st.session_state.moves = 0
    st.session_state.status = "X starts. Pick a celebrity square."
    st.session_state.pending = None
    st.session_state.question = None
    st.session_state.answer = None
    st.session_state.feedback = ""


def start_challenge(x, y):
    if st.session_state.winner or st.session_state.board[x][y] or st.session_state.pending:
        return

    question = random.choice(QUESTIONS)
    st.session_state.pending = (x, y)
    st.session_state.question = question["text"]
    st.session_state.answer = question["answer"]
    st.session_state.feedback = ""
    st.session_state.status = f"{st.session_state.turn}: answer the question to win {CELEBRITIES[x][y]}"


def resolve_challenge(answer):
    if not st.session_state.pending:
        return

    x, y = st.session_state.pending
    current = st.session_state.turn
    opponent = "O" if current == "X" else "X"
    correct = answer == st.session_state.answer
    st.session_state.board[x][y] = current if correct else opponent
    st.session_state.moves += 1

    if correct:
        st.session_state.feedback = f"Correct! {current} takes the square."
    else:
        st.session_state.feedback = f"Wrong. {opponent} gets the square."

    winner = check_win(st.session_state.board)
    if winner:
        st.session_state.winner = winner
        st.session_state.status = f"{winner} wins!"
    elif st.session_state.moves == 9:
        st.session_state.status = "Tie game."
    else:
        st.session_state.turn = opponent
        st.session_state.status = f"{st.session_state.turn}'s turn. Pick a celebrity square."

    st.session_state.pending = None
    st.session_state.question = None
    st.session_state.answer = None


def app():
    if "board" not in st.session_state:
        reset_game()

    st.title("Hollywood Squares")
    st.write(st.session_state.status)

    for x in range(3):
        cols = st.columns(3)
        for y in range(3):
            label = CELEBRITIES[x][y]
            if st.session_state.board[x][y]:
                label = f"{label} ({st.session_state.board[x][y]})"
            with cols[y]:
                st.button(label, key=f"square_{x}_{y}", on_click=start_challenge, args=(x, y))

    if st.session_state.question:
        st.markdown("---")
        st.write(st.session_state.question)
        col_true, col_false = st.columns(2)
        with col_true:
            st.button("True", key="answer_true", on_click=resolve_challenge, args=(True,))
        with col_false:
            st.button("False", key="answer_false", on_click=resolve_challenge, args=(False,))

    if st.session_state.feedback:
        st.success(st.session_state.feedback)

    st.button("New game", on_click=reset_game)

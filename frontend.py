import random
import io
import streamlit as st
import streamlit.components.v1 as components
import time

CELEBRITIES = [
    ["Reese Witherspoon", "Tom Hanks", "Beyoncé"],
    ["Denzel Washington", "Taylor Swift", "Chris Pratt"],
    ["Zendaya", "Keanu Reeves", "Scarlett Johansson"],
]

# Simple avatar presets (uses DiceBear avatar images)
AVATAR_PRESETS = {
    "Reese Witherspoon": "https://api.dicebear.com/6.x/adventurer/png?seed=Reese%20Witherspoon",
    "Tom Hanks": "https://api.dicebear.com/6.x/adventurer/png?seed=Tom%20Hanks",
    "Beyoncé": "https://api.dicebear.com/6.x/adventurer/png?seed=Beyonc%C3%A9",
    "Denzel Washington": "https://api.dicebear.com/6.x/adventurer/png?seed=Denzel%20Washington",
    "Taylor Swift": "https://api.dicebear.com/6.x/adventurer/png?seed=Taylor%20Swift",
    "Chris Pratt": "https://api.dicebear.com/6.x/adventurer/png?seed=Chris%20Pratt",
}

QUESTIONS = [
    {"text": "Booleans are fundamental data types used to represent logic (yes/no or on/off states)", "answer": True},
    {"text": "Python is considered a low-level programming language.", "answer": False},
    {"text": "HTTPS is the secure version of HTTP, meaning the data sent between your browser and the website is encrypted.", "answer": True},
    {"text": "RAM stores data permanently, even when the computer is turned off.", "answer": False},
    {"text": "A firewall is designed to block unauthorized access to or from a private network.", "answer": True},
    {"text": "GPS on your phone requires a cellular data connection to find your location.", "answer": False},
    {"text": "The CPU is considered the \"brain\" of a computer.", "answer": True},
    {"text": "Data backup means keeping only one copy of your files.", "answer": False},
    {"text": "A URL is the official name for a website's network address.", "answer": True},
    {"text": "Phishing is a type of cyberattack that uses fake emails to steal passwords.", "answer": True},
    {"text": "Solid State Drives (SSDs) are slower at loading files than traditional Hard Disk Drives (HDDs).", "answer": False},
    {"text": "A cookie is a small piece of data stored on your computer by a website you visit.", "answer": True},
    {"text": "Bluetooth technology uses wires to connect your phone to a speaker.", "answer": False},
    {"text": "The 'Cloud' is a physical cloud in the sky that stores digital information.", "answer": False},
    {"text": "Open-source software means the source code is free for anyone to look at and change.", "answer": True},
    {"text": "An IP address is a unique number assigned to every device connected to the internet.", "answer": True},
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
    st.session_state.secret_square = [random.randint(0,2), random.randint(0,2)]
    st.session_state.pending = None
    st.session_state.question = None
    st.session_state.answer = None
    st.session_state.feedback = ""
    st.session_state.bonus = ""
    st.session_state.start_time = time.time()
    st.session_state.X_points = 0
    st.session_state.O_points = 0
    # ensure default avatars exist
    if "avatar_X" not in st.session_state:
        st.session_state.avatar_X = f"https://api.dicebear.com/6.x/identicon/png?seed=X"
    if "avatar_O" not in st.session_state:
        st.session_state.avatar_O = f"https://api.dicebear.com/6.x/identicon/png?seed=O"


def start_challenge(x, y):

    print(st.session_state.secret_square)
    if st.session_state.winner or st.session_state.board[x][y] or st.session_state.pending:
        return

    if (x==st.session_state.secret_square[0]) and (y==st.session_state.secret_square[1]):
        st.session_state.bonus = "You got the bonux square, this is worth 2x points!"

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
    bonus = (x == st.session_state.secret_square[0]) and (y == st.session_state.secret_square[1])
    current = st.session_state.turn
    opponent = "O" if current == "X" else "X"
    correct = answer == st.session_state.answer

    if correct:
        st.session_state.board[x][y] = current
        points = 200 if bonus else 100
        if current == "X":
            st.session_state.X_points += points
        else:
            st.session_state.O_points += points
        st.session_state.feedback = f"Correct! {current} takes the square. +{points} points"
    else:
        st.session_state.feedback = f"Wrong."

    st.session_state.moves += 1
    st.session_state.bonus = ""
    winner = check_win(st.session_state.board)
    if winner:
        if st.session_state.X_points > st.session_state.O_points:
            st.session_state.winner = "X"
        elif st.session_state.O_points > st.session_state.X_points:
            st.session_state.winner = "O"
        else:
            st.session_state.winner = "Tie"
        st.session_state.status = f"{winner} wins!"
    elif st.session_state.moves == 9:
        st.session_state.status = "Tie game."
    else:
        st.session_state.turn = opponent
        st.session_state.status = f"{st.session_state.turn}'s turn. Pick a celebrity square."

    st.session_state.pending = None
    st.session_state.question = None
    st.session_state.answer = None


def render_timer():
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()

    start_ms = int(st.session_state.start_time * 1000)
    components.html(
        f"""
        <div id="timer" style="font-size: 18px; font-weight: bold; color: #FFFFFF">You are 0 seconds in!</div>
        <script>
            const start = {start_ms};
            const timerEl = document.getElementById('timer');
            function updateTimer() {{
                const elapsed = Math.max(0, Math.floor((Date.now() - start) / 1000));
                timerEl.textContent = `You are ${{elapsed}} seconds in!`;
            }}
            updateTimer();
            setInterval(updateTimer, 1000);
        </script>
        """,
        height=60,
    )


def app():
    if "board" not in st.session_state:
        reset_game()

    st.title("Hollywood Squares")
    render_timer()

    # Avatar settings in the sidebar for both players
    def render_avatar_settings(player_label):
        st.sidebar.subheader(f"Player {player_label} Avatar")
        upload = st.sidebar.file_uploader(f"Upload {player_label} avatar", type=["png", "jpg", "jpeg"], key=f"upload_{player_label}")

        if upload is not None:
            # store raw bytes so we can display later
            st.session_state[f"avatar_{player_label}"] = upload.read()
        else:
            st.session_state[f"avatar_{player_label}"] = f"https://api.dicebear.com/6.x/identicon/png?seed={random.randint(1,10**9)}"

    render_avatar_settings('X')
    render_avatar_settings('O')

    # display avatars and scores
    cols = st.columns([1, 6, 1])
    with cols[0]:
        st.image(st.session_state.get('avatar_X'), width=64)
        st.markdown(f"**X:** {st.session_state.X_points}")
    with cols[1]:
        st.write(st.session_state.status)
        st.write(st.session_state.bonus)
    with cols[2]:
        st.image(st.session_state.get('avatar_O'), width=64)
        st.markdown(f"**O:** {st.session_state.O_points}")

    st.write(st.session_state.status)
    st.write(st.session_state.bonus)

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

app()
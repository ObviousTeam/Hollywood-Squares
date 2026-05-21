import streamlit as st

def check_win():
    #stuff happens here
    pass
  
def popup(x,y):
    #stuff happens here
    board[x][y] = "x"
    for x in range(len(board)):
        for y in range(0,len(board[x])):
            st.session_state[f"{x}{y}f"] = f"{board[x][y]}"
    st.dialog(f"{board} Hello")
    check_win()



board = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "],
]

st.title("Celebrity squares")

t = st.columns([1,1,1])

for x in range(len(board)):
    for y in range(0,len(board[x])):
        with t[y]:
            st.session_state[f"{x}{y}f"] = f"{board[x][y]}"
            st.button(st.session_state[f"{x}{y}f"],key=f"{x}{y}", on_click=popup,args=(x,y))
    st.html("</p>")




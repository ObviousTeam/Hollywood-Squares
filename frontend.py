import streamlit as st

def check_win():
    #stuff happens here
    pass

def popup():
    #stuff happens here
    check_win()
    pass



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
            st.button(board[x][y],key=f"{x}{y}", on_click=popup)
    st.html("</p>")



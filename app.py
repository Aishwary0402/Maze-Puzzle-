import streamlit as st
import numpy as np
import time
import os
from maze_utils import generate_random_maze, dijkstra
import matplotlib.pyplot as plt

# ----------------------------------
# 🌟 Streamlit App Setup
# ----------------------------------
st.set_page_config(page_title="Interactive Maze Puzzle", page_icon="🧩", layout="centered")

st.markdown("""
    <style>
        .main {
            background-color: #0E1117;
            color: white;
            text-align: center;
        }
        .stButton>button {
            border-radius: 10px;
            font-weight: bold;
            height: 3em;
            width: 7em;
            background-color: #4B8BF5;
            color: white;
        }
        .stButton>button:hover {
            background-color: #2563EB;
        }
        .maze-grid {
            font-family: monospace;
            font-size: 18px;
            line-height: 20px;
            white-space: pre;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------
# 🧩 Title and Instructions
# ----------------------------------
st.title("🧩 Interactive Maze Puzzle")
st.subheader("Can you find your way to the goal in the fewest moves?")

# Instruction image (optional)
image_path = "assets/image.png"
if os.path.exists(image_path):
    st.image(image_path, caption="How to play: Reach the goal 🟩 using arrow buttons. Avoid walls ⬛.", use_container_width=True)
else:
    st.info("ℹ️ Place your instruction image at `assets/image.png` to show gameplay guide here.")

# ----------------------------------
# 🎮 Sidebar - Game Settings
# ----------------------------------
st.sidebar.header("🎮 Game Settings")

# Difficulty selector — this controls maze size + density
difficulty = st.sidebar.radio("Select Difficulty Level", ["Easy", "Medium", "Hard"])

# Set maze parameters for each level
if difficulty == "Easy":
    rows, cols, wall_prob = 8, 8, 0.2
elif difficulty == "Medium":
    rows, cols, wall_prob = 12, 12, 0.35
else:
    rows, cols, wall_prob = 18, 18, 0.45

# ----------------------------------
# 🧠 Initialize or Reset Session
# ----------------------------------
if "difficulty" not in st.session_state or st.session_state.difficulty != difficulty:
    # If level changed, rebuild maze
    st.session_state.difficulty = difficulty
    st.session_state.maze = generate_random_maze(rows, cols, wall_prob)
    st.session_state.player = [0, 0]
    st.session_state.goal = [rows - 1, cols - 1]
    st.session_state.moves = 0
    st.session_state.start_time = time.time()
    st.session_state.trail = [[0, 0]]
    st.session_state.hint_path = []
    st.session_state.best_path = []

# Sidebar buttons
if st.sidebar.button("🔄 New Maze"):
    st.session_state.maze = generate_random_maze(rows, cols, wall_prob)
    st.session_state.player = [0, 0]
    st.session_state.goal = [rows - 1, cols - 1]
    st.session_state.moves = 0
    st.session_state.start_time = time.time()
    st.session_state.trail = [[0, 0]]
    st.session_state.hint_path = []
    st.session_state.best_path = []

if st.sidebar.button("💡 Hint (Next Step)"):
    path = dijkstra(st.session_state.maze, tuple(st.session_state.player), tuple(st.session_state.goal))
    st.session_state.hint_path = path[1:3] if len(path) > 2 else []

if st.sidebar.button("📍 Show Best Path"):
    st.session_state.best_path = dijkstra(st.session_state.maze, tuple(st.session_state.player), tuple(st.session_state.goal))

# ----------------------------------
# 🧩 Maze Rendering with Matplotlib
# ----------------------------------
maze = st.session_state.maze
rows, cols = maze.shape
player = st.session_state.player
goal = st.session_state.goal

fig, ax = plt.subplots()
ax.imshow(maze, cmap="plasma", origin="upper")

# Draw player's path (trail)
if len(st.session_state.trail) > 1:
    trail = np.array(st.session_state.trail)
    ax.plot(trail[:,1], trail[:,0], color="red", linewidth=2, marker="o")

# Draw hint (yellow)
if st.session_state.hint_path:
    hint = np.array(st.session_state.hint_path)
    ax.plot(hint[:,1], hint[:,0], color="yellow", linewidth=2, linestyle="--", marker="o")

# Draw optimal (orange)
if st.session_state.best_path:
    best = np.array(st.session_state.best_path)
    ax.plot(best[:,1], best[:,0], color="orange", linewidth=2, linestyle="--")

# Start & Goal markers
ax.text(0, 0, "S", color="white", fontsize=14, ha="center", va="center", fontweight="bold")
ax.text(goal[1], goal[0], "G", color="black", fontsize=14, ha="center", va="center", fontweight="bold")

ax.set_title("Maze visualization (0 = free, 1 = wall)")
st.pyplot(fig)

# ----------------------------------
# 🕹️ Movement Controls
# ----------------------------------
elapsed = round(time.time() - st.session_state.start_time, 1)
st.markdown(f"### Moves: {st.session_state.moves} | Time: {elapsed}s")

col1, col2, col3 = st.columns(3)
with col2:
    if st.button("⬆️"):
        new = [player[0]-1, player[1]]
        if new[0] >= 0 and maze[new[0], new[1]] == 0:
            st.session_state.player = new
            st.session_state.trail.append(new)
            st.session_state.moves += 1
with col1:
    if st.button("⬅️"):
        new = [player[0], player[1]-1]
        if new[1] >= 0 and maze[new[0], new[1]] == 0:
            st.session_state.player = new
            st.session_state.trail.append(new)
            st.session_state.moves += 1
with col3:
    if st.button("➡️"):
        new = [player[0], player[1]+1]
        if new[1] < cols and maze[new[0], new[1]] == 0:
            st.session_state.player = new
            st.session_state.trail.append(new)
            st.session_state.moves += 1

st.write("")
if st.button("⬇️"):
    new = [player[0]+1, player[1]]
    if new[0] < rows and maze[new[0], new[1]] == 0:
        st.session_state.player = new
        st.session_state.trail.append(new)
        st.session_state.moves += 1

# ----------------------------------
# 🏁 Check for Goal
# ----------------------------------
if st.session_state.player == goal:
    st.success(f"🎉 You reached the goal in {st.session_state.moves} moves and {elapsed}s!")
    if st.button("Play Again"):
        st.session_state.maze = generate_random_maze(rows, cols, wall_prob)
        st.session_state.player = [0, 0]
        st.session_state.goal = [rows - 1, cols - 1]
        st.session_state.moves = 0
        st.session_state.start_time = time.time()
        st.session_state.trail = [[0, 0]]
        st.session_state.hint_path = []
        st.session_state.best_path = []

# Magislov 🎮✨

Welcome to **Magislov**, a top-down RPG where players take on the role of a young wizard. Use voice commands to control and interact with the world around you! The game combines fantasy elements with innovative technology, offering an immersive adventure filled with battles, challenges, and magical quests. 🧙‍♂️⚡
The project is not fully finished.

[Watch the gameplay demo on YouTube](https://youtu.be/5M3P_NsG4pE)

## Features 🌟

### Dual Control Mechanism 🎮🎤
Players can control the wizard either via:
- **Keyboard** (using arrow keys, space, etc.)
- **Voice Commands** (via voice recognition libraries) */not implemented because of slow speed of free voice recognition services*/

---

### Wizard’s Abilities ✨
- **Cast fireballs** and other magical attacks! 🔥
- **Run fast** or walk normally. 🏃‍♂️
- Pick up items to use or carry (e.g., healing fruits, quest items).
- Simple interactions like opening doors, chests, and more (often with the “E” key).
- Take damage and heal! 💪
- **Level up** and unlock new abilities! 🔮
- No jumping, flying, or swimming yet. 😅

---

### Enemy AI 👹
- Basic but effective AI with two types of enemies:
  - **Melee Fighters**: Chase and attack up close.
  - **Long-range Magicians**: Keep their distance and attack with projectiles.

---

### Mini-games 🎮
Mini-games can be part of side quests or challenges to gather resources. Completing them rewards the player with **XP** or **quest progression**!

#### Types of Mini-games 🎲:
- **Quiz** (Who Wants to Be a Millionaire-style): Answer questions via voice or keyboard/mouse.
- **Memory Match**: Match a sequence of emojis. With voice control, say the emoji names in the correct order!
- **Sliding Puzzle**: Rearrange tiles to form a picture. (Voice or keyboard/mouse control).
- **Color Mixing Game**: Mix colors to match a target hue. Say the color names out loud or use the keyboard.
- **Open-world challenges**: Including epic boss fights! (optional).

---

### Leveling System 📈
- **XP system** based on completing quests and mini-games.
- **Level up** to unlock new spells and stronger abilities! 🔮
- Some areas will be locked until the player reaches a specific level.

---

### User Interface 🎨
- Control sound, visuals, and gameplay settings in menus.
- Health bar, player stats, and the playable area.

---

### Audio & Graphics 🎶🎨
- Background music tailored to each environment 🎶
- Sound effects for actions like casting spells and fighting enemies. 🎧
- Pixel art assets for characters, environments, and items. 🖼️

---

### Optional Features 🌈
- **Localization**: Add **Bulgarian** language support for dialogues and voice.
- **Side Quests**: Create quests like carrying objects for NPCs.
- **World Map**: Add a world map with teleportation options.
- **Character Customization**: Personalize the wizard’s look.

---

## Milestones ⏳

### Game Structure (12-14 hours)
- Set up the main game platform (screen, controls, etc.).
- Handle file reading/writing via **JSON** files.
- Create player character movement and actions.
- Implement projectile behavior (spells, arrows).
- Create interaction buttons and menus.
- Room-to-room transitions.

---

### Voice Recognition Integration (7-8 hours)
- Integrate a **speech recognition module** (Google Web Speech API) to enable voice commands in the game.
- Support voice commands initially in **English**, with a future plan for **Bulgarian**.

---

### Enemy AI System (6-8 hours)
- Design and implement basic AI for **Melee Fighters** and **Long-range Magicians**.

---

### Mini-game Implementation (10-12 hours)
- Develop each mini-game and integrate them into the main game.
- Add **voice control** support for each mini-game.

---

### Leveling & Progression System (5-6 hours)
- Build the **XP system** for leveling up and unlocking abilities.
- Implement life-changing items (health potions, etc.).

---

### Sound & Visuals (5-6 hours)
- Add music, sound effects, and graphical assets.
- Improve visual effects and gameplay experience.

---

### Demo Design (2-3 hours)
- Create a demo version showcasing key features of the game.

---

## Estimated Time 🕒
**Total Estimate**: 47-57 hours

---

## Technologies Used 🛠️
- **Pygame**: Main game engine for graphics and input handling. Also for sounds, images, and menus.
- **SpeechRecognition & PyAudio**: For integrating voice commands through the Google Web Speech API.
- **Python libraries**: random, os, sys, json for handling game logic and file systems.
- Optional: **Numpy** for AI algorithms and optimization.
- **Git**: Version control to manage and track changes in the project.
- Pixel Art Assets & Sounds: Pre-made pixel art assets and sound effects.

---

## Credits 🎉
- **Tutorial Author**: [Link to the tutorial I followed to some extent](https://www.youtube.com/watch?v=QU1pPzEGrqw&t=14049s).
- **Pixel Art Assets & Sound Effects**: [Link to asset providers](https://pixel-boy.itch.io/ninja-adventure-asset-pack).
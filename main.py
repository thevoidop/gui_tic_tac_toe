# Import necessary modules
import customtkinter as ctk
from random import choice, randint
try:
    from ctypes import windll, byref, sizeof, c_int
except ImportError:
    pass

# Define color constants
PRIMARY_COLOR = "#F3DE8A"
PRIMARY_HEX = 0x008adef3
BOX_BORDER_COLOR = "#331832"
X_TEXT_COLOR = "#399384"
O_TEXT_COLOR = "#C95227"

# Define the main application class
class App(ctk.CTk):
    def __init__(self):
        # Initialize the custom Tkinter application
        super().__init__(fg_color=PRIMARY_COLOR)
        self.geometry("600x600")
        self.title("Tic-Tac-Toe")
        self.iconbitmap("icon.ico")
        self.resizable(False, False)
        self.titleBarColor()  # Set the title bar color using the titleBarColor method

        # Placing buttons and initializing game state variables
        self.mainMenu()

        # Logic variables
        self.clickCount = 0
        self.win = False
        self.draw = False
        self.currentButton = None
        self.player = None # Initialize player attribute
        self.turnLogic()
        
        self.mainloop()

    # Set the title bar color (Windows only)
    def titleBarColor(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = PRIMARY_HEX
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass

    # Display the main menu with options for single and multi-player
    def mainMenu(self):
        self.gameMode = 0
        self.mainMenuFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.mainMenuFrame.pack(expand=True, fill="both")
        ctk.CTkLabel(self.mainMenuFrame, text="TIC-TAC-TOE", font=("Futura Md BT", 90), text_color="#0B4F6C").pack(
            pady=100, padx=30, expand=True,)
        singleplayer = ctk.CTkButton(self.mainMenuFrame, text="Single Player", font=("Futura Md BT", 30),
                                     fg_color=X_TEXT_COLOR, height=100, command=self.singlePlayer)
        multiplayer = ctk.CTkButton(self.mainMenuFrame, text="Multi Player", font=("Futura Md BT", 30),
                                     fg_color=X_TEXT_COLOR, height=100, command=self.multiPlayer)
        # Packing buttons
        singleplayer.pack(expand=True, padx=20, pady=20, fill="x")
        multiplayer.pack(expand=True, padx=20, pady=20, fill="x")

    # Create the game board buttons
    def createButtons(self):
        self.mainMenuFrame.pack_forget()
        self.buttonFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttonFrame.pack(expand=True, fill="both")
        self.buttonFrame.rowconfigure((0, 1, 2), weight=3, uniform="A")
        self.buttonFrame.columnconfigure((0, 1, 2), weight=1, uniform="A")
        self.buttonlist = [
            ctk.CTkButton(self.buttonFrame, text=" ", font=("Futura Md BT", 120), corner_radius=0, fg_color=PRIMARY_COLOR,
                          hover_color=PRIMARY_COLOR, border_width=4, border_color=BOX_BORDER_COLOR,
                          command=lambda i=i: self.buttonClick(self.buttonlist[i]))
            for i in range(9)
        ]
        for i, button in enumerate(self.buttonlist):
            row, col = divmod(i, 3)
            button.grid(row=row, column=col, sticky="nsew")
        self.currentPlayer()

    # Set initial turn for single player mode
    def turnLogic(self):
        self.turn = randint(0, 1)
        self.player = "O" if self.turn == 1 else "X"

    # Start single player game
    def singlePlayer(self):
        self.gameMode = 1
        self.mainMenuFrame.pack_forget()
        self.createButtons()
        if self.player == "O":
            self.after(500, self.autoPlay)

    # Start multi-player game
    def multiPlayer(self):
        self.gameMode = 2
        self.mainMenuFrame.pack_forget()
        self.createButtons()

    # Perform automatic move in single player mode
    def autoPlay(self):
        if self.player == "O" and not self.win and not self.draw and self.clickCount < 9:
            available_box = [button for button in self.buttonlist if button.cget("text") == " "]
            the_button = choice(available_box)
            if the_button.cget("text") == " ":
                the_button.configure(text="O", text_color=O_TEXT_COLOR)
                self.player = "X"
                self.clickCount += 1
                self.gameWinning()
                self.after(500, self.autoPlay)

    # Handle button click in both single and multi-player modes
    def buttonClick(self, button):
        self.currentButton = button
        if self.gameMode == 2:
            # Multi-player mode logic
            if self.player == "X" and button.cget("text") == " ":
                button.configure(text="X", text_color=X_TEXT_COLOR)
                self.player = "O"
                self.clickCount += 1
            elif self.player == "O" and button.cget("text") == " ":
                button.configure(text="O", text_color=O_TEXT_COLOR)
                self.player = "X"
                self.clickCount += 1
            self.gameWinning()
            self.currentPlayer()
        else:
            # Single player mode logic
            if self.player == "X" and button.cget("text") == " ":
                button.configure(text="X", text_color=X_TEXT_COLOR)
                self.player = "O"
                self.clickCount += 1
                self.gameWinning()
            if self.player == "O":
                self.after(600, self.autoPlay)

    # Display the current player's turn in multi-player mode
    def currentPlayer(self):
        if self.gameMode == 2:
            self.buttonFrame.update()
            self.buttonFrame.rowconfigure(3, weight=1)
            ctk.CTkLabel(self.buttonFrame, text=f"Turn: {self.player}", font=("Futura Md BT", 20),
                          text_color="#0B4F6C").grid(row=3, column=0, columnspan=3, sticky="nsew")

    # Check for a winning condition or a draw
    def gameWinning(self):
        self.winPatterns = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        self.win = False
        self.winner = None
        self.draw = False

        for pattern in self.winPatterns:
            if self.buttonlist[pattern[0]].cget("text") == self.buttonlist[pattern[1]].cget(
                    "text") == self.buttonlist[pattern[2]].cget("text") != " ":
                self.winner = self.buttonlist[pattern[0]].cget("text")
                self.win = True

        if not self.win and self.clickCount == 9:
            self.draw = True

        if self.win or self.draw:
            self.after(700, lambda: self.afterGame(self.win, self.winner, self.draw))  # Add a delay

    # Display the end game screen with winner or draw message
    def afterGame(self, win, winner, draw):
        self.buttonFrame.pack_forget()
        self.endFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.endFrame.pack(expand=True, fill="both")
        self.endFrame.rowconfigure((0, 1, 2, 3), weight=1, uniform="a")
        self.endFrame.columnconfigure(0, weight=1)
        if win:
            ctk.CTkLabel(self.endFrame, text="The winner is:", font=("Futura Md BT", 90),
                          text_color="#0B4F6C").grid(
                row=0, column=0, sticky="nsew")
            ctk.CTkLabel(self.endFrame, text=f"{winner}", font=("Futura Md BT", 90),
                          text_color="#0B4F6C").grid(
                row=1, column=0, sticky="nsew")

        if draw:
            ctk.CTkLabel(self.endFrame, text="The game was a Draw!", font=("Futura Md BT", 45),
                          text_color="#0B4F6C").grid(row=0, rowspan=2, column=0)

        # Buttons for play again and exit
        ctk.CTkButton(self.endFrame, text="Play Again", font=("Futura Md BT", 30), fg_color=X_TEXT_COLOR,
                      height=30, command=self.playAgain).grid(row=2, column=0, sticky="nsew", padx=10, pady=30)
        ctk.CTkButton(self.endFrame, text="Exit", font=("Futura Md BT", 30), fg_color=X_TEXT_COLOR,
                      height=30, command=lambda: exit()).grid(row=3, column=0, sticky="nsew", padx=10, pady=30)

    # Reset the game state for a new game
    def playAgain(self):
        self.endFrame.pack_forget()
        self.clickCount = 0
        self.win = False
        self.player = self.winner
        self.turnLogic()
        self.createButtons()
        if self.gameMode == 1:
            self.autoPlay()

# Run the application if this script is the main entry point
if __name__ == "__main__":
    App()

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import chess
import chess.pgn
from io import StringIO
import re
import os
from datetime import datetime

class CSVtoPGNConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV to PGN Database Converter")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Variables
        self.csv_file_path = tk.StringVar()
        self.pgn_file_path = tk.StringVar()
        self.min_rating = tk.IntVar(value=0)
        self.max_rating = tk.IntVar(value=3000)
        self.selected_openings = []
        self.selected_themes = []
        
        # Common chess openings
        self.openings = [
            "Sicilian Defense", "French Defense", "Caro-Kann Defense",
            "Queen's Gambit", "King's Indian Defense", "English Opening",
            "Ruy Lopez", "Italian Game", "Scandinavian Defense",
            "Alekhine Defense", "Nimzo-Indian Defense", "Queen's Indian Defense",
            "Grünfeld Defense", "Catalan Opening", "Bird's Opening",
            "Réti Opening", "Vienna Game", "King's Gambit",
            "Petrov Defense", "Pirc Defense"
        ]
        
        # Puzzle themes
        self.themes = [
            "Mate in 1", "Mate in 2", "Mate in 3", "Mate in 4+",
            "Back Rank Mate", "Smothered Mate", "Anastasia's Mate",
            "Arabian Mate", "Boden's Mate", "Légal's Mate",
            "Pin", "Fork", "Skewer", "Discovered Attack",
            "Double Attack", "Deflection", "Decoy", "Clearance",
            "Interference", "Zugzwang", "Sacrifice", "Promotion",
            "En Passant", "Castling", "Endgame", "Opening",
            "Middlegame", "Tactical", "Positional"
        ]
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        # CSV file selection
        ttk.Label(file_frame, text="CSV File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Entry(file_frame, textvariable=self.csv_file_path, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(file_frame, text="Browse", command=self.browse_csv_file).grid(row=0, column=2)
        
        # PGN file selection
        ttk.Label(file_frame, text="Output PGN:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        ttk.Entry(file_frame, textvariable=self.pgn_file_path, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 5), pady=(5, 0))
        ttk.Button(file_frame, text="Browse", command=self.browse_pgn_file).grid(row=1, column=2, pady=(5, 0))
        
        # Filters frame
        filters_frame = ttk.LabelFrame(main_frame, text="Filters", padding="10")
        filters_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        filters_frame.columnconfigure(1, weight=1)
        
        # Rating filter
        rating_frame = ttk.Frame(filters_frame)
        rating_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        rating_frame.columnconfigure(1, weight=1)
        rating_frame.columnconfigure(3, weight=1)
        
        ttk.Label(rating_frame, text="Rating Range:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Label(rating_frame, text="Min:").grid(row=0, column=1, sticky=tk.W, padx=(10, 5))
        ttk.Spinbox(rating_frame, from_=0, to=3000, textvariable=self.min_rating, width=10).grid(row=0, column=2, padx=(0, 10))
        ttk.Label(rating_frame, text="Max:").grid(row=0, column=3, sticky=tk.W, padx=(10, 5))
        ttk.Spinbox(rating_frame, from_=0, to=3000, textvariable=self.max_rating, width=10).grid(row=0, column=4, padx=(0, 10))
        
        # Opening filter
        opening_frame = ttk.Frame(filters_frame)
        opening_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        opening_frame.columnconfigure(1, weight=1)
        
        ttk.Label(opening_frame, text="Openings:").grid(row=0, column=0, sticky=(tk.W, tk.N), padx=(0, 5))
        
        # Opening listbox with scrollbar
        opening_list_frame = ttk.Frame(opening_frame)
        opening_list_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
        opening_list_frame.columnconfigure(0, weight=1)
        
        self.opening_listbox = tk.Listbox(opening_list_frame, selectmode=tk.MULTIPLE, height=6)
        opening_scrollbar = ttk.Scrollbar(opening_list_frame, orient=tk.VERTICAL, command=self.opening_listbox.yview)
        self.opening_listbox.configure(yscrollcommand=opening_scrollbar.set)
        
        self.opening_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))
        opening_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        for opening in self.openings:
            self.opening_listbox.insert(tk.END, opening)
        
        # Theme filter
        theme_frame = ttk.Frame(filters_frame)
        theme_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        theme_frame.columnconfigure(1, weight=1)
        
        ttk.Label(theme_frame, text="Themes:").grid(row=0, column=0, sticky=(tk.W, tk.N), padx=(0, 5))
        
        # Theme listbox with scrollbar
        theme_list_frame = ttk.Frame(theme_frame)
        theme_list_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
        theme_list_frame.columnconfigure(0, weight=1)
        
        self.theme_listbox = tk.Listbox(theme_list_frame, selectmode=tk.MULTIPLE, height=6)
        theme_scrollbar = ttk.Scrollbar(theme_list_frame, orient=tk.VERTICAL, command=self.theme_listbox.yview)
        self.theme_listbox.configure(yscrollcommand=theme_scrollbar.set)
        
        self.theme_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))
        theme_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        for theme in self.themes:
            self.theme_listbox.insert(tk.END, theme)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Button(button_frame, text="Preview Data", command=self.preview_data).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Convert", command=self.convert_csv_to_pgn).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(button_frame, text="Clear Filters", command=self.clear_filters).grid(row=0, column=2)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to convert CSV to PGN")
        self.status_label.grid(row=4, column=0, columnspan=2, sticky=tk.W)
        
        # Log text area
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        self.log_text = tk.Text(log_frame, height=10, wrap=tk.WORD)
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
    def log_message(self, message):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def browse_csv_file(self):
        filename = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.csv_file_path.set(filename)
            self.log_message(f"Selected CSV file: {os.path.basename(filename)}")
            
    def browse_pgn_file(self):
        filename = filedialog.asksaveasfilename(
            title="Save PGN file as",
            defaultextension=".pgn",
            filetypes=[("PGN files", "*.pgn"), ("All files", "*.*")]
        )
        if filename:
            self.pgn_file_path.set(filename)
            self.log_message(f"Output file set: {os.path.basename(filename)}")
            
    def clear_filters(self):
        """Clear all filters"""
        self.min_rating.set(0)
        self.max_rating.set(3000)
        self.opening_listbox.selection_clear(0, tk.END)
        self.theme_listbox.selection_clear(0, tk.END)
        self.log_message("Filters cleared")
        
    def get_selected_filters(self):
        """Get currently selected filters"""
        # Get selected openings
        selected_opening_indices = self.opening_listbox.curselection()
        self.selected_openings = [self.openings[i] for i in selected_opening_indices]
        
        # Get selected themes
        selected_theme_indices = self.theme_listbox.curselection()
        self.selected_themes = [self.themes[i] for i in selected_theme_indices]
        
    def validate_pgn_moves(self, moves_str):
        """Validate if moves string is valid PGN"""
        try:
            if not moves_str or pd.isna(moves_str):
                return False
            
            # Create a new game and try to parse moves
            game = chess.pgn.Game()
            board = game.board()
            
            # Clean up the moves string
            moves_str = str(moves_str).strip()
            
            # Remove move numbers and extra whitespace
            moves_str = re.sub(r'\d+\.+', '', moves_str)
            moves_str = re.sub(r'\s+', ' ', moves_str).strip()
            
            if not moves_str:
                return False
            
            moves = moves_str.split()
            
            for move in moves:
                move = move.strip()
                if not move:
                    continue
                    
                # Skip annotations and comments
                if move.startswith('(') or move.startswith('{'):
                    continue
                    
                # Remove check/checkmate symbols and annotations
                clean_move = re.sub(r'[+#!?]+$', '', move)
                
                if clean_move and clean_move not in ['1-0', '0-1', '1/2-1/2', '*']:
                    try:
                        board.push_san(clean_move)
                    except (chess.InvalidMoveError, chess.IllegalMoveError):
                        return False
            
            return True
        except Exception:
            return False
            
    def matches_theme(self, moves_str, themes):
        """Check if game matches selected themes"""
        if not themes:
            return True
            
        moves_str = str(moves_str).lower()
        
        for theme in themes:
            theme_lower = theme.lower()
            
            # Simple theme matching logic
            if 'mate in 1' in theme_lower and ('mate in 1' in moves_str or '#' in moves_str):
                return True
            elif 'mate in 2' in theme_lower and 'mate in 2' in moves_str:
                return True
            elif 'mate in 3' in theme_lower and 'mate in 3' in moves_str:
                return True
            elif 'mate in 4' in theme_lower and 'mate in 4' in moves_str:
                return True
            elif 'pin' in theme_lower and 'pin' in moves_str:
                return True
            elif 'fork' in theme_lower and 'fork' in moves_str:
                return True
            elif 'skewer' in theme_lower and 'skewer' in moves_str:
                return True
            elif 'sacrifice' in theme_lower and ('sacrifice' in moves_str or 'sac' in moves_str):
                return True
            elif 'endgame' in theme_lower and 'endgame' in moves_str:
                return True
            elif 'opening' in theme_lower and 'opening' in moves_str:
                return True
            elif 'middlegame' in theme_lower and 'middlegame' in moves_str:
                return True
                
        return False
        
    def matches_opening(self, opening_str, selected_openings):
        """Check if game matches selected openings"""
        if not selected_openings:
            return True
            
        if not opening_str or pd.isna(opening_str):
            return False
            
        opening_str = str(opening_str).lower()
        
        for selected_opening in selected_openings:
            if selected_opening.lower() in opening_str:
                return True
                
        return False
        
    def preview_data(self):
        """Preview the CSV data and show statistics"""
        if not self.csv_file_path.get():
            messagebox.showerror("Error", "Please select a CSV file first")
            return
            
        try:
            self.log_message("Loading CSV file for preview...")
            df = pd.read_csv(self.csv_file_path.get())
            
            # Show basic statistics
            total_games = len(df)
            columns = list(df.columns)
            
            preview_text = f"CSV Preview:\n"
            preview_text += f"Total games: {total_games}\n"
            preview_text += f"Columns: {', '.join(columns)}\n\n"
            preview_text += f"First 5 rows:\n{df.head().to_string()}"
            
            # Create preview window
            preview_window = tk.Toplevel(self.root)
            preview_window.title("CSV Preview")
            preview_window.geometry("800x600")
            
            preview_text_widget = tk.Text(preview_window, wrap=tk.WORD)
            preview_scrollbar = ttk.Scrollbar(preview_window, orient=tk.VERTICAL, command=preview_text_widget.yview)
            preview_text_widget.configure(yscrollcommand=preview_scrollbar.set)
            
            preview_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            preview_text_widget.insert(tk.END, preview_text)
            preview_text_widget.config(state=tk.DISABLED)
            
            self.log_message(f"Preview loaded: {total_games} games found")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview CSV file: {str(e)}")
            self.log_message(f"Error previewing file: {str(e)}")
            
    def convert_csv_to_pgn(self):
        """Main conversion function"""
        if not self.csv_file_path.get():
            messagebox.showerror("Error", "Please select a CSV file")
            return
            
        if not self.pgn_file_path.get():
            messagebox.showerror("Error", "Please specify output PGN file")
            return
            
        try:
            self.get_selected_filters()
            self.log_message("Starting conversion...")
            self.status_label.config(text="Loading CSV file...")
            
            # Load CSV
            df = pd.read_csv(self.csv_file_path.get())
            total_games = len(df)
            self.log_message(f"Loaded {total_games} games from CSV")
            
            # Set up progress bar
            self.progress['maximum'] = total_games
            self.progress['value'] = 0
            
            converted_games = 0
            skipped_games = 0
            
            with open(self.pgn_file_path.get(), 'w', encoding='utf-8') as pgn_file:
                for index, row in df.iterrows():
                    # Update progress
                    self.progress['value'] = index + 1
                    self.status_label.config(text=f"Processing game {index + 1}/{total_games}")
                    
                    if index % 100 == 0:  # Update every 100 games
                        self.root.update_idletasks()
                    
                    # Apply filters
                    if not self.apply_filters(row):
                        skipped_games += 1
                        continue
                    
                    # Convert row to PGN
                    game = self.row_to_pgn_game(row)
                    if game:
                        pgn_file.write(str(game) + "\n\n")
                        converted_games += 1
                    else:
                        skipped_games += 1
            
            self.progress['value'] = total_games
            self.status_label.config(text="Conversion completed!")
            
            success_msg = f"Conversion completed!\n"
            success_msg += f"Converted: {converted_games} games\n"
            success_msg += f"Skipped: {skipped_games} games\n"
            success_msg += f"Output file: {self.pgn_file_path.get()}"
            
            self.log_message(success_msg)
            messagebox.showinfo("Success", success_msg)
            
        except Exception as e:
            error_msg = f"Conversion failed: {str(e)}"
            self.log_message(error_msg)
            messagebox.showerror("Error", error_msg)
            self.status_label.config(text="Conversion failed!")
            
    def apply_filters(self, row):
        """Apply all filters to a game row"""
        # Rating filter
        rating_cols = ['rating', 'white_rating', 'black_rating', 'player_rating']
        game_rating = None
        
        for col in rating_cols:
            if col in row and not pd.isna(row[col]):
                try:
                    game_rating = int(float(row[col]))
                    break
                except (ValueError, TypeError):
                    continue
        
        if game_rating is not None:
            if game_rating < self.min_rating.get() or game_rating > self.max_rating.get():
                return False
        
        # Opening filter
        opening_cols = ['opening', 'opening_name', 'eco']
        game_opening = None
        
        for col in opening_cols:
            if col in row and not pd.isna(row[col]):
                game_opening = str(row[col])
                break
        
        if not self.matches_opening(game_opening, self.selected_openings):
            return False
        
        # Theme filter
        moves_cols = ['moves', 'pgn', 'game_moves', 'notation']
        game_moves = None
        
        for col in moves_cols:
            if col in row and not pd.isna(row[col]):
                game_moves = str(row[col])
                break
        
        if not self.matches_theme(game_moves, self.selected_themes):
            return False
            
        return True
        
    def row_to_pgn_game(self, row):
        """Convert a CSV row to a PGN game object"""
        try:
            game = chess.pgn.Game()
            
            # Set headers from CSV columns
            header_mapping = {
                'event': ['event', 'tournament', 'competition'],
                'site': ['site', 'location', 'venue'],
                'date': ['date', 'game_date', 'played_date'],
                'round': ['round', 'round_number'],
                'white': ['white', 'white_player', 'player1'],
                'black': ['black', 'black_player', 'player2'],
                'result': ['result', 'game_result'],
                'eco': ['eco', 'opening_code'],
                'opening': ['opening', 'opening_name'],
                'whiteelo': ['white_rating', 'white_elo', 'rating1'],
                'blackelo': ['black_rating', 'black_elo', 'rating2'],
                'timecontrol': ['time_control', 'timecontrol'],
                'termination': ['termination', 'end_reason']
            }
            
            # Set standard headers
            for pgn_header, csv_columns in header_mapping.items():
                for csv_col in csv_columns:
                    if csv_col in row and not pd.isna(row[csv_col]):
                        game.headers[pgn_header.title()] = str(row[csv_col])
                        break
            
            # Default values if not found
            if 'Event' not in game.headers:
                game.headers['Event'] = 'Unknown'
            if 'Site' not in game.headers:
                game.headers['Site'] = 'Unknown'
            if 'Date' not in game.headers:
                game.headers['Date'] = '????.??.??'
            if 'Round' not in game.headers:
                game.headers['Round'] = '?'
            if 'White' not in game.headers:
                game.headers['White'] = 'Unknown'
            if 'Black' not in game.headers:
                game.headers['Black'] = 'Unknown'
            if 'Result' not in game.headers:
                game.headers['Result'] = '*'
            
            # Add moves
            moves_cols = ['moves', 'pgn', 'game_moves', 'notation']
            moves_str = None
            
            for col in moves_cols:
                if col in row and not pd.isna(row[col]):
                    moves_str = str(row[col]).strip()
                    break
            
            if moves_str and self.validate_pgn_moves(moves_str):
                # Parse moves
                board = game.board()
                
                # Clean up moves string
                moves_str = re.sub(r'\d+\.+', '', moves_str)
                moves_str = re.sub(r'\s+', ' ', moves_str).strip()
                
                moves = moves_str.split()
                node = game
                
                for move in moves:
                    move = move.strip()
                    if not move or move in ['1-0', '0-1', '1/2-1/2', '*']:
                        continue
                        
                    # Remove annotations
                    clean_move = re.sub(r'[+#!?]+$', '', move)
                    
                    if clean_move:
                        try:
                            chess_move = board.push_san(clean_move)
                            node = node.add_variation(chess_move)
                        except (chess.InvalidMoveError, chess.IllegalMoveError):
                            break
            
            return game
            
        except Exception as e:
            self.log_message(f"Error converting row to PGN: {str(e)}")
            return None

def main():
    root = tk.Tk()
    app = CSVtoPGNConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
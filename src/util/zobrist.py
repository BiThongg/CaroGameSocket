from random import randint
import pickle
from threading import Thread
import os

from util.cell import Cell


def exists(file_path):
    # Check if the file exists
    try:
        with open(file_path, 'r') as file:
            return True
    except FileNotFoundError:
        return False


class ZobristTable:
    def __init__(self, width: int, height: int, pieces: int):
        self.width = width  
        self.height = height
        self.pieces = pieces
        self.current_hash = 0
        self.MAX_CACHE_SIZE = 1000000  # Limit cache size to 1 million entries
        
        self.cache = {}
        if exists("zobrist_cache.pkl"):
            self.load_cache("zobrist_cache.pkl")
        
        self.table: dict[tuple[int, int], int] = {}
        if exists("zobrist_table.pkl"):
            self.load_generated_table("zobrist_table.pkl")
        else:
            self.generate_zobrist_table()
            self.save_generated_table("zobrist_table.pkl")

    def generate_zobrist_table(self):
        # Initialize the Zobrist table with random values
        for piece in range(self.pieces):
            for square in range(self.width * self.height):
                self.table[(piece, square)] = randint(0, 2**64 - 1)
        # Save the generated table to a file
        self.save_generated_table("zobrist_table.pkl")
    
    def get_hash(self, x: int, y: int, piece: int) -> int:
        return self.table.get((piece, y * self.width + x), 0)
    
    def update_hash(self, current_hash, x, y, piece: Cell) -> int:
        value = 0
        if piece == Cell.X:
            value = 1
        elif piece == Cell.O:
            value = 2
        return current_hash ^ self.get_hash(x, y, value)
    
    def load_generated_table(self, file_path):
        # Load the Zobrist table from a file
        with open(file_path, 'rb') as file:
            self.table = pickle.load(file)
                
    def save_generated_table(self, file_path):
        # Save the Zobrist table to a file using pickle
        with open(file_path, 'wb') as file:
            pickle.dump(self.table, file)
                
    def save_cache(self, file_path):
        # Save the cache to a file using pickle
        with open(file_path, 'wb') as file:
            pickle.dump(self.cache, file)
    
    def load_cache(self, file_path):
        # Load the cache from a file using pickle
        try:
            if not exists(file_path):
                print("Cache file does not exist, creating new cache")
                self.cache = {}
                return
                
            if os.path.getsize(file_path) == 0:
                print("Cache file is empty, creating new cache")
                self.cache = {}
                return
                
            with open(file_path, 'rb') as file:
                self.cache = pickle.load(file)
        except (EOFError, pickle.UnpicklingError) as e:
            print(f"Error loading cache (file may be corrupted): {str(e)}")
            self.cache = {}
        except Exception as e:
            print(f"Unexpected error loading cache: {str(e)}")
            self.cache = {}

    def compute_hash(self, board: list[list[Cell]]) -> int:
        # Compute the hash for the current board state
        self.current_hash = 0
        for y in range(self.height):
            for x in range(self.width):
                piece = board[y][x]
                if piece != Cell.NONE:
                    piece_value = 0 if piece == Cell.X else 1
                    self.current_hash ^= self.get_hash(x, y, piece_value)
        return self.current_hash
    
    # Lets cache :bruh: 🤫🤫
    def lets_cache(self, x, y, piece, value):
        new_hash = self.update_hash(self.current_hash, x, y, piece)
        self.current_hash = new_hash
        
        # Implement cache size limit
        if len(self.cache) >= self.MAX_CACHE_SIZE:
            # Remove oldest entries if cache is full
            self.cache = dict(list(self.cache.items())[-self.MAX_CACHE_SIZE//2:])
            
        self.cache[new_hash] = value
        
        # Save cache in background if needed
        if len(self.cache) % 100 == 0:  # Save every 100 entries
            Thread(target=self.save_cache, args=("zobrist_cache.pkl",), daemon=True).start()

    def get_cache(self, x, y, piece):
        new_hash = self.update_hash(self.current_hash, x, y, piece)
        value = self.cache.get(new_hash, None)
        if value is not None:
            print("Cache hit for", x, y, piece, ":", value)
            return value
        return None


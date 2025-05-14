from secrets import randbits
import os
from threading import Thread, Lock
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
        self._cache_lock = Lock()
        self.MAX_CACHE_SIZE = 1000000  # Limit cache size to 1 million entries
        
        self.cache = {}
        if exists("zobrist_cache.txt") and self.cache == {}:
            self.load_cache("zobrist_cache.txt")
        
        self.table: dict[tuple[int, int], int] = {}
        if exists("zobrist_table.txt"):
            self.load_generated_table("zobrist_table.txt")
        else:
            self.generate_zobrist_table()
            self.save_generated_table("zobrist_table.txt")

    def generate_zobrist_table(self):
        # Initialize the Zobrist table with random values
        for piece in range(self.pieces):
            for square in range(self.width * self.height):
                self.table[(piece, square)] = randbits(64)
        # Save the generated table to a file
        self.save_generated_table("zobrist_table.txt")
    
    def get_hash(self, x: int, y: int, piece: int) -> int:
        return self.table.get((piece, y * self.width + x), 0)
    
    def update_hash(self, current_hash, x, y, cell: Cell) -> int:
        return current_hash ^ self.get_hash(x, y, cell.toInt())
    
    def load_generated_table(self, file_path):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    if line.strip():
                        piece, square, value = map(int, line.strip().split(','))
                        self.table[(piece, square)] = value
        except Exception as e:
            print(f"Error loading Zobrist table: {str(e)}")
            self.generate_zobrist_table()
            self.save_generated_table(file_path)
                
    def save_generated_table(self, file_path):
        # Save the Zobrist table to a text file
        with open(file_path, 'w') as file:
            for (piece, square), value in self.table.items():
                file.write(f"{piece},{square},{value}\n")
                
    def save_cache(self, file_path):
        # Save the cache to a text file
        with open(file_path, 'w') as file:
            for hash_value, value in self.cache.items():
                file.write(f"{hash_value},{value}\n")
    
    def load_cache(self, file_path):
        try:
            if not exists(file_path) or os.path.getsize(file_path) == 0:
                print("Cache file does not exist or is empty, creating new cache")
                self.cache = {}
                return
            with open(file_path, 'r') as file:
                for line in file:
                    try:
                        if line.strip():
                            hash_value, value = map(int, line.strip().split(','))
                            self.cache[hash_value] = value
                    except ValueError:
                        print(f"Skipping malformed cache line: {line.strip()}")
        except Exception as e:
            print(f"Error loading cache: {str(e)}")
            self.cache = {}
            

    def compute_hash(self, board: list[list[Cell]]) -> int:
        # Compute the hash for the current board state
        current_hash = 0
        for y in range(self.height):
            for x in range(self.width):
                cell = board[y][x]
                current_hash ^= self.get_hash(x, y, cell.toInt())
        return current_hash
    
    # Lets cache :bruh: 🤫🤫
    def lets_cache(self, current_hash, x, y, cell, value):
        new_hash = self.update_hash(current_hash, x, y, cell)

        with self._cache_lock:
            if len(self.cache) >= self.MAX_CACHE_SIZE:
                self.cache = dict(list(self.cache.items())[-self.MAX_CACHE_SIZE//2:])
            self.cache[new_hash] = value
            if len(self.cache) % 100 == 0:  # Save less frequently
                Thread(target=self.save_cache, args=("zobrist_cache.txt",), daemon=True).start()

    def get_cache(self, current_hash, x, y, cell):
        new_hash = self.update_hash(current_hash, x, y, cell)
        value = self.cache.get(new_hash, None)
        if value is not None:
            print("Cache hit for", (y, x), cell, ":", value)
            return value
        return None


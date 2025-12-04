"""
NumPy fallback for systems without numpy installed.

Provides minimal numpy-like interface for basic operations.
"""

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    
    # Minimal numpy fallback
    class np:
        """Minimal numpy fallback."""
        
        @staticmethod
        def array(data, dtype=None):
            """Convert to list/array-like with operator support."""
            if isinstance(data, (list, tuple)):
                return ArrayLike(list(data))
            return ArrayLike([data])
        
        @staticmethod
        def zeros(shape, dtype=None):
            """Create zeros array."""
            if isinstance(shape, int):
                return ArrayLike([0.0] * shape)
            elif isinstance(shape, tuple):
                size = 1
                for s in shape:
                    size *= s
                return ArrayLike([0.0] * size)
            return ArrayLike([0.0])
        
        @staticmethod
        def random_normal(loc=0.0, scale=1.0, size=None):
            """Generate random normal values."""
            import random
            if size is None:
                return random.gauss(loc, scale)
            if isinstance(size, int):
                return ArrayLike([random.gauss(loc, scale) for _ in range(size)])
            elif isinstance(size, tuple):
                total = 1
                for s in size:
                    total *= s
                return ArrayLike([random.gauss(loc, scale) for _ in range(total)])
            return random.gauss(loc, scale)
        
        @staticmethod
        def linalg_norm(vec):
            """Compute vector norm."""
            if not vec:
                return 0.0
            # Handle ArrayLike objects
            if hasattr(vec, 'data'):
                data = vec.data
            elif isinstance(vec, (list, tuple)):
                data = vec
            else:
                data = [vec]
            return sum(x * x for x in data) ** 0.5
        
        @staticmethod
        def dot(a, b):
            """Dot product."""
            if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
                return sum(x * y for x, y in zip(a, b))
            return a * b
        
        class linalg:
            @staticmethod
            def norm(vec):
                # Handle ArrayLike objects
                if hasattr(vec, 'data'):
                    data = vec.data
                elif isinstance(vec, (list, tuple)):
                    data = vec
                else:
                    data = [vec]
                return sum(x * x for x in data) ** 0.5
        
        ndarray = list
        
    # Array-like class that supports basic operations
    class ArrayLike:
        """Array-like class that supports basic numpy operations."""
        def __init__(self, data):
            self.data = list(data) if not isinstance(data, list) else data
        
        def __truediv__(self, other):
            """Division operator."""
            if isinstance(other, (int, float)):
                return ArrayLike([x / other for x in self.data])
            return NotImplemented
        
        def __mul__(self, other):
            """Multiplication operator."""
            if isinstance(other, (int, float)):
                return ArrayLike([x * other for x in self.data])
            return NotImplemented
        
        def __rmul__(self, other):
            """Right-side multiplication operator (for float * ArrayLike)."""
            if isinstance(other, (int, float)):
                return ArrayLike([other * x for x in self.data])
            return NotImplemented
        
        def __add__(self, other):
            """Addition operator."""
            if isinstance(other, ArrayLike):
                return ArrayLike([x + y for x, y in zip(self.data, other.data)])
            elif isinstance(other, (int, float)):
                return ArrayLike([x + other for x in self.data])
            return NotImplemented
        
        def __radd__(self, other):
            """Right-side addition operator."""
            return self.__add__(other)
        
        def __getitem__(self, key):
            """Indexing."""
            return self.data[key]
        
        def __setitem__(self, key, value):
            """Assignment."""
            self.data[key] = value
        
        def __len__(self):
            """Length."""
            return len(self.data)
        
        def tolist(self):
            """Convert to list."""
            return self.data
        
        def copy(self):
            """Copy array."""
            return ArrayLike(self.data[:])
        
        def __iter__(self):
            """Iteration."""
            return iter(self.data)
        
        def __repr__(self):
            return f"ArrayLike({self.data})"
else:
    # If numpy is available, ArrayLike is just an alias
    ArrayLike = np.ndarray


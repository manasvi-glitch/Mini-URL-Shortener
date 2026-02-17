import hashlib

class Base62Encoder:
    """Convert numbers to base62 for short codes"""
    
    CHARSET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    @staticmethod
    def encode(num):
        """Convert number to base62 string"""
        if num == 0:
            return Base62Encoder.CHARSET[0]
        
        result = []
        while num > 0:
            result.append(Base62Encoder.CHARSET[num % 62])
            num //= 62
        
        return ''.join(reversed(result))
    
    @staticmethod
    def decode(code):
        """Convert base62 string back to number"""
        result = 0
        for char in code:
            result = result * 62 + Base62Encoder.CHARSET.index(char)
        return result
    
    @staticmethod
    def generate_hash_code(url, length=6):
        """Generate a random-looking short code from URL using hash"""
        # Create MD5 hash of the URL
        hash_object = hashlib.md5(url.encode())
        hash_hex = hash_object.hexdigest()
        
        # Convert first part of hex to integer
        hash_int = int(hash_hex[:16], 16)
        
        # Convert to base62
        if hash_int == 0:
            return Base62Encoder.CHARSET[0] * length
        
        result = []
        while hash_int > 0 and len(result) < length:
            result.append(Base62Encoder.CHARSET[hash_int % 62])
            hash_int //= 62
        
        # Pad with random characters if needed
        while len(result) < length:
            result.append(Base62Encoder.CHARSET[0])
        
        return ''.join(reversed(result[:length]))
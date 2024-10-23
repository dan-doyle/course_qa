class ChunkProcessor:
    def __init__(self, data, strategy):
        self.strategy = strategy
        self.data = data

    def process(self):
        return self.strategy.execute(self.data)


class KeywordStrategy:
    def __init__(self, get_token_length, keyword, max_tokens=512):
        self.get_token_length = get_token_length
        self.max_tokens = max_tokens
        self.keyword = keyword

    def execute(self, data):
        chunks = data.split(self.keyword)
        chunks = (chunk.strip() for chunk in chunks if chunk.strip())
        return self._split_large_chunks(chunks)

    def _split_large_chunks(self, chunks):
        for chunk in chunks:
            token_length = self.get_token_length(chunk)
            if token_length <= self.max_tokens:
                yield chunk
            else:
                yield from self._split_by_token_limit(chunk)

    def _split_by_token_limit(self, chunk):
        words = chunk.split()

        def recursive_split(words):
            if not words:
                return
            
            total_length = self.get_token_length(' '.join(words))
            if total_length <= self.max_tokens:
                yield ' '.join(words)
            else:
                half_index = len(words) // 2
                first_half = words[:half_index]
                second_half = words[half_index:]
                
                yield from recursive_split(first_half)
                yield from recursive_split(second_half)

        yield from recursive_split(words)

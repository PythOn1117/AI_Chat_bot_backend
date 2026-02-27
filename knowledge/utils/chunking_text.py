import re
from typing import Dict, List


class ChunkingStrategy:
    """文本切块策略基类"""
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """切分文本并返回带元数据的块"""
        raise NotImplementedError


class SemanticChunking(ChunkingStrategy):
    """语义切分（保持语义完整性）"""

    def __init__(self, threshold: float = 0.8):
        super().__init__()
        self.threshold = threshold

    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        # 使用句子边界和语义相似度进行切分
        sentences = re.split(r'[。！？；\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        chunks = []
        current_chunk = []

        for sentence in sentences:
            if not current_chunk:
                current_chunk.append(sentence)
            else:
                # 这里可以添加语义相似度判断
                # 如果当前句子与chunk语义相似度高，则加入同一chunk
                current_chunk.append(sentence)

            if len(''.join(current_chunk)) > self.chunk_size:
                chunks.append(' '.join(current_chunk[:-1]))
                current_chunk = [current_chunk[-1]]

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return [
            {
                "text": chunk,
                # "metadata": metadata or {},
                "chunk_size": len(chunk),
                "chunk_index": i
            }
            for i, chunk in enumerate(chunks)
        ]

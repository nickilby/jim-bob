from jim_bob.models.block_type import BlockType


class BlockInfo:
    def __init__(self, block_type: BlockType):
        self.block_type = block_type

    block_id: str
    block_version: int

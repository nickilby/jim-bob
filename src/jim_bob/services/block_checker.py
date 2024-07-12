from requests.structures import CaseInsensitiveDict

from jim_bob.models.block_info import BlockInfo
from jim_bob.models.block_type import BlockType


def check_block(headers: CaseInsensitiveDict[str]) -> BlockInfo:
    block_info = BlockInfo(BlockType.NONE)
    if headers.get("x-alias") is None:
        return block_info

    block_id = headers.get("x-block-id")
    if block_id is None:
        block_info.block_type = BlockType.PROXY
    else:
        block_info.block_type = BlockType.BLOCK

    return block_info

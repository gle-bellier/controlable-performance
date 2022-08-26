import torch
import pytest
from typing import Tuple


@pytest.mark.parametrize("input_shape, stride, expected",
                         [((13, 2, 1024), 2, (13, 16, 512)),
                          ((13, 2, 1024), 1, (13, 16, 1024)),
                          ((13, 2, 1024), 4, (13, 4, 256))])
def test_down_block_shape(input_shape: Tuple[int], stride: int,
                          expected: Tuple[int]) -> None:
    """Test shape of output of upsampling block.

    Args:
        input_shape (Tuple[int]): input shape (B C_in L_in).
        stride (int): stride of the up block.
        expected (Tuple[int]): expected output shape (B C_out L_out).
    """

    from models.blocks.down_block import DownBlock

    batch_size = input_shape[0]
    in_c, out_c = input_shape[1], expected[1]
    sample_length = input_shape[-1]

    down = DownBlock(sample_length, in_c, out_c, stride, 2)

    x = torch.randn(input_shape)
    noise_scale = torch.randn(batch_size, 512)

    assert down(x, noise_scale).shape == expected


@pytest.mark.parametrize("input_shape, stride, expected",
                         [((13, 2, 1024), 2, (13, 16, 2048)),
                          ((13, 2, 1024), 1, (13, 16, 1024)),
                          ((13, 2, 1024), 4, (13, 4, 4096))])
def test_up_block_shape(input_shape: Tuple[int], stride: int,
                        expected: Tuple[int]) -> None:
    """Test shape of output of upsampling block.

    Args:
        input_shape (Tuple[int]): input shape (B C_in L_in).
        stride (int): stride of the up block.
        expected (Tuple[int]): expected output shape (B C_out L_out).
    """

    from models.blocks.up_block import UpBlock

    batch_size = input_shape[0]
    in_c, out_c = input_shape[1], expected[1]
    sample_length = input_shape[-1]

    up = UpBlock(sample_length, in_c, out_c, stride, 2)

    x = torch.randn(input_shape)
    skip = torch.randn(input_shape)
    noise_scale = torch.randn(batch_size, 512)

    assert up(x, skip, noise_scale).shape == expected

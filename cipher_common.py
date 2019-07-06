from typing import Any, Callable


def encrypt_file(pt_filename: str, ct_filename: str, k: Any,
                 pt_chunk_encrypt_func: Callable[[bytes, Any, int], bytes],
                 pt_chunk_length: int, ct_chunk_length: int) -> None:
    with open(pt_filename, 'rb') as pt, open(ct_filename, 'wb') as ct:
        while True:
            curr_pt_chunk = pt.read(pt_chunk_length)

            # near EOF, short read
            if len(curr_pt_chunk) != pt_chunk_length:
                if len(curr_pt_chunk) == 0:
                    # actual EOF
                    break
                else:
                    # pad with zero bytes
                    curr_pt_chunk += bytes(pt_chunk_length - len(curr_pt_chunk))

            curr_ct_chunk = pt_chunk_encrypt_func(curr_pt_chunk, k, ct_chunk_length)
            ct.write(curr_ct_chunk)


def decrypt_file(pt_filename: str, ct_filename: str, k: Any,
                 ct_chunk_decrypt_func: Callable[[bytes, Any, int], bytes],
                 pt_chunk_length: int, ct_chunk_length: int) -> None:
    with open(ct_filename, 'rb') as ct, open(pt_filename, 'wb') as pt:
        while True:
            curr_ct_chunk = ct.read(ct_chunk_length)

            # near EOF, short read
            if len(curr_ct_chunk) != ct_chunk_length:
                if len(curr_ct_chunk) == 0:
                    # actual EOF
                    break
                else:
                    # wrong format
                    raise ValueError("decrypt_file: ciphertext file not padded")

            curr_pt_chunk = ct_chunk_decrypt_func(curr_ct_chunk, k, pt_chunk_length)
            pt.write(curr_pt_chunk)

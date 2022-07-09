
def read_wavefile(filepath):
  print(f'Parsing file: {filepath}\n')

  with open(filepath, 'rb') as f:
    # first 4 bytes are supposed to be a binary representation of 'RIFF', ie 52 49 46 46
    riff = f.read(4)

    if riff != b'RIFF':
      raise Exception('Invalid RIFF header')
    else:
      print('RIFF header is valid')

    # next 4 bytes are supposed to represent the chunk size
    chunk_size = f.read(4)
    chunk_size = int.from_bytes(chunk_size, byteorder='little')
    print(f'Chunk size: {chunk_size}')

    # next 4 bytes are supposed to be a binary representation of 'WAVE', ie 57 41 56 45
    wave = f.read(4)
    if (wave != b'WAVE'):
      raise Exception('Invalid WAVE header')
    else:
      print('WAVE header is valid\n')


    # next 4 bytes are supposed to be a binary representation of 'fmt ', ie 66 74 2d 20
    fmt = f.read(4)
    if (fmt != b'fmt '):
      raise Exception('Invalid fmt header')
    else:
      print('fmt header is valid')

    # next 4 bytes are supposed to represent the first subchunk size
    subchunk1_size = f.read(4)
    subchunk1_size = int.from_bytes(subchunk1_size, byteorder='little')
    print(f'Subchunk1 size: {subchunk1_size} bytes')

    # next 2 bytes are supposed to be a binary representation of the audio format
    audio_format = f.read(2)
    audio_format = int.from_bytes(audio_format, byteorder='little')
    print(f"Audio format: {audio_format} ({'PCM' if audio_format == 1 else 'Compressed Audio'})")

    # next 2 bytes are supposed to be a binary representation of the number of channels
    num_channels = f.read(2)
    num_channels = int.from_bytes(num_channels, byteorder='little')
    print(f"Number of channels: {num_channels} ({'Mono' if num_channels == 1 else 'Stereo'})")

    # next 4 bytes are supposed to represent the sample rate
    sample_rate = f.read(4)
    sample_rate = int.from_bytes(sample_rate, byteorder='little')
    print(f"Sample rate: {sample_rate}")

    # next 4 bytes are supposed to represent the byte rate
    byte_rate = f.read(4)
    byte_rate = int.from_bytes(byte_rate, byteorder='little')
    print(f"Byte rate: {byte_rate}")

    # next 2 bytes are supposed to represent the block align
    block_align = f.read(2)
    block_align = int.from_bytes(block_align, byteorder='little')
    print(f"Block align: {block_align}")

    # next 2 bytes are supposed to represent the bits per sample
    bits_per_sample = f.read(2)
    bits_per_sample = int.from_bytes(bits_per_sample, byteorder='little')
    print(f"Bits per sample: {bits_per_sample} bits\n")

    # perform checks
    print('Performing additional checks for the integrity of the file...')

    # byte_rate must be equal to sample_rate * num_channels * bits_per_sample / 8
    if (byte_rate != sample_rate * num_channels * bits_per_sample / 8):
      raise Exception('Byte rate is not equal to sample rate * number of channels * bits per sample / 8')
    else:
      print('Byte rate corresponds to expected value')
    
    # block_align must be equal to num_channels * bits_per_sample / 8
    if (block_align != num_channels * bits_per_sample / 8):
      raise Exception('Block align is not equal to number of channels * bits per sample / 8')
    else:
      print('Block align corresponds to expected value')

    print('Verification passed!\n')

    # next 4 bytes are supposed to be a binary representation of 'data', ie 64 61 74 61
    data = f.read(4)
    if (data != b'data'):
      raise Exception('Invalid data header')
    else:
      print('data header is valid')

    # next 4 bytes are supposed to represent the second subchunk size
    subchunk2_size = f.read(4)
    subchunk2_size = int.from_bytes(subchunk2_size, byteorder='little')
    print(f'Subchunk2 size: {subchunk2_size} bytes')

    # read the actual sound data
    sound_data = f.read(subchunk2_size)
    print('Successfully read sound data\n')

    # read remaining bytes 
    remaining_bytes = f.read()
    print(f'Remaining data: {remaining_bytes} bytes')

  return {
    'chunk_size': chunk_size,
    'audio_format': audio_format,
    'num_channels': num_channels,
    'sample_rate': sample_rate,
    'byte_rate': byte_rate,
    'block_align': block_align,
    'bits_per_sample': bits_per_sample,
    'subchunk2_size': subchunk2_size,
    'sound_data': sound_data,
    'remaining': remaining_bytes
  }

if __name__ == '__main__':
  print('Running read_wave.py as main script')
import sys
import matplotlib.pyplot as plt 
from sound_utils.read_wave import read_wavefile

if __name__ == '__main__':
  if (len(sys.argv) < 2):
    print("Usage: main.py <filename>")
    sys.exit(1)

  wavpath = sys.argv[1]

  file_data = read_wavefile(wavpath)

  sound_data = file_data['sound_data']
  block_align = file_data['block_align'] # 4 bytes
  num_channels = file_data['num_channels']
  bits_per_sample = file_data['bits_per_sample'] # 16 bits = 2 bytes
  sample_rate = file_data['sample_rate']

  sample_timestamps = []
  channel_data = [ [] for _ in range(num_channels)]

  sample_length = 1 / sample_rate
  for i in range(0, len(sound_data), block_align):
    sample_timestamps.append(i // block_align * sample_length)

    for channel in range(0, num_channels):
      sample = sound_data[i + channel * bits_per_sample // 8: i + (channel + 1) * bits_per_sample // 8]

      channel_data[channel].append(int.from_bytes(sample, byteorder='little', signed=True))

  print(sample_timestamps[-1])

  plt.style.use('fivethirtyeight')

  plt.title(f"{wavpath}, {sample_rate / 1000} kHz, {num_channels}-channel {'Mono' if num_channels == 1 else 'Stereo'}")

  plt.plot(sample_timestamps, channel_data[0], label='Channel 1')
  plt.plot(sample_timestamps, channel_data[1], label='Channel 2')

  plt.show()
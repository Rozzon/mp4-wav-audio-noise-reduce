#!/usr/bin/env python3

from pydub import AudioSegment
import noisereduce as nr
from scipy.io import wavfile
import numpy as np
from moviepy.editor import VideoFileClip

def extract_audio(input_video_path, output_audio_path):
    # Load the video clip
    video_clip = VideoFileClip(input_video_path)

    # Extract audio from the video
    audio_clip = video_clip.audio

    # Write the audio to a WAV file
    audio_clip.write_audiofile(output_audio_path, codec='pcm_s16le', bitrate='192k', ffmpeg_params=["-ac", "2"])

def compress_wav_to_flac(input_wav, output_flac):
    # Load the WAV file
    audio = AudioSegment.from_wav(input_wav)

    # Export as FLAC with compression level (0 to 8, 8 being the highest compression)
    audio.export(output_flac, format="flac", parameters=["-compression_level", "0"])

def reduce_noise(y, sr):
    # Perform noise reduction
    reduced_noise = nr.reduce_noise(y=y, sr=sr)
    return reduced_noise

if __name__ == "__main__":
    input_video_path = "../src/0c069c927bc721fb5d102a839fef97e4.mp4"  # Replace with the path to your input MP4 file
    output_audio_path = "../output/extracted_audio.wav"
    compressed_flac = "../output/compressed_output.flac"
    final_output_wav = "../output/final_output.wav"  # Replace with the desired final output path

    # Step 1: Extract audio from the MP4 file
    extract_audio(input_video_path, output_audio_path)

    # Step 2: Compress the extracted WAV file to FLAC
    compress_wav_to_flac(output_audio_path, compressed_flac)

    # Step 3: Load the compressed FLAC file
    audio_flac = AudioSegment.from_file(compressed_flac, format="flac")

    # Step 4: Convert FLAC to WAV (pydub only supports certain operations on FLAC)
    audio_wav = audio_flac.set_frame_rate(44100).set_sample_width(2).set_channels(1)

    # Step 5: Export the WAV file
    audio_wav.export(final_output_wav, format="wav")

    # Step 6: Load the reduced audio for further noise reduction
    rate, data = wavfile.read(final_output_wav)

    # Step 7: Perform noise reduction
    reduced_audio = reduce_noise(y=data, sr=rate)

    # Step 8: Write the result to a WAV file
    final_output_wav_after_noise_reduction = "../reduced_noise_output/final_output_after_noise_reduction.wav"
    wavfile.write(final_output_wav_after_noise_reduction, rate, reduced_audio)

    print("Audio extraction, compression, and noise reduction complete.")

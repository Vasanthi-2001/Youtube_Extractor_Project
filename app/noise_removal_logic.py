# import os
# import uuid
# import torch
# from df.enhance import enhance, init_df
# from df.io import load_audio, save_audio
# from pydub import AudioSegment

# OUTPUT_DIR = "app/outputs"
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # -------------------------------
# # Initialize DeepFilterNet ONCE
# # -------------------------------
# model, df_state, _ = init_df()

# device = "cuda" if torch.cuda.is_available() else "cpu"
# model.to(device)
# model.eval()

# # -------------------------------
# # Noise reduction function
# # -------------------------------
# def apply_noise_reduction(input_path: str, output_format: str = "wav") -> str:
#     try:
#         # Load audio (DF handles resampling)
#         audio, meta = load_audio(
#             input_path,
#             sr=df_state.sr()
#         )

#         # Stereo → Mono
#         if audio.shape[0] > 1:
#             audio = audio.mean(dim=0, keepdim=True)

#         # Ensure float32
#         audio = audio.float()

#         # Normalize input safely
#         max_val = audio.abs().max()
#         if max_val > 0:
#             audio = audio / max_val

#         # Move to device
#         audio = audio.to(device)

#         # Enhance (stronger attenuation)
#         with torch.no_grad():
#             enhanced = enhance(
#                 model=model,
#                 df_state=df_state,
#                 audio=audio,
#                 atten_lim_db=30
#             )

#         # Safe post-normalization
#         max_enh = enhanced.abs().max()
#         if max_enh > 0:
#             enhanced = enhanced / max_enh

#         # Always save as WAV first
#         temp_name = f"nr_{uuid.uuid4().hex}.wav"
#         temp_path = os.path.join(OUTPUT_DIR, temp_name)

#         save_audio(temp_path, enhanced.cpu(), int(df_state.sr()))

#         # Convert to MP3 if requested
#         if output_format.lower() == "mp3":
#             final_name = temp_name.replace(".wav", ".mp3")
#             final_path = os.path.join(OUTPUT_DIR, final_name)

#             audio_seg = AudioSegment.from_wav(temp_path)
#             audio_seg.export(final_path, format="mp3", codec="libmp3lame")

#             os.remove(temp_path)

#             return final_name

#         return temp_name

#     except Exception as e:
#         raise RuntimeError(f"Noise reduction failed: {str(e)}")














































# import os
# import uuid
# import torch
# import torchaudio
# import soundfile as sf
# from df.enhance import enhance, init_df
# from pydub import AudioSegment

# # ---------------- PATH ----------------
# OUTPUT_DIR = "app/outputs"
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # -------------------------------
# # Initialize DeepFilterNet ONLY ONCE
# # -------------------------------
# model, df_state, _ = init_df()

# device = "cuda" if torch.cuda.is_available() else "cpu"
# model.to(device)
# model.eval()


# # -------------------------------
# # Helper: Noise Gate
# # -------------------------------
# def apply_noise_gate(audio: torch.Tensor, threshold: float = 0.02):
#     gated = audio.clone()
#     gated[gated.abs() < threshold] = 0
#     return gated


# # -------------------------------
# # Helper: High-pass filter
# # -------------------------------
# def apply_highpass(audio: torch.Tensor, sr: int):
#     return torchaudio.functional.highpass_biquad(
#         audio,
#         sample_rate=sr,
#         cutoff_freq=80
#     )


# # -------------------------------
# # MAIN NOISE REDUCTION FUNCTION
# # -------------------------------
# def apply_noise_reduction(
#     input_path: str,
#     output_format: str = "wav",
#     second_pass: bool = True
# ) -> str:

#     try:
#         # ---------------- LOAD AUDIO (Stable Version) ----------------
#         audio, sr = torchaudio.load(input_path)

#         # Resample if needed
#         target_sr = df_state.sr()
#         if sr != target_sr:
#             audio = torchaudio.functional.resample(audio, sr, target_sr)

#         # Stereo → Mono
#         if audio.shape[0] > 1:
#             audio = audio.mean(dim=0, keepdim=True)

#         audio = audio.float().to(device)

#         # ---------------- SMART NORMALIZATION ----------------
#         rms = torch.sqrt(torch.mean(audio ** 2))
#         if rms > 1e-6:
#             audio = audio / (rms * 3)

#         # ---------------- PASS 1 (Strong Denoise) ----------------
#         with torch.no_grad():
#             enhanced = enhance(
#                 model=model,
#                 df_state=df_state,
#                 audio=audio,
#                 atten_lim_db=50
#             )

#         # ---------------- PASS 2 (Refinement) ----------------
#         if second_pass:
#             with torch.no_grad():
#                 enhanced = enhance(
#                     model=model,
#                     df_state=df_state,
#                     audio=enhanced,
#                     atten_lim_db=15
#                 )

#         # ---------------- Move to CPU SAFELY ----------------
#         enhanced = enhanced.detach().cpu().contiguous()

#         # ---------------- HIGH-PASS FILTER ----------------
#         enhanced = apply_highpass(enhanced, target_sr)

#         # ---------------- NOISE GATE ----------------
#         enhanced = apply_noise_gate(enhanced, threshold=0.02)

#         # ---------------- SAFE NORMALIZATION ----------------
#         peak = enhanced.abs().max()
#         if peak > 1e-6:
#             enhanced = enhanced * (0.9 / peak)

#         # ---------------- SAVE TEMP WAV (Safe Write) ----------------
#         temp_name = f"nr_{uuid.uuid4().hex}.wav"
#         temp_path = os.path.join(OUTPUT_DIR, temp_name)

#         sf.write(
#             temp_path,
#             enhanced.squeeze().numpy(),
#             target_sr
#         )

#         # ---------------- MP3 CONVERSION ----------------
#         if output_format.lower() == "mp3":

#             final_name = temp_name.replace(".wav", ".mp3")
#             final_path = os.path.join(OUTPUT_DIR, final_name)

#             audio_seg = AudioSegment.from_wav(temp_path)

#             audio_seg = audio_seg.compress_dynamic_range(
#                 threshold=-24.0,
#                 ratio=4.0,
#                 attack=5,
#                 release=60
#             )

#             audio_seg.export(
#                 final_path,
#                 format="mp3",
#                 bitrate="192k"
#             )

#             os.remove(temp_path)
#             return final_name

#         return temp_name

#     except Exception as e:
#         raise RuntimeError(f"Noise reduction failed: {str(e)}")






















































# cpu version code


# import os
# import uuid
# import torch
# import torchaudio
# from df.enhance import enhance, init_df
# from df.io import load_audio, save_audio
# from pydub import AudioSegment

# # ---------------- PATH ----------------
# OUTPUT_DIR = "app/outputs"
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # -------------------------------
# # Initialize DeepFilterNet ONLY ONCE
# # -------------------------------
# model, df_state, _ = init_df()

# device = "cuda" if torch.cuda.is_available() else "cpu"
# model.to(device)
# model.eval()


# # -------------------------------
# # Helper: Noise Gate
# # -------------------------------
# def apply_noise_gate(audio: torch.Tensor, threshold: float = 0.02):
#     """
#     Removes very low-level background noise between speech.
#     """
#     gated = audio.clone()
#     gated[gated.abs() < threshold] = 0
#     return gated


# # -------------------------------
# # Helper: High-pass filter
# # -------------------------------
# def apply_highpass(audio: torch.Tensor, sr: int):
#     """
#     Removes low-frequency hum and mic rumble.
#     """
#     return torchaudio.functional.highpass_biquad(
#         audio.cpu(),
#         sample_rate=sr,
#         cutoff_freq=80
#     )


# # -------------------------------
# # MAIN NOISE REDUCTION FUNCTION
# # -------------------------------
# def apply_noise_reduction(
#     input_path: str,
#     output_format: str = "wav",
#     second_pass: bool = True
# ) -> str:
#     """
#     Advanced noise reduction using DeepFilterNet + audio cleanup pipeline.
#     """

#     try:
#         # ---------------- LOAD AUDIO ----------------
#         audio, meta = load_audio(input_path, sr=df_state.sr())

#         # Stereo → Mono
#         if audio.shape[0] > 1:
#             audio = audio.mean(dim=0, keepdim=True)

#         audio = audio.float().to(device)

#         # ---------------- SMART NORMALIZATION ----------------
#         rms = torch.sqrt(torch.mean(audio ** 2))
#         if rms > 1e-6:
#             audio = audio / (rms * 3)

#         # ---------------- PASS 1 (Strong Denoise) ----------------
#         with torch.no_grad():
#             enhanced = enhance(
#                 model=model,
#                 df_state=df_state,
#                 audio=audio,
#                 atten_lim_db=50   # stronger suppression
#             )

#         # ---------------- PASS 2 (Refinement) ----------------
#         if second_pass:
#             with torch.no_grad():
#                 enhanced = enhance(
#                     model=model,
#                     df_state=df_state,
#                     audio=enhanced,
#                     atten_lim_db=15
#                 )

#         # Move back to CPU for post-processing
#         enhanced = enhanced.cpu()

#         # ---------------- HIGH-PASS FILTER ----------------
#         enhanced = apply_highpass(enhanced, int(df_state.sr()))

#         # ---------------- NOISE GATE ----------------
#         enhanced = apply_noise_gate(enhanced, threshold=0.02)

#         # ---------------- SAFE NORMALIZATION ----------------
#         peak = enhanced.abs().max()
#         if peak > 1e-6:
#             enhanced = enhanced * (0.9 / peak)

#         # ---------------- SAVE TEMP WAV ----------------
#         temp_name = f"nr_{uuid.uuid4().hex}.wav"
#         temp_path = os.path.join(OUTPUT_DIR, temp_name)

#         save_audio(temp_path, enhanced, int(df_state.sr()))

#         # ---------------- MP3 CONVERSION ----------------
#         if output_format.lower() == "mp3":

#             final_name = temp_name.replace(".wav", ".mp3")
#             final_path = os.path.join(OUTPUT_DIR, final_name)

#             audio_seg = AudioSegment.from_wav(temp_path)

#             # Speech-focused dynamic compression
#             audio_seg = audio_seg.compress_dynamic_range(
#                 threshold=-24.0,
#                 ratio=4.0,
#                 attack=5,
#                 release=60
#             )

#             audio_seg.export(
#                 final_path,
#                 format="mp3",
#                 bitrate="192k"
#             )

#             os.remove(temp_path)
#             return final_name

#         return temp_name

#     except Exception as e:
#         raise RuntimeError(f"Noise reduction failed: {str(e)}")





















# gpu version code

import os
import uuid
import torch
import torchaudio
import soundfile as sf
from df.enhance import enhance, init_df
from pydub import AudioSegment

# ---------------- FORCE CPU COMPLETELY ----------------
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
torch.cuda.is_available = lambda: False  # 🔥 hard disable CUDA

device = torch.device("cpu")
print("Running strictly in CPU mode")

# ---------------- PATH ----------------
OUTPUT_DIR = "app/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- Initialize DeepFilterNet ON CPU ----------------
model, df_state, _ = init_df()

model.to(device)
model.eval()

print("Model loaded successfully (CPU only)")


# ---------------- Noise Gate ----------------
def apply_noise_gate(audio: torch.Tensor, threshold: float = 0.02):
    gated = audio.clone()
    gated[gated.abs() < threshold] = 0
    return gated


# ---------------- High-pass filter ----------------
def apply_highpass(audio: torch.Tensor, sr: int):
    return torchaudio.functional.highpass_biquad(
        audio,
        sample_rate=sr,
        cutoff_freq=80
    )


# ---------------- MAIN FUNCTION ----------------
def apply_noise_reduction(
    input_path: str,
    output_format: str = "wav",
    second_pass: bool = True
) -> str:

    try:
        # Load audio
        audio, sr = torchaudio.load(input_path)
        target_sr = df_state.sr()

        if sr != target_sr:
            audio = torchaudio.functional.resample(audio, sr, target_sr)

        if audio.shape[0] > 1:
            audio = audio.mean(dim=0, keepdim=True)

        audio = audio.float().to(device)

        # Normalize
        rms = torch.sqrt(torch.mean(audio ** 2))
        if rms > 1e-6:
            audio = audio / (rms * 3)

        # Pass 1
        with torch.no_grad():
            enhanced = enhance(
                model=model,
                df_state=df_state,
                audio=audio,
                atten_lim_db=50
            )

        # Pass 2
        if second_pass:
            with torch.no_grad():
                enhanced = enhance(
                    model=model,
                    df_state=df_state,
                    audio=enhanced,
                    atten_lim_db=15
                )

        # 🔥 FORCE CPU BEFORE ANYTHING ELSE
        enhanced = enhanced.detach().to("cpu")

        # Filters (CPU)
        enhanced = apply_highpass(enhanced, target_sr)
        enhanced = apply_noise_gate(enhanced, threshold=0.02)

        # Normalize safely
        peak = enhanced.abs().max()
        if peak > 1e-6:
            enhanced = enhanced * (0.9 / peak)

        # FINAL CPU GUARANTEE
        enhanced_np = enhanced.squeeze().detach().cpu().numpy()

        # Save WAV
        temp_name = f"nr_{uuid.uuid4().hex}.wav"
        temp_path = os.path.join(OUTPUT_DIR, temp_name)

        sf.write(temp_path, enhanced_np, target_sr)

        # Optional MP3
        if output_format.lower() == "mp3":
            final_name = temp_name.replace(".wav", ".mp3")
            final_path = os.path.join(OUTPUT_DIR, final_name)

            audio_seg = AudioSegment.from_wav(temp_path)

            audio_seg = audio_seg.compress_dynamic_range(
                threshold=-24.0,
                ratio=4.0,
                attack=5,
                release=60
            )

            audio_seg.export(
                final_path,
                format="mp3",
                bitrate="192k"
            )

            os.remove(temp_path)
            return final_name

        return temp_name

    except Exception as e:
        raise RuntimeError(f"Noise reduction failed: {str(e)}")
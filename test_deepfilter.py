from df.enhance import enhance, init_df
from df.io import load_audio, save_audio
import torch

# -------------------------------
# Init model
# -------------------------------
model, df_state, _ = init_df()  # no device argument

# Move model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# -------------------------------
# Load audio (DF handles resample)
# -------------------------------
audio, meta = load_audio(
    r"C:\Users\Admin\Downloads\TE_M_DIALOGUES\Dookudu_MB.mp3",
    sr=df_state.sr()
)

# Convert stereo → mono
if audio.shape[0] > 1:
    audio = audio.mean(dim=0, keepdim=True)

# Ensure float32 tensor
audio = audio.float()

# Move audio to same device as model
audio = audio.to(device)

# Normalize audio
audio = audio / audio.abs().max()

print("Audio shape:", audio.shape)
print("Model SR:", df_state.sr())
print("Device:", device)

# -------------------------------
# Enhance
# -------------------------------
enhanced = enhance(
    model=model,
    df_state=df_state,
    audio=audio
)

# -------------------------------
# Post-normalize
# -------------------------------
enhanced = enhanced / enhanced.abs().max()

# -------------------------------
# Save output
# -------------------------------
save_audio(
    "enhanced1.wav",
    enhanced.cpu(),  # move back to CPU for saving
    int(df_state.sr())
)

print("✅ Clean audio saved successfully")

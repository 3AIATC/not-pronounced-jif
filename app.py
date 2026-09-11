import streamlit as st
import subprocess
import tempfile
import os
import zipfile
from pygifsicle import gifsicle

st.title("Batch Video to Optimised GIF Converter")

# 1. Enable multiple file uploads
uploaded_files = st.file_uploader("Upload MP4 videos", type=["mp4"], accept_multiple_files=True)
crop_square = st.checkbox("Crop GIFs to a 1:1 square", value=False)

if uploaded_files:
    if st.button("Convert Videos"):
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "optimised_gifs.zip")

            # Setup progress tracking
            progress_bar = st.progress(0)
            total_files = len(uploaded_files)

            # 2. Open a zip file to store all outputs
            with zipfile.ZipFile(zip_path, "w") as zipf:

                # Loop through each uploaded file
                for i, uploaded_file in enumerate(uploaded_files):
                    base_name = os.path.splitext(uploaded_file.name)[0]

                    mp4_path = os.path.join(temp_dir, f"{base_name}.mp4")
                    palette_path = os.path.join(temp_dir, f"{base_name}_palette.png")
                    gif_path = os.path.join(temp_dir, f"{base_name}.gif")
                    opt_gif_path = os.path.join(temp_dir, f"{base_name}_opt.gif")

                    with open(mp4_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    with st.spinner(f"Processing {uploaded_file.name}..."):
                        try:
                            # Configure FFmpeg filters
                            if crop_square:
                                video_filter = "fps=25,crop='min(iw,ih)':'min(iw,ih)',scale=854:854:flags=lanczos"
                            else:
                                video_filter = "fps=25,scale=854:-1:flags=lanczos"

                            # Generate palette
                            ffmpeg_options = ["-vf", f"{video_filter},palettegen", "-y"]
                            subprocess.run(["ffmpeg", "-i", mp4_path] + ffmpeg_options + [palette_path], check=True,
                                           capture_output=True)

                            # Convert to GIF
                            ffmpeg_paletteuse = [
                                "-filter_complex",
                                f"{video_filter}[x];[x][1:v]paletteuse=dither=floyd_steinberg",
                                "-y"
                            ]
                            subprocess.run(
                                ["ffmpeg", "-i", mp4_path, "-i", palette_path] + ffmpeg_paletteuse + [gif_path],
                                check=True, capture_output=True)

                            # Optimise GIF
                            gifsicle_options = ["--optimize=3", "--dither=floyd", "--lossy=20", "--careful"]
                            gifsicle(
                                sources=gif_path,
                                destination=opt_gif_path,
                                optimize=False,
                                colors=256,
                                options=gifsicle_options
                            )

                            # Add the finalised GIF to the zip archive
                            zipf.write(opt_gif_path, arcname=f"{base_name}.gif")

                        except subprocess.CalledProcessError as e:
                            st.error(f"FFmpeg error on {uploaded_file.name}: {e.stderr.decode('utf-8')}")
                        except Exception as e:
                            st.error(f"An error occurred on {uploaded_file.name}: {str(e)}")

                    # Update the progress bar after each file finishes
                    progress_bar.progress((i + 1) / total_files)

            st.success("Batch conversion complete.")

            # 3. Provide the single zip download
            with open(zip_path, "rb") as file:
                st.download_button(
                    label="Download All Optimised GIFs (ZIP)",
                    data=file,
                    file_name="optimised_gifs.zip",
                    mime="application/zip"
                )
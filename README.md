# not-pronounced-jif: Batch Video to Optimised GIF Converter

A Streamlit web application that converts MP4 videos into high quality, highly optimised GIFs. It processes multiple files simultaneously and bundles the output into a single ZIP archive for easy downloading.

Remember folks: GIF is pronounced with a hard G (unless you pronounce "graphical" as "jraphical", in which case, carry-on, I don't make the rules).

## Features
* **Batch processing:** Upload and convert multiple MP4 files at once.
* **High-quality conversion:** Uses FFmpeg to generate custom colour palettes for each video before conversion.
* **File size optimisation:** Integrates Gifsicle to reduce output file sizes using lossy compression and dithering.
* **Aspect ratio control:** Includes an option to crop videos to a 1:1 square.
* **Cloud-ready:** Pre-configured with `requirements.txt` and `packages.txt` for deployment on Streamlit Community Cloud.


## Local Installation
To run this application locally, you must have FFmpeg and Gifsicle installed on your system. 

1. Clone the repository:
   ```bash
   git clone [https://github.com/3AIATC/not-pronounced-jif.git](https://github.com/3AIATC/not-pronounced-jif.git)
   cd not-pronounced-jif

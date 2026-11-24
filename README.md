# Document Scanner CLI

A local Python tool that finds a document in a photograph, corrects its perspective and saves a PNG scan. Built as a learning project following Adrian Rosebrock's PyImageSearch document-scanner tutorial, then extended for everyday command-line use.

## Features

- Canny edge detection and contour approximation to locate four document corners.
- Perspective correction at the original image resolution.
- Black-and-white, grayscale and colour output.
- Bare filenames resolved in the standard user Downloads folder.
- Numbered output names to preserve earlier scans.
- Windows launcher using the project's virtual environment.
- Optional preview window; processing stays on your computer.

## Setup on Windows (Command Prompt)

Python 3.13 was used during development. Extract this project to a permanent folder, open Command Prompt there, then run:

```bat
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

The dependencies are not fully version-pinned. For a record of your working environment, run `python -m pip freeze > requirements-lock.txt` inside your activated environment.

## Usage

```bat
python scan.py receipt.jpg
python scan.py "hotel receipt.jpg" --mode gray
python scan.py "C:\Users\hassa\Pictures\document.jpg" --mode color
python scan.py "images\document.jpg" --no-preview
python scan.py --help
```
scan "hotel receipt.jpg" --mode color

A filename alone is looked up in `Path.home() / "Downloads"`. A relative path containing a directory is resolved from your current terminal folder. A full path is used directly. If Downloads has been relocated, use its full path.

The output is saved beside the input: `receipt_scanned.png`, then `receipt_scanned_1.png`, and so on. Close the preview by selecting its window and pressing a key. `--no-preview` saves without opening a window.

### Short Windows command

Add the extracted project folder to your **user Path** through "Edit environment variables for your account". Open a new Command Prompt, then run:

```bat
scan receipt.jpg
scan receipt.jpg --mode color
```

`scan.cmd` runs `.venv\Scripts\python.exe` relative to its own location, so manual environment activation is unnecessary. Keep the launcher beside `scan.py` and `.venv`.

## Files

| File/folder | Purpose |
| --- | --- |
| `scan.py` | Argument handling, detection, output modes and saving |
| `transformation.py` | Corner ordering and perspective transformation |
| `scan.cmd` | Windows command launcher |
| `requirements.txt` | Direct Python dependencies |
| `images/` | Local test photographs, ignored by Git |
| `.gitignore` | Excludes environments, caches and local test files |

Outputs now go beside the source image; the old `output/` folder is optional and can stay on your PC.

## Pipeline

1. Resize a detection copy to height 400.
2. Convert it to grayscale, blur it and detect edges.
3. Check the five largest contours for a four-point approximation.
4. Scale detected corners to original-image coordinates.
5. Warp the photograph into a rectangle.
6. Keep colour, convert to grayscale, or apply local thresholding.
7. Save the PNG and optionally show a preview.

## What was added beyond the tutorial

Downloads lookup, positional command-line input, three output modes, collision-safe names for sequential runs, a Windows launcher and clearer failures. The packaged review also corrects swapped colour/grayscale branches, restores preview waiting, and adds `--no-preview`.

## Limitations

This uses a simple contour heuristic: the first four-point shape among the five largest contours can be the wrong object. Low-contrast backgrounds, missing corners, clutter, heavy shadows and strong rotation can cause failures. The sum/difference corner-ordering method can be ambiguous for some rotations. Perspective correction does not flatten wrinkles. Black-and-white mode loses photographic detail and can emphasise crease shadows. PDF input, OCR and manual corner selection are not implemented. Output names are intended for sequential use, not simultaneous processes.

## Verification and portfolio examples

The author manually demonstrated scanning a tutorial receipt and a photographed letter. This reviewed package has additional local checks recorded in REVIEW.md; these do not establish accuracy across arbitrary documents.

For a public demo, use your own non-sensitive sample document. Include the original photograph, scanned result and mode used. Do not commit personal letters, registration numbers or QR codes. Tutorial assets are not redistributed in this package because their reuse terms have not been established.

## Tutorial credit

Adrian Rosebrock, "How to Build a Kick-Ass Mobile Document Scanner in Just 5 Minutes", PyImageSearch (1 September 2014):
https://pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/

The detection and four-point transformation approach follows that tutorial. This is presented as a tutorial-based project with practical extensions, not an original computer-vision algorithm. No licence for third-party tutorial code or assets is granted by this README.

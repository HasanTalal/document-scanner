# Review notes

## Changes from the uploaded code

- Corrected `--mode gray` returning colour and `--mode color` returning grayscale. This explains why the previous grayscale demonstration still had red borders.
- Restored `waitKey(0)` and window cleanup after the preview; both were commented out.
- Added `--no-preview` for command-only runs and automated checks.
- Changed the path check from `exists()` to `is_file()` to reject directories.
- Report an unreadable image through argparse rather than a misleading FileNotFoundError traceback.
- Exit with a failure status if no four-corner outline is found.
- Calculate local thresholds only for black-and-white mode.
- Reject a degenerate transform smaller than two pixels on either side.
- Removed obsolete commented code; kept the sequential tutorial structure and familiar variable names.
- Added setup instructions, direct dependencies and a Git ignore file.

## Checks completed

Python compilation passed. A generated coloured document on a dark background was processed through all three modes without preview. Colour information was retained in colour mode, grayscale contained intermediate shades, and black-and-white output contained only 0 and 255. Three sequential runs produced distinct filenames. Missing-file, directory-input and blank-image cases exited unsuccessfully without a traceback.

These checks used Linux and headless OpenCV in the review environment. The delivered dependencies use desktop OpenCV for Windows preview support. The Windows launcher and interactive preview were not executed here. Downloads resolution was inspected in code, while the user has already demonstrated it on Windows. No accuracy rate is claimed and these checks do not replace testing real photographs.

## Installing this reviewed copy

Keep your existing `.venv` and local photographs. Copy `scan.py`, `transformation.py`, `scan.cmd`, `README.md`, `requirements.txt`, `.gitignore` and this review into your existing project folder. The images folder in the ZIP is empty apart from a placeholder: do not delete your own images. There is no need to move your project or change PATH.

Try:

```bat
scan document.jpg --mode color
scan document.jpg --mode gray
scan document.jpg --no-preview
```

Use an actual filename in Downloads. For the tutorial image within the project, run `python scan.py "images\document.jpg"` from the project folder with the environment activated. Colour should retain colours, grayscale should not, and the default preview should remain until a key is pressed in its window.

## Before publishing

Use an original sample document without personal information for portfolio screenshots. The supplied tutorial photograph and old generated output were omitted from this distribution. Credit the tutorial and distinguish practical extensions from the original algorithm. No public repository or website has been published by this review.

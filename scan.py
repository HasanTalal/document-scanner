from pathlib import Path

import cv2
import imutils
from transformation import four_point_transform

from skimage.filters import threshold_local

import argparse

parser = argparse.ArgumentParser(
    description="Straighten a document photograph and save as a scan.  "
)

parser.add_argument(
    "image",
    help="Specify the name of the file in the downloads folder, OR a full path to the image file if not in dowloads folder."
)

parser.add_argument(
    "--mode",
    choices=["bw", "gray", "color"],
    default="bw",
    help = "Output style for the scanned image.  bw = black and white, gray = grayscale, color = color.  Default is bw."
)

parser.add_argument(
    "--no-preview", action="store_true",
    help="Save the scan without opening an image window"
)
args = parser.parse_args()

image_path = Path(args.image).expanduser()

if not image_path.is_absolute() and image_path.parent == Path("."):
    image_path = Path.home() / "Downloads" / image_path

image_path = image_path.resolve()
if not image_path.is_file():
    parser.error(f"Image file does not exist: {image_path} ")

image = cv2.imread(str(image_path))

if image is None:
    parser.error(f"Could not decode image: {image_path}. Use a supported photograph such as JPG or PNG; PDF input is not supported.")

preview = imutils.resize(image, height=400)

gray = cv2.cvtColor(preview, cv2.COLOR_BGR2GRAY)

blurred = cv2.GaussianBlur(gray, (5,5), 0)

edges = cv2.Canny(blurred, 75, 200)

contours, _ = cv2.findContours(
    edges,
    cv2.RETR_LIST,
    cv2.CHAIN_APPROX_SIMPLE
)

contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

document_corners = None

for contour in contours:
    perimeter = cv2.arcLength(contour, True)

    approximation = cv2.approxPolyDP(
        contour,
        0.02 * perimeter,
        True
    )

    if len(approximation) == 4:
        document_corners = approximation
        break

if document_corners is not None:
    print("Found a possible document with four corners.")
else:
    parser.exit(1, "Could not find a four-corner document outline. Try a contrasting background with all four corners visible.\n")

straightened = None

if document_corners is not None:
    scale_x = image.shape[1] / preview.shape[1]
    scale_y = image.shape[0] / preview.shape[0]

    original_corners = document_corners.reshape(4, 2).astype("float32")
    original_corners[:, 0] *= scale_x
    original_corners[:, 1] *= scale_y

    straightened = four_point_transform(image, original_corners)

    scan_grey = cv2.cvtColor(straightened, cv2.COLOR_BGR2GRAY)

    if args.mode == "color":
        scanned = straightened
    elif args.mode == "gray":
        scanned = scan_grey
    else:
        thresholds = threshold_local(
            scan_grey, block_size=35, method="gaussian", offset=10
        )
        scanned = (scan_grey > thresholds).astype("uint8") * 255

    output_path = image_path.with_name(
        f"{image_path.stem}_scanned.png"
    )
    num = 1
    while output_path.exists():
        output_path = image_path.with_name(
            f"{image_path.stem}_scanned_{num}.png"
        )
        num += 1

    if not cv2.imwrite(str(output_path), scanned):
        raise OSError(f"Couldnt save the scan to : {output_path}")

    print(f"scan saved to: {output_path}")

    if not args.no_preview:
        cv2.imshow("Final scan", imutils.resize(scanned, height=600))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

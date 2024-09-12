# cropC3D
A script to crop C3D files to a specified time period using the `ezc3d` library.

## Features
- Crops markers and analog data to a specified time period.
- Updates the C3D file parameters and headers accordingly.
- Saves the cropped C3D file with a new name suffixed with `_cropped`.

## Requirements
Ensure you have **ezc3d** and **numpy** installed.

## Usage
Call the script with the path to the C3D file, start time, and end time as command-line arguments:

```bash
python cropC3D.py path/to/your/file.c3d start_time end_time
```

For example, on Windows:

```bash
python cropC3D.py C:\\path\\to\\your\\file.c3d 5.1 6.2
```

Alternatively, you can run the script from MATLAB using:

```matlab
pyrunfile("cropC3D.py 'path/to/your/file.c3d' start_time end_time")
```

This will generate a new C3D file named `file_cropped.c3d` with the specified changes.

## Example
To crop a C3D file from 5.1 seconds to 6.2 seconds:

```bash
python cropC3D.py C:\\path\\to\\your\\file.c3d 5.1 6.2
```

## Notes
- The script removes meta points and updates the trial start and end fields.
- If the number of labels in `POINT.LABELS` is less than 255, `POINT.LABELS2` is removed.

## Related Posts
- ezc3d Issue #321
- ezc3d Issue #221

## Author
Created by Harald Penasso on Thu Sep 12 23:33:53 2024.

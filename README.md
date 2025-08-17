# ASCII Video Generator

A Python tool that converts regular videos into ASCII art videos with customizable styling options.

## Requirements

```bash
pip install opencv-python numpy
```

## Usage

### Basic Usage
```python
from ascii_video import ascii_video

ascii_video('input.mp4', 'output.mp4')
```

### Advanced Configuration
```python
ascii_video(
    'input.mp4', 
    'output.mp4',
    ascii_resolution=80,
    char_width=12,
    char_height=24,
    invert_ascii=True,
    colored=True,
    ascii_char_set=";:. "    # custom ordered char string 
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ascii_resolution` | int | 64 | Grid size (e.g., 64 = 64x64 cells) |
| `char_width` | int | 10 | Character width in output pixels |
| `char_height` | int | 20 | Character height in output pixels |
| `invert_ascii` | bool | False | Invert brightness-to-character mapping |
| `colored` | bool | False | Use original video colors vs white on black |
| `ascii_char_set` | str | "short" | Character set to use |

## Character Sets

Use pre-defined character sets (`"short"`, `"long"`, `"dot"`, `"hash"`) or pass a custom string of characters ordered from darkest to lightest (e.g., `";:. "`)

---

*Converts any video into retro ASCII art while preserving motion and optionally color information.*
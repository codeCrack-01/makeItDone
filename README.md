# MakeItDone API

A high-performance, stateless REST API built with FastAPI for seamless image manipulation and PDF conversion.

## 🚀 Features

- **Format Conversion**: Switch between PNG and JPG effortlessly.
- **Compression**: Smart compression to target specific file sizes (e.g., 200KB).
- **Transparency Management**: Remove alpha channels/transparency from images.
- **PDF Tools**: Convert a batch of images into a single PDF or extract images from PDF pages.
- **CI/CD Integrated**: Automated testing suite with GitHub Actions.

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Image Processing**: Pillow (PIL)
- **PDF Conversion**: pdf2image (requires Poppler)
- **Testing**: Pytest & Pytest-asyncio

## 📋 Prerequisites

Before running the API, ensure you have Poppler installed on your system, as it is required for PDF-to-image conversion.

### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install -y poppler-utils
```

### macOS

```bash
brew install poppler
```

## ⚙️ Installation & Setup

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/MakeItDone.git
cd MakeItDone/backend
```

2. **Create a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
pip install pytest pytest-asyncio
```

4. **Run the server:**

```bash
uvicorn main:app --reload
```
OR for development:
```bash
fastapi run dev
```

The API will be available at `http://127.0.0.1:8000`.

## 📖 API Documentation

Once the server is running, you can access the interactive Swagger UI at:

```
http://127.0.0.1:8000/docs
```

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/images/png_to_jpg` | Convert PNG images to JPG format. |
| POST | `/api/images/jpg_to_png` | Convert JPG images to PNG format. |
| POST | `/api/images/compress_to_200kb` | Compress image to stay under 200KB. |
| POST | `/api/images/remove_transparency` | Remove transparency from PNG files. |
| POST | `/api/pdf/images_to_pdf` | Combine multiple images into one PDF. |
| POST | `/api/pdf/pdf_to_images` | Extract pages from a PDF as images. |

## 🧪 Testing

The project uses pytest for automated testing. To run the tests locally:

```bash
cd backend
export PYTHONPATH=$PYTHONPATH:.
pytest
```

## 🤖 CI/CD

This repository includes a GitHub Action workflow (Python Tests) that automatically:

1. Installs system-level dependencies (`poppler-utils`).
2. Sets up Python 3.12.
3. Installs project requirements.
4. Executes the test suite on every push or pull request to the `main` branch.

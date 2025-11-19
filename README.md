# Tổng quan
Đây là project đồ án môn Machine Learning, thực hiện nhận diện biển số xe từ hình ảnh và video trực tiếp từ camera.

# Thành viên nhóm

- Châu Trung Tín - 2410060248
- Phạm Thiên Chương - 2410060300
- Nguyễn Ngọc Duy - 2410060217
- Phan Hữu Thiện - 2410060241

# Mục tiêu Project
Mục tiêu của project là nhận diện được ký tự trên biển số xe trong các điều kiện khác nhau như góc chụp, ánh sáng, chất lượng hình ảnh/video. Do đó, project sẽ bao gồm các tính năng chính sau:
- Nhận diện vị trí biển số xe trong hình ảnh/video.
- Trích xuất và nhận diện ký tự trên biển số xe.

# Technologies
Dự án được xây dựng dựa trên một tech stack hiện đại và mạnh mẽ, bao gồm:
- **Ngôn ngữ lập trình:** Python
- **Backend Framework:** FastAPI
- **Frontend:** HTML, CSS, JavaScript
- **Model phát hiện (Detection):** YOLOv11
- **Model nhận dạng (Recognition):** EasyOCR (dùng pre-trained, chưa fine-tune)
- **Thư viện xử lý ảnh:** OpenCV

# Kiến trúc tổng quan
Dự án được thiết kế theo kiến trúc microservices, bao gồm 2 thành phần chính:
1.  **Backend (FastAPI):**
    *   Cung cấp các API endpoint để xử lý yêu cầu nhận dạng.
    *   Sử dụng YOLOv11 để phát hiện vị trí biển số, OpenCV để xử lý ảnh, và EasyOCR để nhận dạng ký tự.
2.  **Frontend (HTML, CSS, JavaScript):**
    *   Xây dựng giao diện người dùng trên nền tảng web, cho phép người dùng tải ảnh/video lên.
    *   Gửi yêu cầu đến Backend và hiển thị kết quả nhận dạng cho người dùng.

# Training model

Với phạm vi của project, chúng ta cần phải có 2 model riêng biệt:

- **Model detection**: Nhận diện vùng chứa biển số xe (object detection), sử dụng YOLOv11 để phát hiện vị trí biển số xe trong hình ảnh/video. Model này sẽ cho đầu ra là bounding box dùng để xác định vùng biển số xe, được thể hiện qua các tọa độ (x, y, width, height).

- **Model recognition**: Model nhận dạng ký tự (OCR) trong vùng biển số đã được phát hiện. Model này sẽ cho đầu ra là chuỗi ký tự tương ứng với biển số xe (sử dụng model OCR pre-trained).

# Dataset

Để huấn luyện các model, chúng ta cần chuẩn bị các dataset sau:

- **Detection**: Dataset hình ảnh biển số xe để huấn luyện model nhận diện biển số xe. Dataset này bao gồm:
1. Các file hình ảnh các phương tiện có biển số xe, trong ảnh có biển số xe được khoanh vùng rõ ràng và đa dạng các góc chụp, điều kiện ánh sáng, kích thước.
2. Các file nhãn (label) tương ứng với các hình ảnh, trong đó mỗi nhãn bao gồm tọa độ bounding box của biển số xe trong ảnh. 

- **Recognition**: Dataset ký tự trên biển số xe để huấn luyện model OCR. Dataset này bao gồm:
1. Các file hình ảnh chứa biển số xe, trong đó các ký tự trên biển số xe được khoanh vùng rõ ràng.
2. Các file nhãn (label) tương ứng với các hình ảnh, trong đó mỗi nhãn bao gồm chuỗi ký tự tương ứng với biển số xe.

Dataset được chia 2 phần: training set (80%) và validation set (20%) để đánh giá hiệu suất của model trong quá trình huấn luyện.

# Cách sử dụng

## Chạy trên local trực tiếp với Python

### Chuẩn bị môi trường

- [Python 3.11](https://www.python.org/downloads/release/python-3111/)
- [Poetry](https://python-poetry.org/docs/#installation)

### Clone project

```bash
git clone https://github.com/thienph/ML-license_plate_detection_recognition.git
```

### Khởi chạy project

**For Windows:**

```Powershell
cd ML-license_plate_detection_recognition
.\run-project.ps1
```

**For MacOS:**

```bash
cd ML-license_plate_detection_recognition
chmod +x ./scripts/*.sh
.run-project.sh
```

Nếu trang demo không tự động mở, hãy truy cập vào folder `frontend` và chạy file ``index.html`` bằng trình duyệt web.

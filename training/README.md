# Training Component

Thư mục này chứa tất cả các tài nguyên liên quan đến việc huấn luyện và đánh giá các model machine learning cho dự án.

## Dataset
Gồm 2 phần chính:
- [License Plate Detection Dataset](https://drive.google.com/file/d/1xchPXf7a1r466ngow_W_9bittRqQEf_T/view?usp=sharing): Dữ liệu ảnh xe có biển số với nhãn bounding box cho việc huấn luyện model nhận diện biển số xe.

- [Character Detection Dataset](https://drive.google.com/file/d/1bPux9J0e1mz-_Jssx4XX1-wPGamaS8mI/view?usp=sharing): Dữ liệu ảnh chứa các ký tự trên biển số với nhãn cho việc huấn luyện model nhận dạng ký tự.

---

## Training Workflow

Quá trình training được thực hiện trên Google Colab bằng cách sử dụng notebook `license_plate_training.ipynb`.

### 1. Environment Setup
- **Nền tảng:** Google Colab
- **Hardware:** GPU T4

### 2. Chuẩn bị

1.  **Kích hoạt GPU:** Trước khi chạy, hãy đảm bảo bạn đã bật GPU cho Colab Runtime (`Runtime` -> `Change runtime type` -> `Hardware accelerator: GPU` -> `GPU type: T4`).
2.  **Chuẩn bị Dataset:** Đảm bảo 2 file dataset của bạn đã được upload lên Google Drive theo đúng đường dẫn sau:
    - `[Your Google Drive]/MyDrive/projects/license_plate_detection_recognition/training/dataset/LP_detection.zip`
    - `[Your Google Drive]/MyDrive/projects/license_plate_detection_recognition/training/dataset/OCR.zip`

### 3. Thực hiện huấn luyện

- Mở file `training/notebooks/license_plate_training.ipynb` trên Google Colab.
- Chạy lần lượt các cell code từ trên xuống dưới.
- Notebook sẽ tự động thực hiện các công việc:
    - Cài đặt thư viện.
    - Kết nối Google Drive.
    - Sao chép và giải nén dataset.
    - Tạo file cấu hình `data.yaml`.
    - Bắt đầu quá trình huấn luyện model.

### 4. Kết quả

- Các model đã được huấn luyện và log của quá trình training sẽ được lưu vào thư mục `[Your Google Drive]/MyDrive/model_license_plate_runs` trên Google Drive của bạn.

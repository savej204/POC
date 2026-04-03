# Analyst
## Description: Arbitrary file upload in CTFd platform (affected version <= 3.8.1)

- Trang config gồm các chức năng chính là export và import CSV. Điểm vào đầu tiên của chúng ta upload file CSV (định dạng file cho phép .zip).

<img width="1109" height="612" alt="image" src="https://github.com/user-attachments/assets/1af9de5e-4bfb-4cb4-8836-1f71ece1a5e7" />

- Ở file khởi tạo của ```cli folder``` tại dòng 83 gọi func import_ctf nằm trong file utils (ở đây nó để alias là import_ctf_util).
  
  <img width="667" height="87" alt="image" src="https://github.com/user-attachments/assets/a4b92bbe-e876-4085-9bc8-89d8e143a3f5" />
  
- Sau khi nhảy đến func import trong file khởi tạo của utils thì mình nhận thấy rằng hàm này có kiểm tra các filename (nằm bên trong file .zip) nhằm block chuỗi gây Path Traversal nhưng thật sự không an toàn đối với filter như thế này.

<img width="1004" height="475" alt="image" src="https://github.com/user-attachments/assets/8386d5ba-4b3d-4e40-b119-89cf2ecae6c0" />

- Lần theo ```backup``` value ta thấy có một đoạn để extract file hoạt động như sau:

<img width="1045" height="416" alt="image" src="https://github.com/user-attachments/assets/1521d1ff-de6d-4cd1-b35d-92b503d223d5" />

  ```
  1. files value sẽ là 1 array chứa các filename nếu nằm trong uploads folder
  2. Trong loop thì filename = f.split(os.sep, 1)
    -> [uploads/banner.jpg] -> ['uploads','banner.jpg'] -> BYPASS -> [uploads//tmp/pwned] -> filename[1] = /tmp/pwned
      *os.sep hiểu đại loại là nó lấy ký tự đại diện phân cách trong filesystem
  3. Gọi hàm get_uploader trong utils(uploads) sau đó gọi store func để thực hiện tiếp công việc
  ````

<img width="1039" height="406" alt="image" src="https://github.com/user-attachments/assets/d8cbb89c-0e23-4db9-b620-b882ea73d953" />

```
get_uploader func trả về 1 trong 2 giá trị app_config trong UPLOADERS value. FilesystemUploader và S3Uploader là 2 class import từ uploaders func thì mình lấy đại diện class FilesystemUploader để test.
Tại store func chứa 3 tham số trong đó self là lấy đường dẫn filesystem config:
1. fileobj chứa nội dung của file
2. filname là tên file sau khi được tách rời trước đó(filename[1])
```

<img width="936" height="385" alt="image" src="https://github.com/user-attachments/assets/8a7bb1b5-7283-4b00-bc95-4e2449d18785" />

> Cuối cùng thực hiện lưu nội dung vào file (dst) và tại đây ta đã thực hiện thành công việc ghi đè file và có thể tạo luôn được cả file độc hại để lấy shell.

https://github.com/user-attachments/assets/c6c1c685-57ed-4392-b3f7-83f294eab0b1



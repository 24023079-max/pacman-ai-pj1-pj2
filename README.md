# pacman-ai-pj1-pj2
Pacman AI – A team project combining CS188 Project 1 (Search Algorithms: DFS, BFS, UCS, A*) and Project 2 (Multi-Agent Search: Minimax, Alpha-Beta Pruning, Expectimax) to develop intelligent Pacman agents.
# PACMAN AI - Tích hợp Search & Multi-Agent Search

> **Dự án nhóm môn Trí tuệ nhân tạo** | Tham khảo bài tập **UC Berkeley CS188 - Project 1: Search** và **Project 2: Multi-Agent Search**.
>
> **Mục tiêu:** Xây dựng một tác nhân Pacman có khả năng tìm đường đến thức ăn và đưa ra quyết định khi có ma trong mê cung.

## 1. Giới thiệu dự án

Pacman AI là dự án phát triển tác nhân thông minh cho trò chơi Pacman trên nền mã nguồn bài tập CS188. Nhóm thực hiện hai mảng thuật toán:

- **Tìm kiếm đường đi (Project 1):** DFS, BFS, Uniform Cost Search (UCS), A* và các hàm heuristic phục vụ bài toán tìm thức ăn.
- **Tìm kiếm đa tác nhân (Project 2):** Reflex Agent, Minimax, Alpha-Beta Pruning, Expectimax và hàm đánh giá trạng thái khi Pacman đối mặt với ma.

**Định hướng tích hợp:** Thay vì chỉ chạy hai project riêng, nhóm phát triển thêm một tác nhân thống nhất: tận dụng kết quả tìm đường từ Project 1 để xác định hướng đi đến thức ăn, đồng thời xét rủi ro và các nước đi của ma bằng kỹ thuật từ Project 2. Tác nhân cần có cơ chế lập kế hoạch lại khi trạng thái trò chơi thay đổi.

> **Lưu ý về tiến độ:** Các thuật toán của PJ1/PJ2 là nội dung cần triển khai theo đề CS188. Tác nhân tích hợp và kết quả đánh giá chỉ được xem là hoàn thành sau khi nhóm viết code, chạy thử và xác nhận bằng kiểm thử. README này không khẳng định các tính năng đang chạy được nếu mã nguồn tương ứng chưa được bổ sung.

## 2. Mục tiêu và chức năng

| Thành phần | Nội dung | Vai trò |
| --- | --- | --- |
| Project 1 - Search | DFS, BFS, UCS, A*, Corners/Food Search, heuristic | Tìm đường đi đến mục tiêu và thức ăn |
| Project 2 - Multi-Agent | Reflex, Minimax, Alpha-Beta, Expectimax, Evaluation Function | Chọn hành động trong môi trường có ma |
| Integrated Pacman AI *(nhóm phát triển)* | Kết hợp lập kế hoạch đường đi và đánh giá nguy cơ | Điều khiển một Pacman AI thống nhất |
| Evaluation *(nhóm phát triển)* | Tỷ lệ thắng, điểm trung bình, thời gian tính toán, số nút mở rộng (khi đo được) | Đánh giá và so sánh các chiến lược |

## 3. Công nghệ sử dụng

- **Ngôn ngữ:** Python 3.
- **Nền tảng:** Bộ mã nguồn Pacman của UC Berkeley CS188.
- **Công cụ:** Git, GitHub; khuyến nghị Visual Studio Code.
- **Kiểm thử:** `autograder.py` đi kèm từng project.

Không tự động cài thư viện ngoài nếu chưa có yêu cầu trong bộ mã nguồn. Tùy hệ điều hành, phiên bản Pacman có giao diện đồ họa có thể cần **Tkinter**.

## 4. Cấu trúc thư mục dự kiến

```text
pacman-ai-integrated/
├── README.md
├── project1-search/             # Giữ riêng bộ mã nguồn Project 1
│   ├── pacman.py
│   ├── search.py
│   ├── searchAgents.py
│   ├── autograder.py
│   ├── layouts/
│   └── test_cases/
├── project2-multiagent/         # Giữ riêng bộ mã nguồn Project 2
│   ├── pacman.py
│   ├── multiAgents.py
│   ├── autograder.py
│   ├── layouts/
│   └── test_cases/
├── integrated/                  # Phần tích hợp do nhóm tự xây dựng
│   └── (sẽ bổ sung mã nguồn và hướng dẫn chạy)
└── docs/                        # Báo cáo, hình ảnh, kết quả thử nghiệm
```

**Quan trọng:** Project 2 yêu cầu sử dụng bộ mã nguồn riêng; **không chép đè toàn bộ file từ Project 1 sang Project 2**. Cấu trúc trên là gợi ý tổ chức repository, không phải danh sách file đã có sẵn trên GitHub.

## 5. Hướng dẫn cài đặt

### 5.1. Chuẩn bị

Cài đặt:

1. **Python 3** (kiểm tra bằng `python --version`; trên một số máy sử dụng `py -3 --version` hoặc `python3 --version`).
2. **Git** (kiểm tra bằng `git --version`).
3. **VS Code** hoặc trình soạn thảo Python bất kỳ.

### 5.2. Tải dự án từ GitHub

```bash
git clone https://github.com/24023079-max/REPOSITORY_NAME.git
cd pacman-ai-integrated
```

> Nếu nhóm đặt tên repository khác, hãy thay URL bằng đường dẫn HTTPS lấy tại nút **Code** trên GitHub.

### 5.3. Chuẩn bị mã nguồn

Nếu repository chưa có code, tải **bộ mã nguồn Project 1 và Project 2** từ tài liệu CS188 mà nhóm đang sử dụng, giải nén và đưa vào **hai thư mục riêng** `project1-search/` và `project2-multiagent/`. Giữ nguyên các file hỗ trợ và thư mục kiểm thử đi kèm từng bộ.

## 6. Hướng dẫn chạy thử

Các lệnh bên dưới chỉ hoạt động sau khi đã đưa **đúng bộ mã nguồn CS188** vào thư mục tương ứng và hoàn thiện các hàm được giao.

### 6.1. Chạy Project 1 - Search

Mở Terminal tại thư mục gốc repository:

```bash
cd project1-search
python pacman.py
```

Ví dụ chạy các thuật toán tìm kiếm:

```bash
# DFS
python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs

# BFS
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs

# UCS
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs

# A* với Manhattan heuristic
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```

Kiểm thử:

```bash
python autograder.py
python autograder.py -q q1
```

### 6.2. Chạy Project 2 - Multi-Agent Search

Mở Terminal mới tại thư mục gốc repository (hoặc quay lại thư mục gốc bằng `cd ..`):

```bash
cd project2-multiagent
python pacman.py -p ReflexAgent -l testClassic
```

Ví dụ chạy các tác nhân:

```bash
# Minimax
python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=2

# Alpha-Beta
python pacman.py -p AlphaBetaAgent -l smallClassic -a depth=2

# Expectimax
python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=2
```

Kiểm thử:

```bash
python autograder.py
python autograder.py -q q2
```

### 6.3. Chạy Integrated Pacman AI

**Đang phát triển.** Nhóm sẽ bổ sung lệnh chạy chính xác sau khi hoàn thiện tác nhân tích hợp và xác định cách đăng ký agent với bộ mã nguồn Pacman. Không sử dụng các lệnh chạy agent chưa tồn tại.

### 6.4. Xử lý lỗi cơ bản

- **`python` không được nhận diện:** Thử `py -3` trên Windows hoặc `python3` trên Linux/macOS.
- **`No such file or directory: pacman.py`:** Kiểm tra Terminal đã ở đúng thư mục `project1-search/` hoặc `project2-multiagent/`.
- **Lỗi hiển thị đồ họa/Tkinter:** Kiểm tra Python có hỗ trợ Tkinter; dùng tùy chọn `--no-graphics` cho autograder khi cần.
- **Không chạy được agent/thuật toán:** Kiểm tra hàm đã triển khai và tên lớp/hàm đúng theo đề CS188; chạy autograder của project tương ứng để xác định lỗi.

## 7. Phân công công việc

| Thành viên | Nhiệm vụ | Nhánh Git đề xuất |
| --- | --- | --- |
| Thành viên 1 | Hoàn thành PJ1: DFS, BFS, UCS, A*, Corners/Food Search, heuristic | `feature/search-algorithms` |
| Thành viên 2 | Hoàn thành PJ2: Reflex, Minimax, Alpha-Beta, Expectimax, Evaluation Function | `feature/multi-agent` |
| Thành viên 3 | Thiết kế agent tích hợp, phối hợp ghép module, kiểm thử, thống kê và demo | `feature/integration` |

Các thành viên 1 và 2 tiếp tục hỗ trợ sửa lỗi module của mình khi tích hợp, tránh dồn toàn bộ việc khắc phục xung đột cho thành viên 3.

## 8. Quy trình làm việc trên GitHub

Mỗi thành viên **clone repository một lần**, sau đó tạo nhánh riêng:

```bash
git switch main
git pull origin main
git switch -c feature/search-algorithms
```

Sau khi thay đổi code:

```bash
git status
git add .
git commit -m "Implement search algorithms"
git push -u origin feature/search-algorithms
```

Mở **Pull Request** trên GitHub để nhóm kiểm tra trước khi gộp vào `main`. Thay `feature/search-algorithms` bằng nhánh cá nhân của bạn. Không sửa trực tiếp `main` khi đang làm việc nhóm.

## 9. Kế hoạch đánh giá

Nhóm dự kiến thử nghiệm nhiều bản đồ và số lượng ma, sau đó tổng hợp:

- **Win rate (%):** Tỷ lệ ván thắng trên tổng số ván thử.
- **Average score:** Điểm trung bình của Pacman.
- **Execution time:** Thời gian xử lý/chạy thử.
- **Search cost / expanded nodes:** Độ dài hoặc chi phí đường đi và số nút tìm kiếm được mở rộng, khi có dữ liệu phù hợp.

Để so sánh công bằng, cần thống nhất bản đồ, số ma, số lần thử và (nếu có thể) hạt giống ngẫu nhiên. **Chưa có số liệu kết quả thực nghiệm trong README này.**

## 10. Tài liệu tham khảo và ghi nhận

- **UC Berkeley CS188 - Project 1: Search:** https://inst.eecs.berkeley.edu/~cs188/sp26/projects/proj1/
- **UC Berkeley CS188 - Project 2: Multi-Agent Search:** https://inst.eecs.berkeley.edu/~cs188/sp26/projects/proj2/

Bộ khung Pacman và các bài kiểm thử thuộc tài liệu môn học CS188; phần cài đặt thuật toán và tác nhân tích hợp là công việc nhóm tự thực hiện. Dự án phục vụ học tập và **không tuyên bố là sản phẩm chính thức của UC Berkeley**.

> **Lưu ý học thuật:** Không công khai lời giải bài tập nếu quy định của môn học hoặc nhà trường không cho phép; ưu tiên repository **Private** và chỉ cấp quyền cho thành viên nhóm/giảng viên.

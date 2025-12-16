# 真实地址生成器 API (Real Address Generator API)

这是一个基于 FastAPI 的服务，用于生成**真实存在的物理地址**（通过 OpenStreetMap 验证），并附带符合当地习惯的姓名和电话号码。该服务具有高度自适应性，能够处理多种国家输入格式（如 "US", "America", "美国"），并在特定城市或邮编无效时智能回退，确保始终返回有效结果。

## 功能特性

*   **真实地址**: 通过 OpenStreetMap (Nominatim) 获取真实存在的街道地址。
*   **智能自适应**: 能够处理输入冲突（例如：输入的城市不在所选国家内），优先保证在目标国家内生成真实地址。
*   **多语言支持**: 支持多种国家名称输入，包括英文、中文（如“美国”、“日本”）及 ISO 代码。
*   **本地化身份**: 生成与地址所在国家语言习惯相符的姓名和电话号码。
*   **易于部署**: 内置 `Dockerfile`，可直接部署至 Render 等平台。

## 本地运行

### 使用 Python

1.  安装依赖:
    ```bash
    pip install -r requirements.txt
    ```
2.  启动服务:
    ```bash
    uvicorn app.main:app --reload
    ```
3.  访问 API 文档: `http://localhost:8000/docs`.

### 使用 Docker

1.  构建镜像:
    ```bash
    docker build -t real-address-api .
    ```
2.  运行容器:
    ```bash
    docker run -p 8000:8000 real-address-api
    ```

## API 使用说明

### 接口: `GET /api/generate`

**参数:**
*   `country` (必填): 国家名称 (例如: "US", "China", "Germany", "美国").
*   `city` (可选): 偏好城市.
*   `zipcode` (可选): 偏好邮编.
*   `state` (可选): 偏好省/州.

**请求示例:**
```
GET /api/generate?country=US&city=New%20York
```

**响应示例:**
```json
{
  "name": "John Doe",
  "phone": "+1-555-0199",
  "address": "44 West 63rd Street",
  "city_state": "New York, New York",
  "zipcode": "10023",
  "country": "United States",
  "full_address": "Hotel Empire, 44, West 63rd Street, Lincoln Square, New York, 10023, United States"
}
```

## 部署 (Render)

1.  在 Render 上创建一个新的 **Web Service**。
2.  连接本仓库。
3.  Runtime 选择 **Docker**。
4.  Render 将自动读取 `Dockerfile` 进行构建和部署。

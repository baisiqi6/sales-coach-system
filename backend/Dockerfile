FROM python:3.11-slim

WORKDIR /app

# 构建时通过 --build-arg 传入代理地址（host.docker.internal:7890 = 宿主机 FlClash）
ARG HTTP_PROXY
ARG HTTPS_PROXY
ENV http_proxy=$HTTP_PROXY \
    https_proxy=$HTTPS_PROXY \
    no_proxy="localhost,127.0.0.1"

# 使用 trixie 源（与 python:3.11-slim 底层 Debian 13 版本匹配）
RUN rm -rf /etc/apt/sources.list.d/* && \
    cat > /etc/apt/sources.list << 'EOF'
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ trixie main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security/ trixie-security main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ trixie-updates main contrib non-free non-free-firmware
EOF

# 安装 PostgreSQL + Redis 客户端（pg_isready / redis-cli 用于 entrypoint 健康检查）
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

# 设置 pip 国内镜像，优先清华，没有时 fallback 到 PyPI
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip config set global.extra-index-url https://pypi.org/simple

# 先拷贝依赖文件，利用 Docker 缓存层
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝整个 backend 目录
COPY . .

# 确保 entrypoint 可执行
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]

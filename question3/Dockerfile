ARG PYTHON_VERSION=3.9
FROM python:${PYTHON_VERSION}

ARG CUDA_VERSION=cu118
ARG TORCH_VERSION=2.2.0

# Install Python and pip
RUN apt-get update && apt-get install -y python3-pip

# Install some dependencies such as Hugging Face Transformers and PyTorch
RUN pip3 install torch==${TORCH_VERSION} --index-url https://download.pytorch.org/whl/${CUDA_VERSION}
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy test script
COPY test.py .

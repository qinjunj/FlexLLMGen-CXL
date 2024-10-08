"""
Usage:
python3 profile_matmul.py
"""

import time

import numpy as np
import torch


def benchmark_func(func, number, repeat, warmup=3):
    for i in range(warmup):
        func()

    costs = []

    for i in range(repeat):
        torch.cuda.synchronize()
        tic = time.time()
        for i in range(number):
            func()
        torch.cuda.synchronize()
        costs.append((time.time() - tic) / number)

    return costs


def bench_matmul():
    for device in ["cuda"]:  # "cpu"
        for n in [1024, 2048, 4096, 8192]:
            if device == "cuda":
                dtype = torch.float16
            else:
                dtype = torch.float32

            a = torch.rand(n, n).to(dtype).to(device)
            b = torch.rand(n, n).to(dtype).to(device)

            def func():
                return torch.matmul(a, b)

            cost = np.mean(benchmark_func(func, number=5, repeat=3))

            tflops = 2 * n * n * n / cost / 1e12
            print(f"device: {device}, N: {n}, latency: {cost*1e3:.2f} ms, TFLOPS: {tflops:.3f}")
        print()


if __name__ == "__main__":
    bench_matmul()

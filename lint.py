#!/usr/bin/env python

import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """실행 명령어를 실행하고 결과를 출력합니다."""
    print(f"\n=== Running {description} ===")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"{description} failed!")
        sys.exit(result.returncode)
    print(f"{description} completed successfully!")

def main():
    # 프로젝트 루트 디렉토리 (pyproject.toml이 있는 위치)
    project_root = Path(__file__).parent.parent

    # 검사할 Python 파일들이 있는 디렉토리들
    python_dirs = ["app"]
    dirs_to_check = " ".join(python_dirs)

    # isort 실행
    run_command(
        f"isort {dirs_to_check} --settings-path {project_root}/pyproject.toml",
        "isort"
    )

    # black 실행
    run_command(
        f"black {dirs_to_check} --config {project_root}/pyproject.toml",
        "black"
    )

    # flake8 실행
    run_command(
        f"flake8 {dirs_to_check} --config={project_root}/flake8.cfg",
        "flake8"
    )

if __name__ == "__main__":
    main()
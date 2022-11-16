import argparse
from korBERT.similarity import get_similarity


def main():
    text = input("데이터 명세를 입력하세요 : ")
    get_similarity(text)


if __name__ == "__main__":
    main()

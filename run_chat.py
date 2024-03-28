import argparse
import os
import sys
from llama_cpp import Llama


def main(
    model_path="/home/ubuntu/isaac/telegram-chatbot/capybarahermes-2.5-mistral-7b.Q4_K_M.gguf",
    verbose=False,
    n_threads=16,
    seed=None,
):
    params = {
        "model_path": model_path,
        "n_ctx": 1024,
        "seed": seed,
        "n_threads": n_threads,
        "verbose": verbose,
        #'n_batch': 256,
        #'n_gpu_layers': 128
    }

    llm = Llama(**params)
    os.system("clear")

    messages = ""
    while True:
        prompt = input(">>> ")

        if prompt == "clear":
            print("=== Clear! ===")
            messages = ""
            continue

        if prompt == "bye":
            break

        messages += f"User: {prompt}\nAssistant: "

        stream = llm(
            messages,
            max_tokens=512,
            stream=True,
        )

        for output in stream:
            out_text = output["choices"][0]["text"]
            messages += out_text
            print(out_text, end="")
            sys.stdout.flush()

        messages += " "


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--n_threads", default=16, help="Number of threads to run the LLM."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Whether to have verbose outputs."
    )
    args = parser.parse_args()
    main(verbose=args.verbose)

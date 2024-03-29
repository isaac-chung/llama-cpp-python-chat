import os
import logging

from llama_cpp import Llama
import telebot

logging.basicConfig(level=logging.INFO)
TOKENS_TO_CLEAN = ["[INST]", "[/INST]", "<<ASSISTANT>>", "<</ASSISTANT>>", "<<START>>", "<</START>>", "<<SYS>>"]
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, threaded=False)

cwd = os.getcwd()
model_path = os.path.join(cwd, "capybarahermes-2.5-mistral-7b.Q4_K_M.gguf")
## Initialize LLM
params = {
    "model_path": model_path,
    "n_ctx": 32768,
    "chat_format": "llama-2",
    "seed": 4,
    "n_threads": 16,
    "max_tokens": 512,
    #'n_batch': 256,
    # 'n_gpu_layers': 35
}
llm = Llama(**params)

messages = [{"role": "system", "content": "You are a helpful assistant."}]


@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(message.chat.id, "To clear the message cache enter /clear.")


def clean_output_message(msg: str) -> str:
    for tkn in TOKENS_TO_CLEAN:
        msg = msg.replace(tkn, "")
    return msg


def clean_input_messages(msg: str) -> str:
    if msg in ".,/;:\[]\{\}":
        return "No message"
    return msg


@bot.message_handler(func=lambda message: True)
def chat(message):
    global messages
    chat_id = message.chat.id

    if message.text == "/clear":
        logging.info("Clear!")
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        bot.send_message(chat_id, "** reset **")
        return

    input_text = clean_input_messages(message.text)
    messages.append({"role": "user", "content": input_text})
    logging.info(f"{messages=}")

    bot.send_chat_action(chat_id, "typing")
    try:
        raw_output = llm.create_chat_completion(messages=messages, stop=["[/INST]", "\n\n", "<<USER>>"])
    except Exception as e:
        logging.info(f"Prompt failed. Fallback. {e}")
        messages.pop(-1)
        messages.append({"role": "user", "content": "No message"})
        raw_output = llm.create_chat_completion(messages=messages, stop=["[/INST]", "\n\n", "<<USER>>"])

    usage = raw_output.get("usage", "")
    logging.info(f"{usage=}")

    if len(raw_output.get("choices")) == 0:
        messages.append({"role": "assistant", "content": "No message"})

    output_text = raw_output["choices"][0]["message"]["content"]
    logging.info(f"raw = {output_text}")
    output_text = clean_output_message(output_text)
    logging.info(f"cleaned = {output_text}")
    bot.send_message(chat_id, output_text)
    messages.append({"role": "assistant", "content": output_text})


bot.infinity_polling()

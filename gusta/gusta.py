import json
import datetime
import os
import tkinter as tk
import openai as ai
from newspaper import Article


def startup():
    def fill_templates(templates_dict):
        """Later we will need three components of a prompt template."""
        for v in templates_dict.values():
            while len(v) < 3:
                v.append("")
        return templates_dict

    # The file with efault prompt templates and GUI messages and labels.
    with open("config.json", "r", encoding="utf-8") as t:
        t = json.loads(t.read())
        engines = t["engines"]
        templates = fill_templates(t["templates"])
        interface = t["interface"]

    # The customisable config file with API key and custom templates.
    try:
        with open("config.user.json", "r", encoding="utf-8") as c:
            c = json.loads(c.read())
            try:
                apikey = c["key"]
            except:
                apikey = "xxx"
                interface["message_down"] = interface["message_down_no_key"]
                interface["answer"] = interface["answer_no_key"]
            try:
                if c["archive"].lower() == "false":
                    archive = False
                else:
                    archive = True
            except:
                archive = True
            try:
                archive_path = c["archive_path"]
            except:
                archive_path = "archive"
            if c["currency"]:
                currency = c["currency"]["shortcut"]
                rate = c["currency"]["exchange_rate_to_USD"]
            else:
                currency = "$"
                rate = 1
            templates_custom = fill_templates(c["templates"])
            templates.update(templates_custom)
    except:
        apikey, currency, rate, archive, archive_path = "", "", 1, False, ""
        interface["message_up"] = interface["message_up_no_key"]
        interface["message_down"] = interface["message_down_no_key"]
        interface["answer"] = interface["answer_no_key"]

    return (
        apikey,
        interface,
        engines,
        templates,
        currency,
        rate,
        archive,
        archive_path,
    )


def dear_gpt(apikey, selected_engine, system_prompt, prompt1, input, prompt2):
    """The interface between the script and the GPT magic."""
    ai.api_key = apikey
    separator1 = "\n\n***\n\n"
    separator2 = "\n\n***\n\n"
    if len(prompt1) < 1:
        separator1 = ""
    if len(prompt2) < 1:
        separator2 = ""
    answer = ai.ChatCompletion.create(
        model=selected_engine,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"""{prompt1}{separator1}{input}{separator2}{prompt2}""",
            },
        ],
    )
    return answer


def gustaokno():
    """This is where the circus takes place."""

    def clean_input(*args):
        """Cleans the upper text field."""
        if frame1.get(1.0, tk.END).strip() == interface["message_up"].strip():
            frame1.delete(1.0, tk.END)

    def clean_url(*args):
        """Cleans the upper text field."""
        if address_bar.get(1.0, tk.END).strip() == interface["url"].strip():
            address_bar.delete(1.0, tk.END)

    def scrape_article(url):
        """Loads a web page and scrapes the text of the article. Hopefully"""
        try:
            article = Article(url)
            article.download()
            article.parse()
            article = article.text
        except Exception as e:
            article = f"{e}.strip()"
        return article

    def insert_article_text(url):
        """Inserts the text of the scraped article."""
        frame1.delete(1.0, tk.END)
        frame1.insert(tk.END, scrape_article(url))
        address_bar.delete(1.0, tk.END)

    def set_prompt(selected_option):
        """I gues this is redundant but I don't know what to do."""
        return selected_option

    def set_engine(selected_engine):
        """I gues this is redundant but I don't know what to do."""
        return selected_engine

    def clip():
        """Copies the content of the lower text field to the clipboard."""
        window.clipboard_clear()
        window.clipboard_append(frame3.get("1.0", tk.END))

    def gustav(selected_engine, selected_option, input):
        """A wrapper for the prompting function."""
        frame3.delete(1.0, tk.END)
        system_prompt = templates[selected_option][0]
        prompt1 = templates[selected_option][1]
        prompt2 = templates[selected_option][2]
        reply = dear_gpt(
            apikey, selected_engine, system_prompt, prompt1, input, prompt2
        )
        frame3.insert(tk.END, reply.choices[0].message.content.strip())
        money = (
            int(reply.usage.prompt_tokens)
            / 1000
            * float(engines[selected_engine][1] * float(rate))
        ) + (
            int(reply.usage.completion_tokens)
            / 1000
            * float(engines[selected_engine][2] * float(rate))
        )
        window.title(
            f"""{interface["title"]} ({int(reply.usage.prompt_tokens) + 
            int(reply.usage.completion_tokens)} tokens, {'{0:.2f}'.format(money)} {currency})"""
        )
        if archive:
            if not os.path.exists(archive_path):
                os.makedirs(archive_path)
            record = {}
            record["time"] = str(datetime.datetime.now())
            record["system_prompt"] = system_prompt
            record["prompt"] = prompt1 + " " + input + " " + prompt2
            record["reply"] = reply.choices[0].message.content.strip()
            filename = f"""{record["time"].replace(":", "-").replace(" ", "-").split(".")[0]}.txt"""
            with open(
                os.path.join(archive_path, filename), "w+", encoding="utf-8"
            ) as a:
                json.dump(record, a, ensure_ascii=False)
            with open(
                os.path.join(archive_path, filename), "w+", encoding="utf-8"
            ) as a:
                json.dump(reply, a, ensure_ascii=False)
        return ()

    def switch_top():
        """Switches staying on top."""
        if window.attributes("-topmost"):
            window.attributes("-topmost", False)
        else:
            window.attributes("-topmost", True)

    def switch_archive():
        """Switches saving the prompts and answers into Archive folder."""
        global archive
        if archive:
            archive = False
        else:
            archive = True

    window = tk.Tk()
    window.title(f"""{interface["title"]}""")
    window.geometry("440x680")

    top_bar = tk.Frame(master=window, pady=2, padx=5)
    top_bar.pack(fill="both")

    engine_choices = [x for x in engines.keys()]
    selected_engine = tk.StringVar()
    selected_engine.set(engine_choices[0])

    dropdown_engines = tk.OptionMenu(
        top_bar, selected_engine, *engine_choices, command=set_engine
    )
    dropdown_engines.config(border=1)
    dropdown_engines.pack(side="left", fill="both")

    button_scrape = tk.Button(
        top_bar,
        text=interface["scrape"],
        command=lambda: insert_article_text(address_bar.get(1.0, tk.END).strip()),
        border=1,
        pady=2,
        height=1,
    )
    button_scrape.pack(side="right", fill="both")

    address_bar = tk.Text(top_bar, wrap="none", height=1, padx=5, pady=5)
    address_bar.pack(side="left")
    address_bar.insert(tk.END, interface["url"])

    upper_window = tk.Frame(master=window, height=120)
    upper_window.pack(fill="both")
    upper_window.pack_propagate(0)

    scroll1 = tk.Scrollbar(upper_window)
    scroll1.pack(side="right", fill="y")

    frame1 = tk.Text(
        master=upper_window, wrap="word", padx=10, pady=10, yscrollcommand=scroll1.set
    )
    frame1.pack(side="left", fill="both")
    frame1.insert(tk.END, interface["message_up"])

    frame2 = tk.Frame(master=window, pady=2, padx=5)
    frame2.pack(fill="both")

    prompt_choices = [x for x in templates.keys()]
    selected_option = tk.StringVar()
    selected_option.set(prompt_choices[0])

    dropdown_templates = tk.OptionMenu(
        frame2, selected_option, *prompt_choices, command=set_prompt
    )
    dropdown_templates.config(border=1)
    dropdown_templates.pack(side="left", fill="both", expand=True)

    button_response = tk.Button(
        frame2,
        text=interface["answer"],
        command=lambda: gustav(
            selected_engine.get(),
            selected_option.get(),
            frame1.get(1.0, tk.END).strip(),
        ),
        bd=1,
        pady=2,
    )
    button_response.pack(fill=tk.BOTH, expand=1)

    lower_window = tk.Frame(master=window)
    lower_window.pack(fill="both", expand=True)

    scroll2 = tk.Scrollbar(lower_window)
    scroll2.pack(side="right", fill="y")

    frame3 = tk.Text(
        master=lower_window, wrap="word", padx=10, pady=10, yscrollcommand=scroll2.set
    )
    frame3.pack(side="left", fill="both", expand=True)
    frame3.insert(tk.END, interface["message_down"])

    status_bar = tk.Frame(master=window, pady=2, padx=5, height=20)
    status_bar.pack(fill="both")
    status_bar

    button_top = tk.Checkbutton(status_bar, text=interface["top"], command=switch_top)
    button_top.pack(side="left")

    button_archive = tk.Checkbutton(
        status_bar, text=interface["archive"], command=switch_archive
    )
    button_archive.pack(side="left")
    if archive:
        button_archive.select()

    button_copy = tk.Button(
        status_bar, text=interface["copy"], command=clip, border=1, pady=2
    )
    button_copy.pack(side="left", fill="both", expand=True)

    scroll1.config(command=frame1.yview)
    scroll2.config(command=frame3.yview)

    frame1.bind("<Button-1>", clean_input)
    frame1.bind(
        "<Control-Return>",
        lambda event: gustav(
            selected_engine.get(),
            selected_option.get(),
            frame1.get(1.0, tk.END).strip(),
        ),
    )
    address_bar.bind("<Button-1>", clean_url)

    window.mainloop()


# It's showtime folks!

apikey, interface, engines, templates, currency, rate, archive, archive_path = startup()

gustaokno()

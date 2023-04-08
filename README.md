# Gusta the GPT prompt processor

Living with ADHD, I hate these things about ChatGPT:

- It takes ages for the chat interface to finally load.
- It's such a pain to type out the same prompts over and over again.
- Too often, I switch tabs while waiting for the response to appear, and then later, I accidentally close the tab with the response without ever seeing it.

So, I created Gusta - the GPT prompt processor.

- Gusta allows you to choose from prompt templates, both default and custom.
- It saves the prompts and responses in JSON files (this feature can be turned off).
- A URL can be easily scraped for an article's content with just a single click.
- The price of the last job is shown in either dollars or your preferred currency.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Contributing](#contributing)
4. [License](#license)

## Installation

### Prerequisites

- Python
- Newspaper3k
- openai

### Installing

1. Clone the repository:

   ```
   git clone https://github.com/michalkasparek/gusta/project.git
   ```
   
2. Navigate to the project directory:

   ```
   cd project
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

4. Rename `config.user_sample.json` to `config.user.json`. Open it and save your API key ([https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)) in the "key" field, then save the file.

5. If you want to add your own templates, add them to the `config.user.json` file. Get inspiration from the sample templates included in the file.

## Usage

__

## Contributing

### To-do

- Exception handling has not been implemented yet, which means there are no error messages. Some of the usual cases:
   - Bad API key.
   - The input is too long.
   - GPT servers are down.
   - Problems with internet connection.
- Some parts of the interface disappear when the window is resized below 420 x 630 pixels.

## License

Gusta is licensed under the MIT License.
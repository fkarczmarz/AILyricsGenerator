import os
import pandas as pd
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling

def load_dataset(file_path, tokenizer, block_size=128):
    dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=file_path,
        block_size=block_size,
    )
    return dataset

def train_model(artist, data_path, model_name='gpt2', output_dir_base="../model"):
    # Load pre-trained model and tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # Load dataset
    dataset = load_dataset(data_path, tokenizer)

    # Define output directory for the artist model
    output_dir = os.path.join(output_dir_base, f"gpt2-lyrics-{artist}")

    # Define training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        save_steps=10_000,
        save_total_limit=2,
    )

    # Create data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset,
    )

    # Train the model
    trainer.train()

    # Save the final model
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Model trained and saved for artist: {artist}")

def main():
    input_dir = os.path.join("..", "data", "processed_lyrics")
    model_name = "gpt2"

    for artist_file in os.listdir(input_dir):
        if artist_file.endswith('.csv'):
            artist = os.path.splitext(artist_file)[0].replace("_lyrics", "")
            data_path = os.path.join(input_dir, artist_file)
            train_model(artist, data_path, model_name)

if __name__ == "__main__":
    main()

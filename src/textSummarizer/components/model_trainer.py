from transformers import TrainingArguments, Trainer
from transformers import DataCollatorForSeq2Seq
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
from datasets import load_dataset, load_from_disk
import os
from textSummarizer.entity import ModelTrainerConfig

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_ckpt)
        model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt).to(device)
        seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer, model=model_pegasus)

        #Loading Data
        dataset_samsum_pt = load_from_disk(self.config.data_path)
        train_subset = dataset_samsum_pt["train"].select(range(5))
        eval_subset = dataset_samsum_pt["validation"].select(range(5))

        trainer_args = TrainingArguments(output_dir=self.config.root_dir,
                                         num_train_epochs = self.config.num_train_epochs,
                                         warmup_steps = self.config.warmup_steps,
                                         per_device_train_batch_size = self.config.per_device_train_batch_size,
                                         weight_decay = self.config.weight_decay,
                                         logging_steps = self.config.logging_steps,
                                         eval_strategy = self.config.eval_strategy,
                                         eval_steps = self.config.eval_steps,
                                         save_strategy = self.config.save_strategy,
                                         gradient_accumulation_steps = self.config.gradient_accumulation_steps)
        
        trainer = Trainer(model=model_pegasus, args=trainer_args,
                  tokenizer=tokenizer, data_collator=seq2seq_data_collator,
                  train_dataset=train_subset,
                  eval_dataset=eval_subset)
        
        trainer.train()
        #Save Model
        model_pegasus.save_pretrained(os.path.join(self.config.root_dir, "pegasus-samsum-model"))
        #Save Tokenizer
        tokenizer.save_pretrained(os.path.join(self.config.root_dir, "tokenizer"))


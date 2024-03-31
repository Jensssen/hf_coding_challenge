import gcsfs
import os
from datasets import load_dataset
from transformers import AutoTokenizer, DataCollatorWithPadding, TrainerCallback, AutoModelForSequenceClassification, \
    Trainer, TrainingArguments

raw_datasets = load_dataset("glue", "mrpc")
checkpoint = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
checkpoint_directory = "my_checkpoints"


def tokenize_function(example):
    return tokenizer(example["sentence1"], example["sentence2"], truncation=True)


class SyncWithExternalStorage(TrainerCallback):

    def __init__(self, local_checkpoint_dir: str, gcp_project: str = 'my-test-gcp-project',
                 gcs_bucket: str = 'my-bucket-name'):
        super().__init__()
        self.local_checkpoint_dir = local_checkpoint_dir
        self.gcp_project = gcp_project
        self.gcs_bucket = gcs_bucket
        self.fs = gcsfs.GCSFileSystem(project=gcp_project)

    def on_save(self, args, state, control, logs=None, **kwargs) -> None:
        """Callback function, triggered when ever a new model is saved."""
        local_directory_path = os.path.join(self.local_checkpoint_dir, f"checkpoint-{state.global_step}")
        for root, directories, files in os.walk(local_directory_path):
            for file_name in files:
                local_file_path = os.path.join(root, file_name)
                gcs_destination_file_path = os.path.join(self.gcs_bucket, f"checkpoint-{state.global_step}", file_name)
                self.write_file_to_bucket(local_file_path, gcs_destination_file_path)

    def write_file_to_bucket(self, local_file_path: str, destination_file_path: str) -> None:
        """
        Save local file to remote storage bucket.

        Args:
            local_file_path: Path to local file that shall be uploaded.
            destination_file_path: Destination path of file on GCS.
        """
        with open(local_file_path, 'rb') as local_file:
            with self.fs.open(destination_file_path, 'wb') as file:
                file.write(local_file.read())
        print(f"File saved to {destination_file_path}")


tokenized_datasets = raw_datasets.map(tokenize_function, batched=True)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

training_args = TrainingArguments(checkpoint_directory)

model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2)

trainer = Trainer(
    model,
    training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    data_collator=data_collator,
    tokenizer=tokenizer,
    callbacks=[SyncWithExternalStorage(local_checkpoint_dir=checkpoint_directory)]
)

trainer.train()

predictions = trainer.predict(tokenized_datasets["validation"])
print(predictions.predictions.shape, predictions.label_ids.shape)

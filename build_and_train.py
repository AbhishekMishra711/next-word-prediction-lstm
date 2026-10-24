import json
import math
import os
import re
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

# 1. Corpus Preparation
sample_text = """
artificial intelligence is transforming the way humans interact with technology.
machine learning algorithms can learn complex patterns directly from data.
deep learning models are composed of multiple layers of artificial neural networks.
natural language processing helps to understand, interpret, and generate human language.
recurrent neural networks are designed to process sequential data effectively.
long short term memory networks overcome the vanishing gradient problem in traditional recurrent models.
next word prediction is a fundamental task in language modeling and natural language understanding.
the model predicts the next word based on the context of preceding tokens.
language models assign a probability distribution over sequences of words.
sequence prediction is widely used in smartphone keyboards and search query suggestions.
recurrent architectures maintain an internal memory state across time steps.
the input gate decides which information should be updated in the memory cell.
the forget gate removes obsolete information from the previous hidden state.
the output gate determines what the next hidden state should contain.
deep neural networks achieve high accuracy when trained on large textual corpora.
text preprocessing involves lowercasing, tokenization, and vocabulary creation.
word embeddings map discrete tokens into dense continuous vector representations.
loss functions like cross entropy measure the difference between predicted and actual tokens.
perplexity is an intrinsic evaluation metric for measuring language model quality.
lower perplexity indicates better predictive confidence and performance.
transfer learning has revolutionized modern artificial intelligence research.
large language models have demonstrated remarkable reasoning and generation capabilities.
computer vision and natural language processing are two major subfields of artificial intelligence.
intelligent conversational agents rely on deep language models for dialogue generation.
the system was designed to predict the most probable word following a user prompt.
users can type a prompt and receive top candidate suggestions instantly.
gradient descent iteratively optimizes the network weights to minimize loss.
regularization techniques such as dropout prevent the neural network from overfitting.
bidirectional models consider both past and future context in sentence comprehension.
attention mechanisms allow models to focus dynamically on relevant tokens in context.
the training pipeline converts raw text into sequential n gram training pairs.
evaluation metrics include training loss, validation accuracy, top five accuracy, and perplexity.
the interactive web interface allows seamless exploration of language model predictions.
modern smartphone keyboards use next word prediction to improve typing speed.
data science combines statistics, computer science, and domain knowledge to extract insights.
computational linguistics bridges the gap between human language and computer programs.
deep learning architectures continue to evolve with new attention and recurrence mechanisms.
an effective language model balances vocabulary size with computational efficiency.
text generation can be performed greedily or by sampling from candidate probabilities.
the next word prediction system demonstrates the practical utility of lstm networks in nlp.
"""

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

cleaned = clean_text(sample_text)
tokens = cleaned.split()

# Vocabulary construction
special_tokens = ['<PAD>', '<UNK>']
unique_words = sorted(list(set(tokens)))
vocab = special_tokens + unique_words
word2idx = {w: i for i, w in enumerate(vocab)}
idx2word = {i: w for i, w in enumerate(vocab)}

print(f"Total tokens in corpus: {len(tokens)}")
print(f"Unique vocabulary size: {len(vocab)}")

# Sequence creation (Context window = 5)
seq_length = 4
sequences = []
for i in range(seq_length, len(tokens)):
    input_seq = tokens[i - seq_length:i]
    target_token = tokens[i]
    sequences.append((input_seq, target_token))

print(f"Total training sequences: {len(sequences)}")

class TextDataset(Dataset):
    def __init__(self, sequences, word2idx):
        self.data = []
        for inp, tgt in sequences:
            inp_idx = [word2idx.get(w, word2idx['<UNK>']) for w in inp]
            tgt_idx = word2idx.get(tgt, word2idx['<UNK>'])
            self.data.append((torch.tensor(inp_idx, dtype=torch.long), torch.tensor(tgt_idx, dtype=torch.long)))
            
    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, idx):
        return self.data[idx]

dataset = TextDataset(sequences, word2idx)
loader = DataLoader(dataset, batch_size=16, shuffle=True)

# 2. LSTM Model Definition
class LSTMNextWord(nn.Module):
    def __init__(self, vocab_size, embed_dim=128, hidden_dim=256, num_layers=2, dropout=0.2):
        super(LSTMNextWord, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, num_layers=num_layers, batch_first=True, dropout=dropout if num_layers > 1 else 0.0)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim, vocab_size)
        
    def forward(self, x):
        emb = self.dropout(self.embedding(x))
        out, _ = self.lstm(emb)
        out = self.dropout(out[:, -1, :])  # take last timestep output
        logits = self.fc(out)
        return logits

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = LSTMNextWord(len(vocab), embed_dim=128, hidden_dim=256, num_layers=2, dropout=0.2).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.003, weight_decay=1e-5)

# 3. Training Loop
epochs = 60
history = {'loss': [], 'perplexity': [], 'top1_acc': [], 'top5_acc': []}

for epoch in range(1, epochs + 1):
    model.train()
    total_loss = 0.0
    correct_top1 = 0
    correct_top5 = 0
    total_samples = 0
    
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item() * inputs.size(0)
        _, top5_pred = outputs.topk(5, dim=-1)
        _, top1_pred = outputs.topk(1, dim=-1)
        
        correct_top1 += (top1_pred.squeeze(-1) == targets).sum().item()
        correct_top5 += (top5_pred == targets.unsqueeze(-1)).any(dim=-1).sum().item()
        total_samples += inputs.size(0)
        
    avg_loss = total_loss / total_samples
    ppl = math.exp(avg_loss) if avg_loss < 20 else 99999.0
    top1 = correct_top1 / total_samples * 100
    top5 = correct_top5 / total_samples * 100
    
    history['loss'].append(round(avg_loss, 4))
    history['perplexity'].append(round(ppl, 2))
    history['top1_acc'].append(round(top1, 2))
    history['top5_acc'].append(round(top5, 2))
    
    if epoch % 10 == 0 or epoch == 1:
        print(f"Epoch {epoch:02d}/{epochs} - Loss: {avg_loss:.4f} - Perplexity: {ppl:.2f} - Top-1 Acc: {top1:.2f}% - Top-5 Acc: {top5:.2f}%")

# Save model and metadata
torch.save(model.state_dict(), 'next_word_lstm.pth')
with open('metadata.json', 'w') as f:
    json.dump({
        'vocab': vocab,
        'word2idx': word2idx,
        'idx2word': idx2word,
        'seq_length': seq_length,
        'embed_dim': 128,
        'hidden_dim': 256,
        'num_layers': 2,
        'final_metrics': {
            'loss': history['loss'][-1],
            'perplexity': history['perplexity'][-1],
            'top1_acc': history['top1_acc'][-1],
            'top5_acc': history['top5_acc'][-1]
        },
        'history': history
    }, f, indent=2)

print("Training finished! Model saved to next_word_lstm.pth and metadata.json")

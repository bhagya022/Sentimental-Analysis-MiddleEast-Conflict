# Crisis Sentiment Analysis Pipeline

A domain-adapted, multi-model sentiment analysis pipeline for social media comments on geopolitical and economic crisis events, built without any model fine-tuning.

---

## Overview

This project analyses public sentiment across Instagram, X (Twitter), and Reddit on crisis topics including the LPG price crisis in India, Iran-Israel war, farmer distress, Pakistan economic crisis, Ukraine war, and India heatwave.

The pipeline uses a three-model ensemble architecture with eight rule-based decision layers to classify comments as Positive, Negative, or Neutral - handling sarcasm, double negation, resolution statements, speculative language, and shrinkflation detection.

---

## Model Architecture

```
  Input Comment
      |
  Preprocessing
  (clean, min word check, statistical fact detection)
      |
  Negation Normalisation
  (rewrite double negations before model inference)
      |
  +-----------------------------------------------------+
  |  BART-MNLI          ->  emotion labels and scores   |
  |  RoBERTa Sentiment  ->  Positive / Negative / Neutral  |
  |  RoBERTa Irony      ->  sarcasm True / False        |
  +-----------------------------------------------------+
      |
  8-Rule Decision Layer
      |
  Final Sentiment + Confidence Score
```

### Models Used

| Model | Source | Role |
|---|---|---|
| facebook/bart-large-mnli | HuggingFace | Primary zero-shot emotion classifier |
| cardiffnlp/twitter-roberta-base-sentiment-latest | HuggingFace | Sentiment cross-checker for ensemble |
| cardiffnlp/twitter-roberta-base-irony | HuggingFace | Sarcasm and irony detection |

---

## The 8 Decision Rules

| Rule | Name | Description |
|---|---|---|
| 1 | Shrinkflation Detection | Product size or weight reduction classified as Negative |
| 2 | Resolution Phrase Matching | Confirmed good news classified as Positive |
| 3 | Hedge Language | Speculative statements classified as Neutral |
| 4 | BART Sarcasm Flag | Internal BART sarcasm score override |
| 5 | Irony Detector | External irony model sarcasm override |
| 6 | Negation Confirmation | Confirmed negations classified as Negative |
| 7 | Ensemble Vote | BART and RoBERTa combined decision |
| 8 | Context Flip Guard | RoBERTa overrides BART false positives |

---

## Requirements

```
Python 3.10 or higher
transformers
torch
pandas
matplotlib
openpyxl
tqdm
emoji
```

Install all dependencies:

```bash
pip install transformers torch pandas matplotlib openpyxl tqdm emoji
```

---

## How to Run

### Option 1 — Google Colab (Recommended)

1. Open Google Colab at colab.research.google.com
2. Upload SA_final.py and your data file to /content/
3. Run the following in a cell:

```python
exec(open('SA_final.py').read())
```

4. When prompted, choose one of the three modes described below.

### Option 2 — Local Machine

```bash
git clone https://github.com/yourusername/crisis-sentiment-analysis.git
cd crisis-sentiment-analysis
pip install transformers torch pandas matplotlib openpyxl tqdm emoji
python SA_final.py
```

---

## Usage Modes

When the script runs it will prompt you to select a mode:

```
Choose Option:
1 -> Run Full Pipeline
2 -> Live Comment Checker
3 -> Quick Tests

Enter choice:
```

### Mode 1 - Full Pipeline

Processes an entire CSV or Excel file end to end. Before running, update the CONFIG block at the top of SA_final.py with your file paths:

```python
CONFIG = {
    'input_file'  : '/content/your_file.xlsx',
    'output_file' : '/content/results.xlsx',
    'eda_output'  : '/content/eda.png',
}
```

The pipeline will automatically detect comment, date, and platform columns, remove null comments and duplicates, fill null dates with the most common date in the dataset, fill null platform values with the most common platform, run all three models on each comment, and export a colour-coded Excel file with an EDA visualisation.

### Mode 2 - Live Comment Checker

Type any comment and receive an instant sentiment prediction. Type exit to stop.

```
Enter comment (or type 'exit'): LPG prices have gone up again this month

Comment      : LPG prices have gone up again this month
Sentiment    : Negative
Emotion      : frustrated or angry
Score        : 0.724
Irony        : False
Confidence   : HIGH
```

This mode is useful for testing individual comments or demonstrating the pipeline interactively. It uses the same three models and eight rules as the full pipeline.

### Mode 3 - Quick Tests

Runs a built-in set of labelled test cases covering Positive, Negative, and Neutral categories and reports accuracy. Use this to verify the pipeline is working correctly after setup or after making any changes to the code.

```
#    Expected   Got        Match
--------------------------------------
1    Positive   Positive   True
2    Negative   Negative   True
3    Neutral    Neutral    True

Accuracy : 7/8 = 87%
```

---

## Input File Format

The pipeline auto-detects columns by name. Your CSV or Excel file should contain the following:

| Column | Accepted Names | Required |
|---|---|---|
| Comment text | comment, text, tweet, sentence, review | Yes |
| Post date | date, time, created_at | Optional |
| Platform | type, platform, source | Optional |

A sample input file test_data.xlsx is included in the repository. It contains 58 comments across six crisis domains with intentional null values and duplicates to demonstrate the EDA and data cleaning steps.

---

## Output Format

Each processed comment receives the following columns in the output:

| Column | Description |
|---|---|
| sentiment | Positive, Negative, or Neutral |
| emotion | Detailed emotion label assigned by BART |
| score | Model confidence score between 0 and 1 |
| irony | Whether sarcasm was detected |
| confidence | HIGH, MEDIUM, or LOW |

The output Excel file uses colour coding — green rows for Positive, red rows for Negative, and yellow rows for Neutral. A Summary sheet is included with overall counts and processing timestamp.

---

## Crisis Domains Tested

| Domain | Type |
|---|---|
| LPG Crisis India | National |
| Iran-Israel War | International |
| Farmer Distress India | National |
| Pakistan Economy | Regional |
| Ukraine War | International |
| India Heatwave | National |

The pipeline is domain-specific and optimised for crisis and geopolitical social media text. Performance on unrelated everyday content is lower by design, which is expected behaviour for a zero-shot domain-adapted system and not indicative of overfitting.

---

## Limitations

- Sarcasm detection works well on obvious patterns but may miss subtle irony
- Resolution statements with ambiguous context may occasionally be misclassified
- The pipeline is optimised for crisis text and not intended as a general purpose sentiment classifier
- No model fine-tuning was performed all classification is zero-shot

## Key Findings

- Negative sentiment dominated LPG crisis discourse across all platforms
- Peak negative sentiment observed during March to April 2025 coinciding with Iran-Israel conflict escalation
- Zero-shot models exhibit negativity bias on crisis-domain text without domain adaptation
- Combining BART internal sarcasm scores with a dedicated irony model improved sarcasm detection significantly
- Resolution statements require explicit phrase matching to overcome domain vocabulary bias in zero-shot models

## Tech Stack

- Python 3.10+
- HuggingFace Transformers
- PyTorch
- pandas
- matplotlib
- openpyxl
- Google Colab


## License

MIT License. Free to use, modify, and distribute with attribution.

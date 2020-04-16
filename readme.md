# A BiLSTM-CRF model for Auto-Repair-Domain Named Entity Recognition

This repository includes the code for buliding a very simple __character-based BiLSTM-CRF sequence labeling model__ for Auto-Repair Domain Named Entity Recognition task. Its goal is to recognize three types of Named Entity: CAR, CPT and BRD. They refer to the car brand, car-component name, car-breakdown code.

This code works on __Python 3 & TensorFlow 1.2__ .

## Model



For one Auto-Repair sentence, each character in this sentence has / will have a tag which belongs to the set {O, B-CAR, I-CAR, B-CPT, I-CPT, B-BRD, I-BRD}.

The first layer, __look-up layer__, aims at transforming each character representation from one-hot vector into *character embedding*. In this code I initialize the embedding matrix randomly. We could add some linguistic knowledge later. For example, do tokenization and use pre-trained word-level embedding, then augment character embedding with the corresponding token's word embedding. In addition, we can get the character embedding by combining low-level features (please see paper[2]'s section 4.1 and paper[3]'s section 3.3 for more details).

The second layer, __BiLSTM layer__, can efficiently use *both past and future* input information and extract features automatically.

The third layer, __CRF layer__,  labels the tag for each character in one sentence. If we use a Softmax layer for labeling, we might get ungrammatic tag sequences beacuse the Softmax layer labels each position independently. We know that 'I-CPT' cannot follow 'B-CAR' but Softmax doesn't know. Compared to Softmax, a CRF layer can use *sentence-level tag information* and model the transition behavior of each two different tags.

## Dataset


My original corpus comes from more than 20,000 articles in the automotive field, containing more than 210,000 sentences and a total of 12 million characters.

|    | #sentence | #CAR | #CPT | #BRD |
| :----: | :---: | :---: | :---: | :---: |
| train  | 146354 | 127954 | 112549 | 29571 |
| test   | 68620  | 54413  | 66406  | 11137  |

### corpus files

Due to the privacy, the data in this folder is provided by the project company I serve. You can obtain the vocabulary and corpus data online.But I have provided a few samples.The directory `./corpus` contains:

- the unprocessed original corpus file,`car_ner_corpus.xlsx`.
- the word dicts for car,component and breakdown code.

### data files

The directory `./data_path` contains:

- the preprocessed data files, `train_data` and `test_data` 
- a vocabulary file `word2id.pkl` that maps each character to a unique id  

For generating vocabulary file, please refer to the code in `data.py`. 

### data format

Each data file should be in the following format:

```
奔	B-CAR
驰	I-CAR
发	B-CPT
动	I-CPT
机	I-CPT
很	O
不	O
错	O
！	O

句	O
子	O
结	O
束	O
是	O
空	O
行	O
。	O
```

If you want to use your own dataset, please: 

- transform your corpus to the above format
- generate a new vocabulary file

## Quick to start

### train

`python main.py --mode=train `

### test

`python main.py --mode=test --demo_model=1586944910`

`1586944910` is my trained model for your guys. 

Metric Performance:

| P     | R     | F     | 
| :---: | :---: | :---: |
| 0.9802 | 0.9716 | 0.9759 |

An official evaluation tool for computing metrics: [click here](http://sighan.cs.uchicago.edu/bakeoff2006/)

### demo

`python main.py --mode=demo --demo_model=1586944910`

You can input one auto-related sentence and the model will return the recognition result:


## Reference

Thanks to these open source projects for their help

\[0\][https://github.com/Determined22/zh-NER-TF](https://github.com/Determined22/zh-NER-TF)

\[1\] [Bidirectional LSTM-CRF Models for Sequence Tagging](https://arxiv.org/pdf/1508.01991v1.pdf)

\[2\] [Neural Architectures for Named Entity Recognition](http://aclweb.org/anthology/N16-1030)

\[3\] [Character-Based LSTM-CRF with Radical-Level Features for Chinese Named Entity Recognition](https://link.springer.com/chapter/10.1007/978-3-319-50496-4_20)

\[4\] [https://github.com/guillaumegenthial/sequence_tagging](https://github.com/guillaumegenthial/sequence_tagging)  

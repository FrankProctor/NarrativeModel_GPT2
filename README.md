# Narrative Text Generation Using GPT-2

For the explainating on GPT-2 Model and article generation, please read [here](https://oursky.quip.com/ta3HA42rjZIr/Article-Generation-and-GPT-2-Model)

## Processing text extracted from In-Design files

### Extracting text for In-Design files
Text inside a In-Design files (*.indd) could be extracted using In-Design itself,
the way to do so is select following in the menu bar when the *.indd is opened.
Window > Utilities > Script > run "Exportallstories" script.


Basically each text-box will lead to one txt file. Also, the extracted text has mixed
encoding issue. `tools/process_indd_converted_text.py` is used to handle that.

### Using process_indd_converted_text.py
```bash
cd ./tools
pip install -r requirements.txt
python process_indd_converted_text.py PATH_TO_INDD_TXT_DIR
```

`PATH_TO_INDD_TXT_DIR` is the path to direction that containing all those
extracted txt files from In-Design files. This script will look for all `.txt`
files in the this path recursively.

It will output `indd.train.txt` and `indd.test.txt`, which is the training text and 
test text. The default train-test ratio is 9:1, you could change it by specifying with `-s` options.


## Doing Fine-tuning

### Preparing the training text file and test text file
All the provided `.epub`, `.indd`, `.pdf`, `.pages` are converted to `.txt` files and put inside
`./dataset`. They are already splited in to train and test set. For example, `1.train.txt` and `1.test.txt`
are corresponding to the same book. For `7.train.txt` and `7.test.txt`, they are text from all provided *.indd files.

We will need to concatenate all training files to one file, and all the test files to one file.

```bash
cat ./dataset/*.train.txt > data.train.txt
cat ./dataset/*.test.txt > data.test.txt
```

### Install python library
```bash
# At project root
pip install -r requirements.txt
```

### Run the fine-tuning
```bash
python run_language_modeling.py \
    --output_dir=output \          # The trained model will be store at ./output
    --model_type=gpt2 \            # Tell huggingface transformers we want to train gpt-2
    --model_name_or_path=gpt2 \    # This will use the pre-trained gpt2 samll model
    --do_train \
    --train_data_file=data.train.txt \
    --do_eval \
    --eval_data_file=data.test.txt \
    --per_gpu_train_batch_size=1   # For GPU training only, you may increase it if your GPU has more memory to hold more training data.
```

For more options and the default value of the options, please refer to `run_language_modeling.py`

### Hyper-parameter search
`./hyper_param_search/run.py` is the script for trying different hyper-parameters in model fine-tuning.

The hyper-parameters that are going to explored are defined in `./hyper_param_search/config.py`.
You could see the range of each parameter there as well.

We are using random search for hyper-parameter searching, that is sample a set of hyper-parameters and 
use it to train a model, and keep repeating this util it reach the desired number of iteration.

```bash
cd ./hyper_param_search
echo "{}" > perplexities.json

python ./run.py \
  -n 100 \ # number of iteratioon
  -s 0 \ # seed used for sampling
  -k 20 \ #  number of the best-k model to keep
  ../data.train.txt \
  ../data.test.txt
```

The hyper-parameter search could take a long time, it is recommended to run on a machine
with GPU. You can keep track of its progress at `processed.txt`, when a new model is trained, 
its name will be appended to this file.
The model name is in the format of `{seed}_{iteration-index}`. And models are stored in `gpt2_outputs`.

`perplexities.json` will also updated during the search and showing the top-k models's name and their perplexity.

## Running Article Generation web server locally
### Prepare trained model
Before starting the server, please train a model first and on move the model 
directory (it should containing files like `config.json`) into `./web/models`.

### Running server locally
Make sure you have docker and docker-compose installed and run following.
You also need up install yarn
```bash
cd ./web
docker-compose -p article_generation up -d
cd frontend
yarn
yarn start 
```

You can tell access the article generator on http://localhost:8080/.

## Running jupyter notebooks

Two jupyter notebooks are prepare for interactively playing with the attention visualization
and word importance visualization.

To run the jupyter notebooks
```bash
# At project root, assume you have already run pip install
jupyter notebook
```

A browser should pop up and you can choose the `notebooks` folder and play with the notebook there.

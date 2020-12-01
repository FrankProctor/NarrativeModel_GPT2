import logging
import os.path
import gc
import functools

from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor

from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
)

logger = logging.getLogger(__name__)

MAX_LENGTH = int(10000)

ArticleGeneratorConfig = namedtuple(
    'ArticleGeneratorConfig',
    ['temperature', 'k', 'p', 'repetition_penalty'],
    defaults=[1.0, 0, 0.95, 1.0]
)


class ModelNotLoaded(Exception):
    pass


class ModelNotFound(Exception):
    pass


executor = ThreadPoolExecutor(max_workers=1)


def run_in_executor(fn):
    @functools.wraps(fn)
    def decorated(*args, **kwargs):
        f = executor.submit(fn, *args, **kwargs)
        return f.result()

    return decorated


class ArticleGenerator:

    device = "cpu"

    instance = None

    @staticmethod
    def get():
        if ArticleGenerator.instance is not None:
            return ArticleGenerator.instance

        ArticleGenerator.instance = ArticleGenerator()
        return ArticleGenerator.instance

    def __init__(self):
        self.model_class = GPT2LMHeadModel
        self.tokenizer_class = GPT2Tokenizer

        self.model = None
        self.tokenizer = None
        self.input_text_preprocessing_fn = None
        self.model_name = None

        # 1.0 has no effect, lower tend toward greedy sampling
        self.temperature = 1.0

        self.k = 0
        self.p = 0.9

        self.do_sample = True
        self.config = ArticleGeneratorConfig()

        self.tokens_to_end_with = [['.', '!', '?'], ',']

    @run_in_executor
    def load_model(self, path):
        if not os.path.isdir(path):
            raise ModelNotFound

        logger.info('Start to load model at {}...'.format(path))

        self.tokenizer = self.tokenizer_class.from_pretrained(path)
        self.model = self.model_class.from_pretrained(path)
        self.model.to(ArticleGenerator.device)

        gc.collect()

        self.model_name = path.split('/')[-1]

        logger.info('Done model loading.')

    @staticmethod
    def adjust_length_to_model(length, max_sequence_length):
        if length < 0 and max_sequence_length > 0:
            length = max_sequence_length
        elif 0 < max_sequence_length < length:
            # No generation bigger than model size
            length = max_sequence_length
        elif length < 0:
            # avoid infinite loop
            length = MAX_LENGTH
        return length

    def encode_input_text(self, input_text):
        if self.tokenizer is None or self.model is None:
            raise ModelNotLoaded

        if self.input_text_preprocessing_fn is not None:
            preprocessed_input_text = self.input_text_preprocessing_fn(
                self.config, self.model, self.tokenizer, input_text
            )

            return self.tokenizer.encode(
                preprocessed_input_text,
                add_special_tokens=False,
                return_tensors="pt",
                add_space_before_punct_symbol=True
            )

        return self.tokenizer.encode(
            input_text,
            add_special_tokens=False,
            return_tensors="pt",
            add_space_before_punct_symbol=True
        )

    def decode_output_sequence(self, sequence, encoded_input_first):
        if self.tokenizer is None:
            raise ModelNotLoaded

        sequence = sequence.tolist()

        text = self.tokenizer.decode(
            sequence,
            clean_up_tokenization_spaces=True)

        # Remove the excess text that was used for pre-processing
        return text[
            len(self.tokenizer.decode(
                encoded_input_first,
                clean_up_tokenization_spaces=True)):]

    @run_in_executor
    def generate(self, input_text, output_length=50,
                 num_return_sequences=1, should_trim_ending=True):
        if self.tokenizer is None or self.model is None:
            raise ModelNotLoaded

        encoded_input = self.encode_input_text(input_text)
        encoded_input.to(ArticleGenerator.device)

        max_length = (
            len(encoded_input[0]) +
            ArticleGenerator.adjust_length_to_model(
                output_length,
                max_sequence_length=self.model.config.max_position_embeddings)
        )

        output_sequences = self.model.generate(
            input_ids=encoded_input,
            max_length=max_length,
            temperature=self.config.temperature,
            top_k=self.config.k,
            top_p=self.config.p,
            repetition_penalty=self.config.repetition_penalty,
            do_sample=True,
            num_return_sequences=num_return_sequences,
            pad_token_id=self.model.config.eos_token_id,
        )

        if len(output_sequences.shape) > 2:
            output_sequences.squeeze_()

        post_decode = (
            self.trim_ending if should_trim_ending
            else lambda x: x
        )

        return [
            post_decode(self.decode_output_sequence(x, encoded_input[0]))
            for x in output_sequences
        ]

    def trim_ending(self, text):
        for token_to_end_with in self. tokens_to_end_with:
            index = None

            if isinstance(token_to_end_with, list):
                for t in token_to_end_with:
                    cur_index = text.rfind(t)
                    if index is None or cur_index > index:
                        index = cur_index
            else:
                index = text.rfind(token_to_end_with)

            if index is not None and index >= 0:
                return text[0:index + 1]

        return text

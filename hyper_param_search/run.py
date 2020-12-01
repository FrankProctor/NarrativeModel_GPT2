from config import enumerate_config
import click
import subprocess
import os
import os.path
import re
import json
from datetime import datetime

PERPLEXITY_LIST = './perplexities.json'
PROCESSED = './processed.txt'

WEB_SERVER_IP = '10.128.0.7'


@click.command()
@click.option(
    'num_iter', '--num-iter', '-n', type=int, default=100,
    help='Number of fine tuning to perform'
)
@click.option(
    'seed', '--seed', '-s', type=int, default=0,
    help='Random seed'
)
@click.option(
    'num_keep', '--keep', '-k', type=int, default=10,
    help='Keep best n model'
)
@click.option(
    'model', '--model', '-m',
    type=click.Choice(['gpt2', 'gpt2-medium']), default='gpt2',
    help='model to fine tune'
)
@click.option(
    'upload_model', '--upload',
    is_flag=True,
    help='Upload trained model with low perplexity to webserver'
)
@click.argument(
    'train_file_path',
    type=click.Path(exists=True, file_okay=True))
@click.argument(
    'eval_file_path',
    type=click.Path(exists=True, file_okay=True))
def main(num_iter, seed, num_keep, model, upload_model,
         train_file_path, eval_file_path):

    os.makedirs('./{}_outputs', exist_ok=True)

    for index, config in enumerate_config(num_iter, seed=seed):
        output_dir = './{}_outputs/{}_{}'.format(model, seed, index)
        if not is_config_run_before(seed, index):
            execute_training(
                config,
                output_dir,
                model,
                train_file_path,
                eval_file_path)

            perplexity = get_perplexity(output_dir)
            print('perplexity: {}'.format(perplexity))
            is_updated, model_to_remove = update_result(
                seed, index, perplexity, num_keep)
            if not is_updated:
                os.system('rm -rf {}'.format(output_dir))
            else:
                hyper_params_path = os.path.join(
                    output_dir, 'hyper_params.json')
                with open(hyper_params_path, 'w') as fp:
                    json.dump(config, fp, indent=4)

            if model_to_remove is not None:
                os.system(
                    'rm -rf ./{}_outputs/{}'.format(model, model_to_remove))

            os.system('echo {}_{} >> {}'.format(seed, index, PROCESSED))

            if perplexity < 30 and upload_model:
                print('Uploading model to webserver...')
                os.system(
                    'scp -r {} oursky@{}:~/models/'.format(
                        output_dir, WEB_SERVER_IP))

        else:
            print('skip seed:{} index:{}'.format(seed, index))


def is_config_run_before(seed, index):
    key = '{}_{}'.format(seed, index)

    if not os.path.exists(PROCESSED):
        return False

    with open(PROCESSED, 'r') as fp:
        for line in fp.readlines():
            if line.strip() == key:
                return True

    return False


def get_perplexity(output_dir):
    if not os.path.exists(os.path.join(output_dir, 'eval_results.txt')):
        return None

    pattern = r'perplexity = tensor\(([0-9.]+)\)'

    with open(os.path.join(output_dir, 'eval_results.txt'), 'r') as fp:
        line = fp.read().strip()
        matches = re.match(pattern, line)

    return float(matches.group(1))


def update_result(seed, index, perplexity, num_keep):

    is_updated = False
    model_to_remove = None
    with open(PERPLEXITY_LIST, 'r') as fp:
        perplexity_list = json.load(fp)

    if len(perplexity_list) < num_keep:
        key = '{}_{}'.format(seed, index)
        perplexity_list[key] = perplexity
        is_updated = True
    else:
        key_with_highest_perplexity = [
            k for k,
            v in sorted(perplexity_list.items(), key=lambda x: - x[1])
        ][0]

        if perplexity_list[key_with_highest_perplexity] > perplexity:
            del perplexity_list[key_with_highest_perplexity]
            model_to_remove = key_with_highest_perplexity
            key = '{}_{}'.format(seed, index)
            perplexity_list[key] = perplexity
            is_updated = True

    if is_updated:
        with open(PERPLEXITY_LIST, 'w') as fp:
            json.dump(perplexity_list, fp, indent=4)

    return is_updated, model_to_remove


def execute_training(config, output_dir, model,
                     train_file_path, eval_file_path):
    commands = [
        'python', '../run_language_modeling.py',
        '--output_dir={}'.format(output_dir),
        '--model_type=gpt2',
        *['--{}={}'.format(k, v) for k, v in config.items()],
        '--model_name_or_path={}'.format(model),
        '--save_total_limit=1',
        '--save_steps=5000',
        '--per_gpu_train_batch_size={}'.format(2 if model == 'gpt2' else 1),
        '--overwrite_output_dir',
        '--do_train',
        '--train_data_file={}'.format(train_file_path),
        '--do_eval',
        '--eval_data_file={}'.format(eval_file_path),
    ]

    print("[{}] Training {} ...".format(datetime.now(), output_dir))

    subprocess.call(
        commands,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


if __name__ == '__main__':
    main()

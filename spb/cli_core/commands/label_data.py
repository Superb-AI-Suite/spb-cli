import os
import click
import json
import logging
import rich
import rich.table
import rich.console
import rich.logging
import math
from multiprocessing import Process, Manager, Pool
import tqdm
import requests
from collections import ChainMap

import spb
from spb.cli_core.utils import recursive_glob_image_files, recursive_glob_label_files
from spb.models.label import Label

console = rich.console.Console()

NUM_MULTI_PROCESS = 4
LABEL_DESCRIBE_PAGE_SIZE = 10


class LabelData():

    def upload_data(self, project, dataset_name, directory_path, include_label):
        spb.client()
        imgs_path = recursive_glob_image_files(directory_path)
        if not click.confirm(f"Uploading {len(imgs_path)} data and {len(recursive_glob_label_files(directory_path)) if include_label else 0 } labels to dataset '{dataset_name}' under project '{project.name}'. Proceed?"):
                return
        asset_images = []
        for key in imgs_path:
            file_name = key
            asset_image = {
                'file': imgs_path[key],
                'file_name': file_name,
                'data_key': key,
                'dataset': dataset_name
            }
            asset_images.append(asset_image)
        manager = Manager()
        data_results = manager.list([manager.dict()]*len(asset_images))
        console.print(f"Uploading data:")
        with Pool(NUM_MULTI_PROCESS) as p:
            list(tqdm.tqdm(p.imap(_upload_asset, zip([project.id] * len(asset_images), asset_images, data_results)), total=len(asset_images)))

        label_results = None
        if include_label:
            labels_path = recursive_glob_label_files(directory_path)
            console.print(f"Uploading labels:")
            label_results = manager.list([manager.dict()]*len(labels_path))
            with Pool(NUM_MULTI_PROCESS) as p:
                list(tqdm.tqdm(p.imap(_update_label, zip(labels_path, [project.id]*len(labels_path), [dataset_name]*len(labels_path), label_results)), total=len(labels_path)))

        console.print('\n[b blue]** Result Summary **[/b blue]')
        success_data_count = len(asset_images) - len(data_results[0])
        console.print(f'Successful upload of {success_data_count} out of {len(asset_images)} data. ({round(success_data_count/len(asset_images)*100,2)}%) - [b red]{len(data_results[0])} ERRORS[/b red]')

        if include_label:
            success_label_count=len(labels_path)-len(label_results[0])
            console.print(f'Successful upload of {success_label_count} out of {len(labels_path)} labels. ({round(success_label_count/len(labels_path)*100,2)}%) - [b red]{len(label_results[0])} ERRORS[/b red]')
            self._print_error_table(dict(data_results[0]), dict(label_results[0]))
        else:
            self._print_error_table(data_results=dict(data_results[0]))

    def upload_label(self, project, dataset_name, directory_path):
        labels_path = recursive_glob_label_files(directory_path)
        if not click.confirm(f"Uploading {len(labels_path)} labels to project '{project.name}'. Proceed?"):
            return

        manager = Manager()
        label_results = manager.list([manager.dict()]*len(labels_path))
        with Pool(NUM_MULTI_PROCESS) as p:
            list(tqdm.tqdm(p.imap(_update_label, zip(labels_path, [project.id]*len(labels_path), [dataset_name]*len(labels_path), label_results)), total=len(labels_path)))

        console.print('\n[b blue]** Result Summary **[/b blue]')
        success_label_count=len(labels_path)-len(label_results[0])
        console.print(f'Successful upload of {success_label_count} out of {len(labels_path)} labels. ({round(success_label_count/len(labels_path)*100,2)}%) - [b red]{len(label_results[0])} ERRORS[/b red]')

        self._print_error_table(label_results=label_results[0])

    def download(self, project, directory_path):
        command = spb.Command(type='describe_label')
        _, label_count = spb.run(command=command, option={
            'project_id' : project.id
        }, page_size = 1, page = 1)

        page_length = int(label_count/LABEL_DESCRIBE_PAGE_SIZE) if label_count % LABEL_DESCRIBE_PAGE_SIZE == 0 else int(label_count/LABEL_DESCRIBE_PAGE_SIZE)+1

        if not click.confirm(f"Downloading {label_count} data and {label_count} labels from project '{project.name}' to '{directory_path}'. Proceed?"):
            return
        manager = Manager()
        results = manager.list([manager.dict()]*page_length)
        with Pool(NUM_MULTI_PROCESS) as p:
            list(tqdm.tqdm(p.imap(_download_worker, zip([project.id] * page_length, range(page_length), [directory_path] * page_length, results)), total=page_length))

        results = results[0]
        data_results = {}
        label_results = {}
        if len(results) > 0:
            for key in results.keys():
                if 'data' in results[key]:
                    data_results[key] = results[key]['data']
                if 'label' in results[key]:
                    label_results[key] = results[key]['label']

        console.print('\n[b blue]** Result Summary **[/b blue]')
        label_success_count = label_count - len(label_results)
        console.print(f'Successful download of {label_success_count} out of {label_count} labels. ({round(label_success_count/label_count*100,2)}%) - [b red]{len(label_results)} ERRORS[/b red]')
        data_success_count = label_count - len(data_results)
        console.print(f'Successful download of {data_success_count} out of {label_count} data. ({round(data_success_count/label_count*100,2)}%) - [b red]{len(data_results)} ERRORS[/b red]')

        self._print_error_table(label_results=label_results, data_results=data_results)

    def _print_error_table(self, data_results = None, label_results = None):
        results = {}

        if isinstance(data_results, dict):
            for key in data_results:
                results[key] = {}
                results[key]['data'] = data_results[key]
                results[key]['label'] = None

        if isinstance(label_results, dict):
            for key in label_results:
                if key in results:
                    results[key]['label'] = label_results[key]
                else:
                    results[key] = {'label':label_results[key], 'data':None}

        if not next(iter(results), None):
                return
        console.print('\n[b red]** Error Table **[/b red]')
        page = 1
        page_length = math.ceil(len(results)/10)
        while True:
            table = rich.table.Table(show_header=True, header_style="bold magenta")
            table.add_column("FILE NAME")
            if isinstance(data_results, dict):
                table.add_column("DATA UPLOAD")
            if isinstance(label_results, dict):
                table.add_column("LABEL UPLOAD")

            for _ in range(10):
                key = next(iter(results), None)
                if not key:
                    break
                if isinstance(data_results, dict) and isinstance(label_results, dict):
                    data = results[key]['data']
                    label = results[key]['label']
                    table.add_row(key, f"{data if data else '-'}", f"{label if label else '-'}")
                elif isinstance(data_results, dict):
                    data = results[key]['data']
                    table.add_row(key, f"{data if data else '-'}")
                else:
                    label = results[key]['label']
                    table.add_row(key, f"{label if label else '-'}")
                del results[key]
            console.print(table)
            if not next(iter(results), None):
                break
            else:
                click.echo(f'Press any button to continue to the next page ({page}/{page_length}). Otherwise press ‘Q’ to quit.', nl=False)
                key = click.getchar()
                click.echo()
                if key=='q' or key=='Q':
                    return


def _download_worker(args):
    [project_id, page_idx, directory_path, result] = args
    command = spb.Command(type='describe_label')
    labels, _ = spb.run(command=command, option={
        'project_id' : project_id
    }, page_size = LABEL_DESCRIBE_PAGE_SIZE, page = page_idx + 1)
    for label in labels:
        error = {}
        path = label.dataset + label.data_key if label.data_key.find('/') != -1 else label.dataset + "/"+label.data_key
        path = f"{directory_path}/{path}"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            label_json_path = f'{path}.json'
            open(label_json_path, 'w').write(label.toJson())
        except Exception as e:
            error = {'label':str(e)}
        try:
            data_url = label.data_url
            path = f'{path}'
            r = requests.get(data_url, allow_redirects=True)
            open(path, 'wb').write(r.content)
        except:
            error.update({'data':str(e)})

        if len(error) > 0:
            result[f'{label.dataset}/{label.data_key}'] = error


def _upload_asset(args):
    logging.debug(f'Uploading Asset: {args}')

    [project_id, asset_image, result] = args
    try:
        command = spb.Command(type='create_data')
        spb.run(command=command, option=asset_image, optional={'projectId': project_id})
    except Exception as e:
        logging.info(f'Failed to Upload Asset: {args}')
        result[asset_image['data_key']] = e.message
        pass


def _update_label(args):
    [label_path, project_id, dataset, result] = args
    data_key = ".".join(label_path.split(".")[:-1])
    if not os.path.isfile(label_path):
        result[data_key] = 'Label json file is not existed.'
        return

    option = {
        'project_id': project_id,
        'dataset': dataset,
        'data_key': data_key
    }
    command = spb.Command(type='describe_label')
    described_labels, _ = spb.run(command=command, option=option, page_size=1, page=1)
    described_label = described_labels[0] if described_labels and described_labels[0] else None
    if described_label is None:
        result[data_key] = 'Label cannot be described.'
        return
    if described_label.data_key != option['data_key'] and described_label.dataset != option['dataset']:
        result[data_key] = 'Described label does not match to upload.'
        return

    label = {
        "id": described_label.id,
        "project_id": project_id,
        "data_key": described_label.data_key,
        "dataset": dataset,
        "result": described_label.result,
    }
    try:
        with open(label_path) as json_file:
            json_data = json.load(json_file)
        if json_data['result'] is None:
            return
        label['result'] = json_data['result']
        command = spb.Command(type='update_label')
        label = spb.run(command=command, option=label)
        with open(label_path, 'w') as f:
            f.write(label.toJson())
        result = True
    except Exception as e:
        result[data_key] = e.message


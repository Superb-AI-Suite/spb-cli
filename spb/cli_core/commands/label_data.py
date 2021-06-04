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
from spb.labels import Label
from spb.labels.label import Tags
from spb.labels.serializer import LabelInfoBuildParams
from spb.labels.manager import LabelManager
from spb.labels.label import WorkappType

console = rich.console.Console()
logger = logging.getLogger()
simple_logger = logging.getLogger('simple')
NUM_MULTI_PROCESS = 4
LABEL_DESCRIBE_PAGE_SIZE = 10


class LabelData():

    def __init__(self):
        self.label_manager = LabelManager()

    def upload_data(self, project, dataset_name, directory_path, include_label, is_forced):
        imgs_path = recursive_glob_image_files(directory_path)
        if not is_forced:
            if not click.confirm(f"Uploading {len(imgs_path)} data and {len(recursive_glob_label_files(directory_path)) if include_label else 0 } labels to dataset '{dataset_name}' under project '{project.name}'. Proceed?"):
                    return
        asset_images = []
        manager = Manager()
        if len(imgs_path) != 0:
            for key in imgs_path:
                file_name = key
                asset_image = {
                    'file': imgs_path[key],
                    'file_name': file_name,
                    'data_key': key,
                    'dataset': dataset_name
                }
                asset_images.append(asset_image)
            data_results = manager.list([manager.dict()]*len(asset_images))
            console.print(f"Uploading data:")
            with Pool(NUM_MULTI_PROCESS) as p:
                list(tqdm.tqdm(p.imap(_upload_asset, zip([project.id] * len(asset_images), asset_images, data_results)), total=len(asset_images)))
        else:
            data_results = [{}]

        label_results = None
        if include_label:
            labels_path = recursive_glob_label_files(directory_path)
            console.print(f"Uploading labels:")
            if len(labels_path) != 0:
                label_results = manager.list([manager.dict()]*len(labels_path))
                with Pool(NUM_MULTI_PROCESS) as p:
                    list(tqdm.tqdm(p.imap(_update_label, zip([self.label_manager]*len(labels_path), labels_path, [project.id]*len(labels_path), [project.label_interface]*len(labels_path), [dataset_name]*len(labels_path), label_results)), total=len(labels_path)))
            else:
                label_results = [{}]

        console.print('\n[b blue]** Result Summary **[/b blue]')
        success_data_count = len(asset_images) - len(data_results[0])
        data_success_ratio = round(success_data_count/len(asset_images)*100,2) if len(data_results[0]) != 0 else 100
        console.print(f'Successful upload of {success_data_count} out of {len(asset_images)} data. ({data_success_ratio}%) - [b red]{len(data_results[0])} ERRORS[/b red]')

        if include_label:
            success_label_count=len(labels_path)-len(label_results[0])
            label_success_ratio = round(success_label_count/len(labels_path)*100,2) if len(label_results[0]) != 0 else 100
            console.print(f'Successful upload of {success_label_count} out of {len(labels_path)} labels. ({label_success_ratio}%) - [b red]{len(label_results[0])} ERRORS[/b red]')
            self._print_error_table(data_error_results=dict(data_results[0]), label_error_results=dict(label_results[0]))
        else:
            self._print_error_table(data_error_results=dict(data_results[0]))

    def upload_label(self, project, dataset_name, directory_path, is_forced):
        labels_path = recursive_glob_label_files(directory_path)
        if not is_forced:
            if not click.confirm(f"Uploading {len(labels_path)} labels to project '{project.name}'. Proceed?"):
                return
        if len(labels_path) != 0:
            manager = Manager()
            label_results = manager.list([manager.dict()]*len(labels_path))
            with Pool(NUM_MULTI_PROCESS) as p:
                list(tqdm.tqdm(p.imap(_update_label, zip([self.label_manager]* len(labels_path), labels_path, [project.id]*len(labels_path), [project.label_interface]*len(labels_path), [dataset_name]*len(labels_path), label_results)), total=len(labels_path)))
        else:
            label_results = [{}]

        console.print('\n[b blue]** Result Summary **[/b blue]')
        success_label_count=len(labels_path)-len(label_results[0])
        success_label_ratio = round(success_label_count/len(labels_path)*100,2) if len(labels_path) != 0 else 100
        console.print(f'Successful upload of {success_label_count} out of {len(labels_path)} labels. ({success_label_ratio}%) - [b red]{len(label_results[0])} ERRORS[/b red]')

        self._print_error_table(label_error_results=dict(label_results[0]))

    def download(self, project, directory_path, is_forced):
        process_results = []
        success_data_count = 0
        success_labels_count = 0
        data_error_results = {}
        label_error_results = {}
        # get data count
        main_label_count, labels = self.label_manager.get_labels(project.id, label_type='DEFAULT', page=1, page_size=1)
        # get labels count
        total_label_count, labels = self.label_manager.get_labels(project.id, page=1, page_size=1)

        #Download project configuration
        try:
            project_config_path = os.path.join(directory_path, 'project.json')
            with open(project_config_path, 'w') as input:
                json.dump(project.label_interface, input, indent=4)
            is_download_project_config = True
        except Exception as e:
            is_download_project_config = False

        if main_label_count != 0:
            page_length = int(main_label_count/LABEL_DESCRIBE_PAGE_SIZE) if main_label_count % LABEL_DESCRIBE_PAGE_SIZE == 0 else int(main_label_count/LABEL_DESCRIBE_PAGE_SIZE)+1
            if not is_forced:
                if not click.confirm(f"Downloading {main_label_count} data and {total_label_count} labels from project '{project.name}' to '{directory_path}'. Proceed?"):
                    return
            manager = Manager()
            label_results_dict = manager.dict()
            label_results = manager.list([label_results_dict]*page_length)
            process_results = manager.list(range(page_length))
            with Pool(NUM_MULTI_PROCESS) as p:
                list(tqdm.tqdm(p.imap(_download_worker, zip([self.label_manager]* page_length, [project.id] * page_length, range(page_length), [directory_path] * page_length, label_results, [process_results] * page_length)), total=page_length))

            for key in label_results_dict.keys():
                results_error = label_results_dict[key]['error']
                success_data_count += 1
                success_labels_count += label_results_dict[key]['success_labels_count']
                if 'data' in results_error:
                    data_error_results[key] = results_error['data']
                if 'label' in results_error:
                    label_error_results[key] = results_error['label']


        console.print('\n[b blue]** Result Summary **[/b blue]')
        console.print(f'Download of project configuration - {"[b blue]Success[/b blue]" if is_download_project_config else "[b red]Fail[/b red]"}')
        console.print(f'Successful download of {success_labels_count} out of {total_label_count} labels. ({round(success_labels_count/total_label_count*100,2)}%) - [b red]{total_label_count - success_labels_count} ERRORS[/b red]')
        console.print(f'Successful download of {success_data_count} out of {main_label_count} data. ({round(success_data_count/main_label_count*100,2)}%) - [b red]{main_label_count - success_data_count} ERRORS[/b red]')

        # TODO: Need to refactor Get Labels API Fail Logic
        for process_result in process_results:
            is_process_fail = False
            if not process_result:
                is_process_fail = True
        if is_process_fail:
            console.print(f'[b red]Failed Download Labels from API. Please retry download.[/b red]')

        self._print_error_table(data_error_results=data_error_results, label_error_results=label_error_results, )

    def _print_error_table(self, data_error_results = None, label_error_results = None):
        results = {}

        if isinstance(data_error_results, dict):
            for key in data_error_results:
                results[key] = {}
                results[key]['data'] = data_error_results[key]
                results[key]['label'] = None
        if isinstance(label_error_results, dict):
            for key in label_error_results:
                if key in results:
                    results[key]['label'] = label_error_results[key]
                else:
                    results[key] = {'label':label_error_results[key], 'data':None}

        if not next(iter(results), None):
                return
        console.print('\n[b red]** Error Table **[/b red]')
        page = 1
        page_length = math.ceil(len(results)/10)
        while True:
            table = rich.table.Table(show_header=True, header_style="bold magenta")
            table.add_column("FILE NAME")
            if isinstance(data_error_results, dict):
                table.add_column("DATA UPLOAD")
            if isinstance(label_error_results, dict):
                table.add_column("LABEL UPLOAD")

            for _ in range(10):
                key = next(iter(results), None)
                if not key:
                    break
                if isinstance(data_error_results, dict) and isinstance(label_error_results, dict):
                    data = results[key]['data']
                    label = results[key]['label']
                    table.add_row(key, f"{data if data else '-'}", f"{label if label else '-'}")
                elif isinstance(data_error_results, dict):
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
                    break
        console.log(f'[b]Check the log file for more details[/b]')
        console.log(f'- {simple_logger.handlers[0].baseFilename}')
        console.log(f'- {logger.handlers[0].baseFilename}')



def _download_worker(args):
    [label_manager, project_id, page_idx, directory_path, label_results_dict, process_results] = args
    # command = spb.Command(type='describe_label')
    # labels, _ = spb.run(command=command, option={
    #     'project_id' : project_id
    # }, page_size = LABEL_DESCRIBE_PAGE_SIZE, page = page_idx + 1)
    labels = []
    try:
        label_count, labels = label_manager.get_labels(project_id, label_type='DEFAULT', page=page_idx + 1, page_size=LABEL_DESCRIBE_PAGE_SIZE)
    except Exception as e:
        process_results[page_idx] = False
        # error = {'label':str(e)}
        # _set_error_result(f'Failed Get Labels', dict(), str(error), error)
        return
    
    for label in labels:
        success_labels_count = 0
        error = {}
        path = os.path.join(label.dataset, label.data_key[1:]) if label.data_key.startswith('/') else os.path.join(label.dataset, label.data_key)
        path = os.path.join(directory_path, path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        label_error = None
        data_error = None
        label_info = label.to_json()
        if label.label_type=="MAIN_LABEL" and label.consensus_status=="CREATED":
            related_label_count, related_labels = label_manager.get_related_labels_by_label(project_id, label.id)
            label_info['related_labels_info'] = {
                'related_labels_count': related_label_count
            }
            label_info['related_labels'] = {
                'consensus_labeling' : [ related_label.to_json(include_project=False, include_data=False) for related_label in related_labels]
            }
            label_info['id'] = None
            label_info['status'] = None
            label_info['work_assignee'] = None
            label_info['consensus_status'] = None
            label_info['consistency_score'] = None
            label_info['stats'] = None
            label_info['tags'] = []
            label_info['result'] = None
            label_info['created_by'] = None
            label_info['created_at'] = None
            label_info['last_updated_by'] = None
            label_info['last_updated_at'] = None
            success_labels_count += related_label_count
        elif label.label_type=="MAIN_LABEL" and label.consensus_status=="QUALIFIED":
            related_label_count, related_labels = label_manager.get_related_labels_by_label(project_id, label.id)
            label_info['related_labels_info'] = {
                'related_labels_count': related_label_count
            }
            label_info['related_labels'] = {
                'consensus_labeling' : [ related_label.to_json(include_project=False, include_data=False) for related_label in related_labels]
            }
            success_labels_count += (related_label_count+1)
        elif label.label_type=="MAIN_LABEL" and label.consensus_status=="":
            success_labels_count += 1

        try:
            label_json_path = f'{path}.json'
            with open(label_json_path, 'w') as input:
                json.dump(label_info, input, indent=4)
        except Exception as e:
            error = {'label':str(e)}
            label_error = error
        try:
            data_url = label.data_url
            path = f'{path}'
            r = requests.get(data_url, allow_redirects=True)
            open(path, 'wb').write(r.content)
        except Exception as e:
            error.update({'data':str(e)})
            data_error = error

        label_results_dict[f'{label.dataset}/{label.data_key}'] = {"error": error, "success_labels_count":success_labels_count}
        if len(error) > 0:
            if label_error:
                _ = dict()
                _set_error_result(f'{label.dataset}/{label.data_key}', _, str(label_error), label_error)
            if data_error:
                _ = dict()
                _set_error_result(f'{label.dataset}/{label.data_key}', _, str(data_error), data_error)
    process_results[page_idx] = True


def _upload_asset(args):
    logging.debug(f'Uploading Asset: {args}')

    [project_id, asset_image, result] = args
    try:
        command = spb.Command(type='create_data')
        spb.run(command=command, option=asset_image, optional={'projectId': project_id})
    except Exception as e:
        _set_error_result(asset_image['data_key'], result, str(e), e)
        pass


def _update_label(args):
    [label_manager, label_path, project_id, label_interface, dataset, result] = args
    data_key = ".".join(label_path.split(".")[:-1])
    if not os.path.isfile(label_path):
        _set_error_result(data_key, result, 'Label json file is not existed.')
        return

    # option = {
    #     'project_id': project_id,
    #     'dataset': dataset,
    #     'data_key': data_key
    # }
    try:
        # command = spb.Command(type='describe_label')
        # described_labels, _ = spb.run(command=command, option=option, page_size=1, page=1)
        label_count, labels = label_manager.get_labels(project_id, label_type='DEFAULT', page=1, page_size=1, dataset=dataset, data_key=data_key)
        described_label = labels[0] if label_count > 0 else None
        if described_label is None:
            _set_error_result(data_key, result, 'Label cannot be described.')
            return
        if described_label.data_key != data_key and described_label.dataset != dataset:
            _set_error_result(data_key, result, 'Described label does not match to upload.')
            return
    except Exception as e:
        _set_error_result(data_key, result, str(e), e)
        return
    update_tags = [Tags.get_data(tag) for tag in described_label.tags]
    update_result = described_label.result
    try:
        with open(label_path) as json_file:
            json_data = json.load(json_file)
        if json_data['result'] is None:
            return
        info_build_params = None
        described_label.result = json_data['result']
        if described_label.workapp == WorkappType.IMAGE_SIESTA.value:
            info_build_params = LabelInfoBuildParams(
                label_interface = label_interface,
                result = json_data['result']
            )
        updated_label = label_manager.update_label(info_build_params = info_build_params, label=described_label)
        updated_label_info = updated_label.to_json()
        if updated_label.label_type=="MAIN_LABEL" and updated_label.consensus_status=="CREATED":
            related_label_count, related_labels = label_manager.get_related_labels_by_label(project_id, updated_label.id)
            updated_label_info['related_labels_info'] = {
                'related_labels_count': related_label_count
            }
            updated_label_info['related_labels'] = {
                'consensus_labeling' : [ related_label.to_json(include_project=False, include_data=False) for related_label in related_labels]
            }
            updated_label_info['id'] = None
            updated_label_info['status'] = None
            updated_label_info['work_assignee'] = None
            updated_label_info['consensus_status'] = None
            updated_label_info['consistency_score'] = None
            updated_label_info['stats'] = None
            updated_label_info['tags'] = []
            updated_label_info['result'] = None
            updated_label_info['created_by'] = None
            updated_label_info['created_at'] = None
            updated_label_info['last_updated_by'] = None
            updated_label_info['last_updated_at'] = None
        elif updated_label.label_type=="MAIN_LABEL" and updated_label.consensus_status=="QUALIFIED":
            related_label_count, related_labels = label_manager.get_related_labels_by_label(project_id, updated_label.id)
            updated_label_info['related_labels_info'] = {
                'related_labels_count': related_label_count
            }
            updated_label_info['related_labels'] = {
                'consensus_labeling' : [ related_label.to_json(include_project=False, include_data=False) for related_label in related_labels]
            }
        with open(label_path, 'w') as input:
            json.dump(updated_label_info, input, indent=4)
    except Exception as e:
        _set_error_result(data_key, result, str(e), e)

def _set_error_result(key, result, message, exception=None):
    result[key] = message
    simple_logger.error(f'{key}    {message}')
    if exception:
        logger.error(f'{key}    {message}')
        logger.error(exception, exc_info=True)
    else:
        logger.error(f'{key}    {message}')
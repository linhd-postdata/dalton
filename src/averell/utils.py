import json
import logging
import os
import urllib.request
from pathlib import Path
from zipfile import ZipFile

import yaml
from tqdm import tqdm

BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
with open(BASE_DIR / 'corpora.yaml', 'r') as config_file:
    CORPORA_SOURCES = yaml.load(config_file, Loader=yaml.FullLoader)

DEFAULT_OUTPUT_FOLDER = Path.cwd() / "corpora"

TEI_NAMESPACE = "{http://www.tei-c.org/ns/1.0}"


def progress_bar(t):
    """ from https://gist.github.com/leimao/37ff6e990b3226c2c9670a2cd1e4a6f5
    Wraps tqdm instance.
    Don't forget to close() or __exit__() the tqdm instance once you're done
    (easiest using `with` syntax).
    Example:
        with tqdm(...) as t:
             reporthook = my_hook(t)
             urllib.urlretrieve(..., reporthook=reporthook)
    """
    last_b = [0]

    def update_to(b=1, bsize=1, tsize=None):
        """
        :param b: int, optional
            Number of blocks transferred so far [default: 1].
        :param bsize: int, optional
            Size of each block (in tqdm units) [default: 1].
        :param tsize: int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            t.total = tsize
        t.update((b - last_b[0]) * bsize)
        last_b[0] = b

    return update_to


def download_corpus(url):
    """
    Function to download the corpus zip file from external source
    :param url: string
        URL of the corpus file
    :return: string
        Local filename of the corpus
    """
    filename = url.split('/')[-1]
    with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=filename) as t:
        filename, *_ = urllib.request.urlretrieve(url, reporthook=progress_bar(t))
    return filename


def uncompress_corpus(filename, save_dir):
    """
    Simple function to uncompress the corpus zip file
    :param filename: string
        The file that is going to be uncompressed
    :param save_dir: string
        The folder where the corpus is going to be uncompressed
    :return: string
        Filename of uncompressed corpus
    """""
    with ZipFile(filename, 'r') as zipObj:
        zipObj.extractall(save_dir)
    os.remove(filename)
    return filename


def download_corpora(corpus_indices=None,
                     output_folder=DEFAULT_OUTPUT_FOLDER):
    """
    Download corpus from a list of sources to a local folder
    :param corpus_indices: list
        List with the indexes of CORPORA_SOURCES to choose which corpus
        is going to be downloaded
    :param output_folder: string
        The folder where the corpus is going to be saved
    """
    folder_list = []
    if corpus_indices:
        for index in tqdm(corpus_indices):
            try:
                folder_name = CORPORA_SOURCES[index]["properties"]["folder_name"]
                folder_path = Path(output_folder) / folder_name
                if folder_path.exists():
                    logging.info(
                        f'Corpus {CORPORA_SOURCES[index]["name"]}'
                        f' already downloaded')
                    continue
                else:
                    url = CORPORA_SOURCES[index]["properties"]["url"]
                    filename = download_corpus(url)
                    folder_list.append(uncompress_corpus(filename, output_folder))
            except IndexError:
                logging.error("Index number not in corpora list")
                return "Error"
    else:
        logging.error("No corpus selected. Nothing will be downloaded")
    return folder_list


def get_stanza_features(poem_features):
    """
    Filter the stanza features of a poem
    :param poem_features: dict
        Poem dictionary
    :return: dict list
        Stanzas dict list
    """
    stanza_list = []
    for stanza_index, key in enumerate(poem_features["stanzas"]):
        stanza_features = poem_features['stanzas'][stanza_index]
        dic_final = {
            'stanza_number': stanza_features['stanza_number'],
            'manually_checked': poem_features['manually_checked'],
            'poem_title': poem_features['poem_title'],
            'author': poem_features['author'],
            'stanza_text': stanza_features['stanza_text'],
            'stanza_type': stanza_features['stanza_type']
        }
        stanza_list.append(dic_final)
    return stanza_list


def get_line_features(features):
    """
    Filter the line features of a poem
    :param features: dict
        Poem dictionary
    :return: dict list
        Lines dict list
    """
    stanza_features = get_stanza_features(features)
    lines_features = []
    for stanza_index, stanza in enumerate(stanza_features):
        key = features["stanzas"][stanza_index]
        for line in key["lines"]:
            line_features = {}
            if not line.get("words"):
                line_features.update(line)
            else:
                line_features['line_number'] = line['line_number']
                line_features['line_text'] = line['line_text']
                line_features['metrical_pattern'] = line['metrical_pattern']
            lines_features.append({**line_features, **stanza})
    return lines_features


def get_word_features(features):
    """
    Filter the word features of a poem
    :param features: dict
        Poem dictionary
    :return: dict list
        Words dict list
    """
    all_lines_features = get_line_features(features)
    all_words_features = []
    for stanza_index, stanza in enumerate(features["stanzas"]):
        lines = stanza["lines"]
        for line in lines:
            line_number = int(line["line_number"])
            for word in line["words"]:
                word_features = {"word_text": word["word_text"]}
                line_features = all_lines_features[line_number - 1]
                word_features.update(line_features)
                word_features.pop("stanza_text")
                all_words_features.append(word_features)
    return all_words_features


def get_syllable_features(features):
    """
    Filter the syllable features of a poem
    :param features: dict
        Poem dictionary
    :return: dict list
        Syllables dict list
    """
    all_words_features = get_word_features(features)
    all_syllable_features = []
    word_number = 0
    for stanza_index, stanza in enumerate(features["stanzas"]):
        lines = stanza["lines"]
        for line in lines:
            line_number = int(line["line_number"])
            words = line["words"]
            for word_index, word in enumerate(words):
                syllables = word["syllables"]
                for syllable in syllables:
                    syllable_features = {
                        "syllable": syllable,
                        "line_number": line_number,
                    }
                    word_features = all_words_features[word_number]
                    syllable_features.update(word_features)
                    all_syllable_features.append(syllable_features)
                word_number += 1
    return all_syllable_features


def filter_features(features, corpus_index, granularity=None):
    """
    Select the granularity
    :param features: dict
        Corpora poems dict
    :param corpus_index: int
        Corpus index to be filtered
    :param granularity: string
        Level to filter the poem (stanza, line, word or syllable)
    :return: list
        List of rows with the granularity info
    """
    filtered_features = []
    granularities_list = CORPORA_SOURCES[corpus_index]["properties"][
        "granularity"]
    if granularity in granularities_list:
        if granularity == "stanza":
            filtered_features = get_stanza_features(features)
        elif granularity == "line":
            filtered_features = get_line_features(features)
        elif granularity == "word":
            filtered_features = get_word_features(features)
        elif granularity == "syllable":
            filtered_features = get_syllable_features(features)
    return filtered_features


def write_json(poem_dict, filename):
    """
    Simple function to save data in json format
    :param poem_dict: dict
        Python dict with poem data
    :param filename: string
        JSON filename that will be written with the poem data
    :return:
    """
    with open(filename + ".json", 'w', encoding='utf-8') as f:
        json.dump(poem_dict, f, ensure_ascii=False, indent=4)

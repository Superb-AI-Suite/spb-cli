import spb
from spb.models import Data
from spb.orm.utils import is_data_url, is_url

dummy_data = {
  'id': None,
  'file': None,
  'file_name': 'file_name.jpg',
  'data_key': 'data_key',
  'dataset': 'dataset'
}

file_path = {'file': './tests/unit/model/asdf.png'}

def test_data_model():
    print('------------ Data Model with file path ------------')
    dummy_data.update(file_path)
    data = Data(dummy_data)
    print(data)
    assert is_data_url(data.file)


if __name__ == '__main__':
    test_data_model()

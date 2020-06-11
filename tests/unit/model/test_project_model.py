import spb
from spb.models import Project

dummy_project = {
    'id': 'dummy_project_id',
    'name': 'Special Day',
    'label_count': 100,
    'summary': {
        'dataType': 'image',
        'objectDetection': {
            'annotationTypes': [
                'box',
                'polyline',
                'polygon',
                'keypoint'
            ],
            'objectClasses': [
                {
                    'name': 'car',
                    'color': '#FF625A',
                    'annotationType': 'box'
                },
                {
                    'name': 'road',
                    'color': '#F89400',
                    'annotationType': 'polyline'
                },
                {
                    'name': 'tree',
                    'color': '#FFCC00',
                    'annotationType': 'polygon'
                },
                {
                    'name': 'face',
                    'color': '#A3EB57',
                    'annotationType': 'keypoint',
                    'keypointName': 'face'
                }
            ],
            'objectGroups': [
                {
                    'name': 'main',
                    'objectClasses': [
                        'car'
                    ]
                },
                {
                    'name': 'sub',
                    'objectClasses': [
                        'road',
                        'tree',
                        'face'
                    ]
                }
            ],
            'keypointInterfaces': [
                {
                    'name': 'face',
                    'points': [
                        'left eye center',
                        'left eye inner corner',
                        'left eye outer corner',
                        'right eye center',
                        'right eye inner corner',
                        'right eye outer corner',
                        'left eyebrow inner end',
                        'left eyebrow outer end',
                        'right eyebrow inner end',
                        'right eyebrow outer end',
                        'nose tip',
                        'mouth left corner',
                        'mouth right corner',
                        'mouth center top lip',
                        'mouth center bottom lip'
                    ]
                }
            ]
        },
        'imageCategorization': [
            {
                'name': 'Image Categorization',
                'type': 'Multiple Selection',
                'options': [
                    {
                        'name': 'animal',
                        'children': [
                            {
                                'name': 'dog'
                            },
                            {
                                'name': 'cat'
                            }
                        ]
                    },
                    {
                        'name': 'person',
                        'children': [
                            {
                                'name': 'man',
                                'children': [
                                    {
                                        'name': 'taesang'
                                    },
                                    {
                                        'name': 'jonghyuk'
                                    }
                                ]
                            },
                            {
                                'name': 'woman',
                                'children': [
                                    {
                                        'name': 'seohee'
                                    },
                                    {
                                        'name': 'jieun'
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
}


def test_project_model():
    project = Project(dummy_project)
    print(project)
    print(project.summary.objectDetection.annotationTypes)
    print(project.summary.objectDetection.keypointInterfaces[0].points)

    assert isinstance(project.summary.objectDetection.keypointInterfaces[0].points, list)
    assert len(project.summary.objectDetection.keypointInterfaces[0].points) == 15

    print('---- print project model attributes ----')
    print(str(project))
    print('---- print project summary inner model attributes ----')
    print(str(project.summary))


if __name__ == '__main__':
    test_project_model()

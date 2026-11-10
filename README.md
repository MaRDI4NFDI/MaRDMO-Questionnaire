# MaRDMO-Questionnaire

This repository contains the questionnaire for the [MaRDMO-Export-Plugin](https://github.com/MarcoReidelbach/MaRDMO-Export-Plugin) developed within Task Area 4 "Interdisciplinary Mathematics" of the [Mathematical Research Data Initiative](https://www.mardi4nfdi.de/about/mission) (MaRDI). 

## Structure of the MaRDMO-Questionnaire directory

```bash
. 
├── catalog - Questionnaire Files 
│   ├── conditions.xml - individual conditions of Questionnaire 
│   ├── attributes.xml - individual domains of Questionnaire 
│   ├── optionsets.xml - individual options of Questionnaire
│   ├── mardmo-model-catalog.xml - Model Questionnaire
│   ├── mardmo-algorithm-catalog.xml - Algorithm Questionnaire
│   ├── mardmo-interdisciplinary-workflow-catalog.xml - Interdisciplinary Workflow Questionnaire 
│   └── mardmo-search-catalog.xml - Search Questionnaire
│ 
├── ci
│   └── check_catalog.py - Checks of the catalog files
│ 
└── LICENSE.md 
```

## Usage of MaRDMO-Questionaire

Check out the [MaRDI-Export-Plugin](https://github.com/MarcoReidelbach/MaRDMO-Export-Plugin) for further information.  

## Checks

Every push and pull request runs two checks (`.github/workflows/checks.yml`):

- **Catalog files** (`ci/check_catalog.py`): all files are well-formed XML; every referenced element (attribute, option set, option, question, question set, page, section, catalog, condition) is defined; no element is defined twice in a file or differently in two files (RDMO imports one element per URI, the file imported last would win); every widget type is known to the latest RDMO release; every text is given in English and German.
- **MaRDMO tests**: the tests of the [MaRDMO-Plugin](https://github.com/MaRDI4NFDI/MaRDMO-Plugin) with this questionnaire, which also import it into RDMO. The plugin branch is the one with the same name as this branch, else the one of the integration branch (e.g. `0.8.0`) this branch is based on, else `main`.

To check the catalog files locally (needs RDMO, `pip install rdmo`):

```bash
python ci/check_catalog.py catalog
```
